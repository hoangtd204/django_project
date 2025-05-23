from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    MAJOR_CHOICES = [
        ("Biotechnology", "Biotechnology"),
        ("Graphic Design", "Graphic Design"),
        ("Data Science", "Data Science"),
        ("Software Engineering", "Software Engineering"),
        ("Cybersecurity", "Cybersecurity"),
        ("Cloud Computing", "Cloud Computing"),
    ]
    student_id = models.CharField(max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^PH\d{5}$',
                message='Student ID must start with "PH" followed by 5 digits (ex:PH12345)'
            )
        ])
    name = models.CharField(max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z ]+$',
                message='Only letters (A–Z, a–z) and spaces are allowed.'
            )
        ])
    age = models.IntegerField(validators=[
            MinValueValidator(10, message="Age must be at least 10."),
            MaxValueValidator(100, message="Age must be at most 100."),
        ])
    major = models.CharField(max_length=50, choices=MAJOR_CHOICES)

    class Meta:
        db_table = 'infor'

# class StudentClass(models.Model):
#