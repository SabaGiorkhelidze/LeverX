from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification


# Create your views here.
class user_view_set(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['post'], permission_classes=[])
    def register(self, request):
        serializer =  UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Notification.objects.create(
                user=user,
                message=f"Welcome {user.email}! You have successfully registered as a {user.role}."
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer