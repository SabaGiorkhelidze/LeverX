from rest_framework import serializers
from .models import Course, Lecture, Homework, Submission, Grade, Comment

class course_serializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'created_by', 'teachers', 'students']

class lecture_serializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'course', 'topic', 'presentation']

class homework_serializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['id', 'lecture', 'description']

class submission_serializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'homework', 'student', 'content', 'submitted_at']

class grade_serializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'submission', 'value', 'teacher_comment']

class comment_serializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'grade', 'user', 'text', 'created_at']