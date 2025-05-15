from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    major = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.student_id})"
