from django.db import models
from django import forms

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    instructor = models.CharField(max_length=150)

    DURATION_CHOICES = [('1', '2 Weeks'), ('2', '8 Weeks')]
    duration = models.CharField(max_length=7, choices=DURATION_CHOICES)

    def __str__(self):
        return self.title

    # Don't require file upload
    #image = models.ImageField('course_art/', null=True, blank=True)

