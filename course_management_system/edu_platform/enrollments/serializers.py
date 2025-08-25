from rest_framework import serializers
from .models import EnrollmentRequest

class enrollment_request_serializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentRequest
        fields = ['id', 'student', 'course', 'status', 'created_at']
        read_only_fields = ['student', 'created_at']