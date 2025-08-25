from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        username = validated_data['email'].replace('@', '_').replace('.', '_')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=username,  
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user
    
    




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise exceptions.AuthenticationFailed('Email and password are required.')

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('No user found with this email.')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect password.')

        attrs['username'] = email  # Map email to username for JWT
        return super().validate(attrs)