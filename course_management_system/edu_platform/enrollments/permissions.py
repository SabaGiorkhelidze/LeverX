from rest_framework.permissions import BasePermission
from courses.models import Course

class is_enrollment_course_teacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "teacher"

    def has_object_permission(self, request, view, obj):
        course = obj.course
        return request.user in course.teachers.all() or request.user == course.created_by