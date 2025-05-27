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
    major = models.CharField(max_length=100, choices=MAJOR_CHOICES)




class ClassName(models.Model):
    name = models.CharField(max_length=100, unique=True)
    max_size = models.IntegerField()



class StudentClass(models.Model):
    student = models.ForeignKey(Student, to_field='student_id', on_delete=models.CASCADE)
    classname = models.ForeignKey(ClassName, to_field='name', on_delete=models.PROTECT)
    registered_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)


