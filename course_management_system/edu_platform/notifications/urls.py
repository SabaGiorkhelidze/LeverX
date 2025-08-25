from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import notification_view_set

router = DefaultRouter()
router.register(r'', notification_view_set, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]