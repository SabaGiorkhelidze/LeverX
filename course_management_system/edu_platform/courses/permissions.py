from rest_framework.permissions import BasePermission
from .models import Course, Lecture, Homework, Submission, Grade, Comment

    
class is_course_creator(BasePermission):
    def has_object_permission(self, request, view, obj):
        course = self._get_course(obj)
        if course is None:
            return False
        return request.user == obj.created_by
    
    def _get_course(self, obj):
        if isinstance(obj, Course):
            return obj
        elif isinstance(obj, (Lecture, Homework, Submission, Grade, Comment)):
            return self._get_course_from_related(obj)
        return None
    
    def _get_course_from_related(self, obj):
        if isinstance(obj, Lecture):
            return obj.course
        elif isinstance(obj, Homework):
            return obj.lecture.course
        elif isinstance(obj, Submission):
            return obj.homework.lecture.course
        elif isinstance(obj, Grade):
            return obj.submission.homework.lecture.course
        elif isinstance(obj, Comment):
            return obj.grade.submission.homework.lecture.course
        return None


class is_course_teacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "teacher"
    
    def has_object_permission(self, request, view, obj):
        course = self._get_course(obj)
        if course is None:
            return False
        return request.user in course.teachers.all() or request.user == course.created_by
    
    def _get_course(self, obj):
        if isinstance(obj, Course):
            return obj
        elif isinstance(obj, (Lecture, Homework, Submission, Grade, Comment)):
            return self._get_course_from_related(obj)
        return None

    def _get_course_from_related(self, obj):
        if isinstance(obj, Lecture):
            return obj.course
        elif isinstance(obj, Homework):
            return obj.lecture.course
        elif isinstance(obj, Submission):
            return obj.homework.lecture.course
        elif isinstance(obj, Grade):
            return obj.submission.homework.lecture.course
        elif isinstance(obj, Comment):
            return obj.grade.submission.homework.lecture.course
        return None

class is_enrolled_student(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"

    def has_object_permission(self, request, view, obj):
        course = self._get_course(obj)
        if course is None:
            return False
        return request.user in course.students.all()

    def _get_course(self, obj):
        if isinstance(obj, Course):
            return obj
        elif isinstance(obj, (Lecture, Homework, Submission, Grade, Comment)):
            return self._get_course_from_related(obj)
        return None

    def _get_course_from_related(self, obj):
        if isinstance(obj, Lecture):
            return obj.course
        elif isinstance(obj, Homework):
            return obj.lecture.course
        elif isinstance(obj, Submission):
            return obj.homework.lecture.course
        elif isinstance(obj, Grade):
            return obj.submission.homework.lecture.course
        elif isinstance(obj, Comment):
            return obj.grade.submission.homework.lecture.course
        return None

class is_submission_owner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"

    def has_object_permission(self, request, view, obj):
        submission = self._get_submission(obj)
        if submission is None:
            return False
        return request.user == submission.student

    def _get_submission(self, obj):
        if isinstance(obj, Submission):
            return obj
        elif isinstance(obj, Grade):
            return obj.submission
        elif isinstance(obj, Comment):
            return obj.grade.submission
        return None

class is_owner_or_course_teacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        submission = self._get_submission(obj)
        if submission is None:
            return False
        course = submission.homework.lecture.course
        if request.user == submission.student:
            return True
        if request.user.role == 'teacher' and (request.user in course.teachers.all() or request.user == course.created_by):
            return True
        return False

    def _get_submission(self, obj):
        if isinstance(obj, Submission):
            return obj
        elif isinstance(obj, Grade):
            return obj.submission
        elif isinstance(obj, Comment):
            return obj.grade.submission
        return None
    def has_object_permission(self, request, view, obj):
        return request.user == obj.student