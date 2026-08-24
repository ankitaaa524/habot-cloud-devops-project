from django.db import models


class StudentOnboarding(models.Model):
    student_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    parent_consent = models.CharField()
    special_support_required = models.CharField()
    previous_school = models.CharField(max_length=150)

    def __str__(self):
        return self.student_name