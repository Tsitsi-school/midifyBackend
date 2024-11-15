# api/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Upload, Profile
from .serializers import UploadSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

@api_view(['GET'])
def api_overview(request):
    return Response({
        "message": "Welcome to the Midify API!",
    })

# ViewSet for managing uploads
class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer

    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get upload history for the current user"""
        uploads = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(uploads, many=True)
        return Response(serializer.data)

# ViewSet for managing profiles
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer