# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UploadViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'upload', UploadViewSet)
router.register(r'profile', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = [
#     path('', views.api_overview, name="api-overview"), // for testing api
# ]
