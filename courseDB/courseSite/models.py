from django.db import models

# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=128, unique=True)
    department = models.CharField(max_length=5)
    number = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name
