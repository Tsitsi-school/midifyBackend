# api/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Upload, Profile
from .serializers import UploadSerializer, ProfileSerializer, UploadHistorySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.middleware.csrf import get_token


# ViewSet for managing uploads
class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        # Only return uploads for the logged-in user
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        print("Request user:", self.request.user)
        print("Is authenticated:", self.request.user.is_authenticated)
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)

    @action(detail=True, methods=["post"])
    def convert(self, request, pk=None):
        # Simulate starting a conversion process, Start file conversion.

        upload = self.get_object()
        upload.status = "processing"
        upload.save()
        return Response({"status": "Processing started."}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["get"])
    def status(self, request, pk=None):
        # Return the current status of the file, Check the status of a file conversion.

        upload = self.get_object()
        return Response({"status": upload.status}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        # Return the converted file for download, Download a converted MIDI file.

        upload = self.get_object()
        if upload.converted_file:
            return Response({"file_url": upload.converted_file.url}, status=status.HTTP_200_OK)
        return Response({"error": "File not converted yet."}, status=status.HTTP_400_BAD_REQUEST)


# ViewSet for managing profiles
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Dynamically create a profile if it doesn't exist
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        # Update user profile details.

        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    

class UploadHistoryView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        # Fetch all uploads for the logged-in user
        uploads = Upload.objects.filter(user=request.user)
        serializer = UploadHistorySerializer(uploads, many=True)
        return Response(serializer.data)

class RegisterUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Print the request data for debugging
        print("Request data:", request.data)
        response = super().post(request, *args, **kwargs)
        print("Response data:", response.data)
        return response
    
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        # Log the request data
        if request:
            print("Request received:", request.data)
        else:
            print("No request received")
        
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            # Ensure the user is active
            if not user.is_active:
                return Response({"error": "User account is disabled."}, status=status.HTTP_401_UNAUTHORIZED)

            # Generate or retrieve token
            token, _ = Token.objects.get_or_create(user=user)

            # Return the token
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    

   
def test_view(request):
        print("Request received:", request)
        return JsonResponse({"message": "Test endpoint reached"})

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})