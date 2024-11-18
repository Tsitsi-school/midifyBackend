# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UploadViewSet, ProfileView, UploadHistoryView

router = DefaultRouter()
router.register(r'upload', UploadViewSet, basename='upload')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('history/', UploadHistoryView.as_view(), name='upload-history'),
]

