from django.db import models

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    instructor = models.CharField(max_length=150)

    DURATION_CHOICES = [('1', '2 Weeks'), ('2', '8 Weeks')]
    duration = models.CharField(max_length=7, choices=DURATION_CHOICES)

    # Don't require file upload
    image = models.ImageField('course_art/', null=True, blank=True)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title','description','instructor','duration','image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Name it something good'}),
            'description': forms.Textarea(attrs={'rows':3}),
            'instructor': forms.TextInput(attrs={'placeholder': 'Django Guru'}),
        }
        labels = {
            'title': 'Course Title',
            'image': 'Art',
        }
        help_texts = {
            'description': 'Provide some information about what students will learn.',
        }


