from rest_framework.permissions import BasePermission

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "teacher"
    
class IsCourseCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.created_by
    
class IsCourseTeacher(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.teachers.all() or request.user == obj.created_by

class IsEnrolledStudent(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.students.all()

class IsSubmissionOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.student