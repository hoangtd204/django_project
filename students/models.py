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
    GENDER_CHOICES = [
        ("male", "male"),
        ("female", "female")
    ]
    STATUS_CHOICES = [
        ("studying", "studying"),
        ("dropped out", "dropped out"),
        ("graduated", "graduated")
    ]
    student_id = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    major = models.CharField(max_length=100, choices=MAJOR_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        db_table = "student"


class Teacher(models.Model):
    MAJOR_CHOICES = [
        ("Biotechnology", "Biotechnology"),
        ("Graphic Design", "Graphic Design"),
        ("Data Science", "Data Science"),
        ("Software Engineering", "Software Engineering"),
        ("Cybersecurity", "Cybersecurity"),
        ("Cloud Computing", "Cloud Computing"),
    ]
    GENDER_CHOICES = [
        ("male", "male"),
        ("female", "female")
    ]
    STATUS_CHOICES = [
        ('teaching', 'teaching'),
        ('inactive', 'inactive'),
    ]

    teacher_id = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    major = models.CharField(max_length=100, choices=MAJOR_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        db_table = "teacher"



class Location(models.Model):
    room_number = models.CharField(max_length=10, primary_key=True, unique=True)
    building_name = models.CharField(max_length=100)

    class Meta:
        db_table = "location"


class Schedule(models.Model):
    schedule_id = models.CharField(max_length=20, primary_key=True, unique=True)
    room_number = models.ForeignKey('Location', to_field='room_number', on_delete=models.CASCADE)
    max_size = models.IntegerField()

    class Meta:
        db_table = "schedule"


class ClassName(models.Model):
    class_id = models.CharField(max_length=10, primary_key=True)
    class_name = models.CharField(max_length=100)
    teacher = models.ForeignKey('Teacher', to_field='teacher_id', on_delete=models.CASCADE)
    schedule = models.OneToOneField('Schedule', to_field='schedule_id', on_delete=models.CASCADE)
    max_size = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = "class_name"


class StudentClass(models.Model):
    student_id = models.ForeignKey('Student', to_field='student_id', on_delete=models.CASCADE)
    class_id  = models.ForeignKey('ClassName', to_field='class_id', on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    learning_status = models.CharField(max_length=50)

    class Meta:
        db_table = "student_class"
        unique_together = ('student_id', 'class_id')





