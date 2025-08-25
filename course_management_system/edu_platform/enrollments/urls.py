from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnrollmentRequestViewSet

router = DefaultRouter()
router.register(r'', EnrollmentRequestViewSet, basename='enrollment-request')

urlpatterns = [
    path('', include(router.urls)),
]