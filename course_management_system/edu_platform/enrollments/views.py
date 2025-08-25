from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import EnrollmentRequest
from .serializers import enrollment_request_serializer
from .permissions import is_enrollment_course_teacher
from users.permissions import IsTeacher
from courses.permissions import is_enrolled_student
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification
from courses.models import Course

class EnrollmentRequestViewSet(viewsets.ModelViewSet):
    serializer_class = enrollment_request_serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return EnrollmentRequest.objects.filter(student=user)
        if user.role == 'teacher':
            courses = (Course.objects.filter(teachers=user) | Course.objects.filter(created_by=user)).distinct()
            return EnrollmentRequest.objects.filter(course__in=courses)
        return EnrollmentRequest.objects.none()

    def get_permissions(self):
        if self.action in ['create']:
            return [is_enrolled_student()]
        if self.action in ['update', 'partial_update', 'destroy', 'approve', 'reject']:
            return [IsTeacher(), is_enrollment_course_teacher()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if EnrollmentRequest.objects.filter(student=self.request.user, course=course).exists():
            raise ValidationError("Enrollment request already exists.")
        if self.request.user in course.students.all():
            raise ValidationError("You are already enrolled in this course.")
        serializer.save(student=self.request.user)
        for teacher in course.teachers.all():
            Notification.objects.create(
                user=teacher,
                message=f"{self.request.user.email} requested to enroll in your course: {course.title}"
            )

    @action(detail=True, methods=['post'], permission_classes=[is_enrollment_course_teacher])
    def approve(self, request, pk=None):
        enrollment_request = self.get_object()
        if enrollment_request.status != 'pending':
            return Response({'error': 'Request is not pending'}, status=400)
        enrollment_request.status = 'approved'
        enrollment_request.save()
        enrollment_request.course.students.add(enrollment_request.student)
        Notification.objects.create(
            user=enrollment_request.student,
            message=f"Your enrollment request for {enrollment_request.course.title} has been approved."
        )
        return Response({'status': 'enrollment approved'})

    @action(detail=True, methods=['post'], permission_classes=[is_enrollment_course_teacher])
    def reject(self, request, pk=None):
        enrollment_request = self.get_object()
        if enrollment_request.status != 'pending':
            return Response({'error': 'Request is not pending'}, status=400)
        enrollment_request.status = 'rejected'
        enrollment_request.save()
        Notification.objects.create(
            user=enrollment_request.student,
            message=f"Your enrollment request for {enrollment_request.course.title} has been rejected."
        )
        return Response({'status': 'enrollment rejected'})