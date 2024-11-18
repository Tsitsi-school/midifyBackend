# api/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Upload, Profile
from .serializers import UploadSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView




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
    permission_classes = [IsAuthenticated]  # Ensure only logged-in users can access this endpoint

    def get(self, request):
        # Fetch all uploads for the logged-in user
        uploads = Upload.objects.filter(user=request.user)
        serializer = UploadSerializer(uploads, many=True)
        return Response(serializer.data)
