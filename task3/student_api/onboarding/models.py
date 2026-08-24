from django.db import models

# Create your models here.

from django.db import models


class StudentOnboarding(models.Model):
    student_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    parent_consent = models.CharField(max_length=3)
    special_support_required = models.CharField(max_length=3)
    previous_school = models.CharField(max_length=150)

    def __str__(self):
        return self.student_name
