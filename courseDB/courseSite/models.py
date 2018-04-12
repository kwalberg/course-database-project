from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.


class Course(models.Model):
    # Ex: COMP 225-01
    course_id = models.CharField(max_length=20)
    full_title = models.CharField(max_length=250)
    course_number = models.IntegerField()
    department = models.CharField(max_length=5)
    description = models.TextField()
    instructor = models.CharField(max_length=150)
    days = models.CharField(max_length=5)
    times = models.CharField(max_length=10)

    def __str__(self):
        return self.course_id

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add='true')
    cost = models.IntegerField(null=True)
    difficulty = models.IntegerField(null=True)
    recommend = models.IntegerField(null=True)


