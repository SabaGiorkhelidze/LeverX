from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
    

class Course(models.Model):
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_courses")
    teachers = models.ManyToManyField(User, related_name="teaching_courses")
    students = models.ManyToManyField(User, related_name="enrolled_courses")

    
    def clean(self):
        if self.created_by and self.pk and self.created_by not in self.teachers.all():
            raise ValidationError("The course creator must remain a teacher.")
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.created_by and self.created_by not in self.teachers.all():
            self.teachers.add(self.created_by)

    def __str__(self):
        return self.title
    
    
class Lecture(models.Model):
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lectures")
    topic = models.CharField(max_length=200)
    presentation = models.FileField(upload_to='presentations/')
    
    def __str__(self):
        return f"{self.topic} ({self.course})"
    
    
class Homework(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='homework')
    description = models.TextField()
    
    def __str__(self):
        return f"Homework for {self.lecture}"

class Submission(models.Model):
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    )
    
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Submission by {self.student} for {self.homework}"

    

class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grade')
    value = models.IntegerField()
    teacher_comment = models.TextField(blank=True)
    
    def __str__(self):
        return f"Grade {self.value} for {self.submission}"

class Comment(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user} on {self.grade}"