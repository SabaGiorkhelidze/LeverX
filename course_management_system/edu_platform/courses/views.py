# edu_platform/courses/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Course, Lecture, Homework, Submission, Grade, Comment
from .serializers import (
    UserSerializer, CourseSerializer, LectureSerializer,
    HomeworkSerializer, SubmissionSerializer, GradeSerializer, CommentSerializer
)
from .permissions import IsTeacher, IsCourseCreator, IsCourseTeacher, IsEnrolledStudent, IsSubmissionOwner
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsTeacher(), IsCourseCreator()]
        if self.action in ['update', 'partial_update', 'add_teacher', 'remove_teacher']:
            return [IsTeacher(), IsCourseCreator()]
        if self.action in ['create', 'add_student']:
            return [IsTeacher()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['post'], permission_classes=[IsCourseTeacher])
    def add_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        student = User.objects.get(id=student_id, role='student')
        course.students.add(student)
        return Response({'status': 'student added'})

    @action(detail=True, methods=['post'], permission_classes=[IsCourseCreator])
    def add_teacher(self, request, pk=None):
        course = self.get_object()
        teacher_id = request.data.get('teacher_id')
        teacher = User.objects.get(id=teacher_id, role='teacher')
        course.teachers.add(teacher)
        return Response({'status': 'teacher added'})

    @action(detail=True, methods=['post'], permission_classes=[IsCourseCreator])
    def remove_teacher(self, request, pk=None):
        course = self.get_object()
        teacher_id = request.data.get('teacher_id')
        teacher = User.objects.get(id=teacher_id, role='teacher')
        if teacher == course.created_by:
            return Response({'error': 'Cannot remove course creator'}, status=400)
        course.teachers.remove(teacher)
        return Response({'status': 'teacher removed'})

class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacher(), IsCourseTeacher()]
        return [IsAuthenticated(), IsEnrolledStudent()]

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacher(), IsCourseTeacher()]
        return [IsAuthenticated(), IsEnrolledStudent()]

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsEnrolledStudent()]
        return [IsAuthenticated(), IsSubmissionOwner()]

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsTeacher(), IsCourseTeacher()]
        return [IsAuthenticated(), IsSubmissionOwner()]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsSubmissionOwner()]