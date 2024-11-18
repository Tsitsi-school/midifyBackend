# api/serializers.py

from rest_framework import serializers
from .models import Upload, Profile

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['id', 'file', 'uploaded_at', 'status', 'converted_file']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'preferred_language']
