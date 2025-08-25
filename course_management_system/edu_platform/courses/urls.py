from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, LectureViewSet, HomeworkViewSet,
    SubmissionViewSet, GradeViewSet, CommentViewSet
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lectures', LectureViewSet, basename='lecture')
router.register(r'homework', HomeworkViewSet, basename='homework')
router.register(r'submissions', SubmissionViewSet, basename='submission')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]