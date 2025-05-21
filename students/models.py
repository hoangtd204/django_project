from django.db import models

class Student(models.Model):
    MAJOR_CHOICES = [
        ("Biotechnology", "Biotechnology"),
        ("Graphic Design", "Graphic Design"),
        ("Data Science", "Data Science"),
        ("Software Engineering", "Software Engineering"),
        ("Cybersecurity", "Cybersecurity"),
        ("Cloud Computing", "Cloud Computing"),
    ]
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    major = models.CharField(max_length=50, choices=MAJOR_CHOICES)

    class Meta:
        db_table = 'infor'

