from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db.models import Avg
from .models import Course, Lecture, Homework, Submission, Grade, Comment
from .serializers import course_serializer, lecture_serializer, homework_serializer, submission_serializer, grade_serializer, comment_serializer
# from  users.serializers import UserSerializer
from .permissions import is_course_creator, is_course_teacher, is_enrolled_student, is_submission_owner, is_owner_or_course_teacher
from users.permissions import IsTeacher
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification
from users.models import User
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = course_serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Course.objects.none()
        if user.role == 'teacher':
            return (Course.objects.filter(teachers=user) | Course.objects.filter(created_by=user)).distinct()
        if user.role == 'student':
            return Course.objects.filter(students=user)
        return Course.objects.none()

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsTeacher(), is_course_creator()]
        if self.action in ['update', 'partial_update', 'add_teacher', 'remove_teacher']:
            return [IsTeacher(), is_course_creator()]
        if self.action in ['create', 'add_student', 'remove_student']:
            return [IsTeacher()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        course = serializer.save(created_by=self.request.user)
        Notification.objects.create(
            user=self.request.user,
            message=f"You created a new course: {course.title}"
        )

    @action(detail=True, methods=['post'], permission_classes=[is_course_teacher])
    def add_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        try:
            student = User.objects.get(id=student_id, role='student')
        except User.DoesNotExist:
            return Response({'error': 'Student not found'}, status=400)
        course.students.add(student)
        Notification.objects.create(
            user=student,
            message=f"You have been added to the course: {course.title}"
        )
        return Response({'status': 'student added'})

    @action(detail=True, methods=['post'], permission_classes=[is_course_teacher])
    def remove_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        try:
            student = User.objects.get(id=student_id, role='student')
        except User.DoesNotExist:
            return Response({'error': 'Student not found'}, status=400)
        if student not in course.students.all():
            return Response({'error': 'Student not enrolled'}, status=400)
        course.students.remove(student)
        Notification.objects.create(
            user=student,
            message=f"You have been removed from the course: {course.title}"
        )
        return Response({'status': 'student removed'})

    @action(detail=True, methods=['post'], permission_classes=[is_course_creator])
    def add_teacher(self, request, pk=None):
        course = self.get_object()
        teacher_id = request.data.get('teacher_id')
        try:
            teacher = User.objects.get(id=teacher_id, role='teacher')
        except User.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=400)
        course.teachers.add(teacher)
        Notification.objects.create(
            user=teacher,
            message=f"You have been added as a teacher to the course: {course.title}"
        )
        return Response({'status': 'teacher added'})

    @action(detail=True, methods=['post'], permission_classes=[is_course_creator])
    def remove_teacher(self, request, pk=None):
        course = self.get_object()
        teacher_id = request.data.get('teacher_id')
        try:
            teacher = User.objects.get(id=teacher_id, role='teacher')
        except User.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=400)
        if teacher == course.created_by:
            return Response({'error': 'Cannot remove course creator'}, status=400)
        course.teachers.remove(teacher)
        Notification.objects.create(
            user=teacher,
            message=f"You have been removed as a teacher from the course: {course.title}"
        )
        return Response({'status': 'teacher removed'})

    @action(detail=True, methods=['get'], permission_classes=[is_course_teacher])
    def analytics(self, request, pk=None):
        course = self.get_object()
        submissions = Submission.objects.filter(
            homework__lecture__course=course,
            status='graded'
        )
        avg_grade = submissions.aggregate(Avg('grade__value'))['grade__value__avg'] or 0
        total_submissions = submissions.count()
        total_students = course.students.count()
        return Response({
            'course': course.title,
            'average_grade': round(avg_grade, 2),
            'total_submissions': total_submissions,
            'total_students': total_students,
        })

class LectureViewSet(viewsets.ModelViewSet):
    serializer_class = lecture_serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Lecture.objects.none()
        if user.role == 'teacher':
            courses = (Course.objects.filter(teachers=user) | Course.objects.filter(created_by=user)).distinct()
        elif user.role == 'student':
            courses = Course.objects.filter(students=user)
        else:
            return Lecture.objects.none()
        return Lecture.objects.filter(course__in=courses)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacher(), is_course_teacher()]
        return [IsAuthenticated(), is_enrolled_student()]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if self.request.user not in course.teachers.all() and self.request.user != course.created_by:
            raise PermissionDenied("You are not a teacher of this course.")
        serializer.save()

class HomeworkViewSet(viewsets.ModelViewSet):
    serializer_class = homework_serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Homework.objects.none()
        if user.role == 'teacher':
            courses = (Course.objects.filter(teachers=user) | Course.objects.filter(created_by=user)).distinct()
        elif user.role == 'student':
            courses = Course.objects.filter(students=user)
        else:
            return Homework.objects.none()
        return Homework.objects.filter(lecture__course__in=courses)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacher(), is_course_teacher()]
        return [IsAuthenticated(), is_enrolled_student()]

    def perform_create(self, serializer):
        lecture = serializer.validated_data['lecture']
        course = lecture.course
        if self.request.user not in course.teachers.all() and self.request.user != course.created_by:
            raise PermissionDenied("You are not a teacher of this course.")
        homework = serializer.save()
        for student in course.students.all():
            Notification.objects.create(
                user=student,
                message=f"New homework assigned in {course.title}: {homework.description[:50]}"
            )

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = submission_serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Submission.objects.none()
        if user.role == 'student':
            return Submission.objects.filter(student=user)
        elif user.role == 'teacher':
            courses = (Course.objects.filter(teachers=user) | Course.objects.filter(created_by=user)).distinct()
            return Submission.objects.filter(homework__lecture__course__in=courses)
        return Submission.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), is_enrolled_student()]
        return [IsAuthenticated(), is_owner_or_course_teacher()]

    def perform_create(self, serializer):
        homework = serializer.validated_data['homework']
        course = homework.lecture.course
        if self.request.user not in course.students.all():
            raise PermissionDenied("You are not enrolled in this course.")
        serializer.save(student=self.request.user)

    def perform_update(self, serializer):
        submission = self.get_object()
        if submission.status == 'graded':
            raise ValidationError("Cannot update graded submission.")
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[is_submission_owner])
    def submit(self, request, pk=None):
        submission = self.get_object()
        if submission.status != 'draft':
            return Response({'error': 'Submission is not in draft state'}, status=400)
        submission.status = 'submitted'
        submission.save()
        course = submission.homework.lecture.course
        for teacher in course.teachers.all():
            Notification.objects.create(
                user=teacher,
                message=f"{submission.student.email} submitted homework for {course.title}"
            )
        return Response({'status': 'submission submitted'})

class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = grade_serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Grade.objects.none()
        if user.role == 'student':
            return Grade.objects.filter(submission__student=user)
        elif user.role == 'teacher':
            courses = (Course.objects.filter(teachers=user) | Course.objects.filter(created_by=user)).distinct()
            return Grade.objects.filter(submission__homework__lecture__course__in=courses)
        return Grade.objects.none()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsTeacher(), is_course_teacher()]
        return [IsAuthenticated(), is_owner_or_course_teacher()]

    def perform_create(self, serializer):
        submission = serializer.validated_data['submission']
        if hasattr(submission, 'grade') and submission.grade:
            raise ValidationError("Grade already exists for this submission.")
        course = submission.homework.lecture.course
        if self.request.user not in course.teachers.all() and self.request.user != course.created_by:
            raise PermissionDenied("You are not a teacher of this course.")
        grade = serializer.save()
        submission.status = 'graded'
        submission.save()
        Notification.objects.create(
            user=submission.student,
            message=f"Your submission for {course.title} has been graded: {grade.value}"
        )

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = comment_serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Comment.objects.none()
        if user.role == 'student':
            return Comment.objects.filter(grade__submission__student=user)
        elif user.role == 'teacher':
            courses = (Course.objects.filter(teachers=user) | Course.objects.filter(created_by=user)).distinct()
            return Comment.objects.filter(grade__submission__homework__lecture__course__in=courses)
        return Comment.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthenticated(), is_owner_or_course_teacher()]

    def perform_create(self, serializer):
        grade = serializer.validated_data['grade']
        submission = grade.submission
        course = submission.homework.lecture.course
        user = self.request.user
        if user.role == 'student' and user != submission.student:
            raise PermissionDenied("You can only comment on your own grades.")
        if user.role == 'teacher' and (user not in course.teachers.all() and user != course.created_by):
            raise PermissionDenied("You are not a teacher of this course.")
        if user.role not in ('student', 'teacher'):
            raise PermissionDenied("Only students and teachers can add comments.")
        serializer.save(user=user)
        recipient = submission.student if user.role == 'teacher' else course.created_by
        Notification.objects.create(
            user=recipient,
            message=f"New comment on grade for {course.title} by {user.email}"
        )