from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    instructor = models.CharField(max_length=150)
    DURATION_CHOICES = [('1', '2 Weeks'), ('2', '8 Weeks')]
    duration = models.CharField(max_length=7, choices=DURATION_CHOICES)
    # Don't require file upload
    # image = models.ImageField('course_art/', null=True, blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    name = models.CharField(max_length=1024)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add='true')
    cost = models.IntegerField(null=True)
    difficulty = models.IntegerField(null=True)
    recommend = models.IntegerField(null=True)


