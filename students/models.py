from django.db import models

class Student(models.Model):

    student_id = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    major = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    status = models.CharField(max_length=20)

    class Meta:
        db_table = "student"


class Teacher(models.Model):
    teacher_id = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    major = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    status = models.CharField(max_length=20)

    class Meta:
        db_table = "teacher"


class ClassName(models.Model):
    class_id = models.CharField(max_length=10, primary_key=True)
    class_name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        db_table = "class_name"


class StudentClass(models.Model):
    student_id = models.ForeignKey(Student, to_field='student_id', on_delete=models.CASCADE)
    class_id = models.ForeignKey(ClassName, on_delete=models.CASCADE, to_field='class_id')
    registered_at = models.DateTimeField(auto_now_add=True)
    learning_status = models.CharField(max_length=50)

    class Meta:
        unique_together = ('student_id', 'class_id')
        db_table = "student_class"


class Location(models.Model):
    room_number = models.CharField(max_length=10, primary_key=True, unique=True)
    building_name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "location"


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True, unique=True)
    class_id = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    room_number = models.ForeignKey(Location, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = "schedule"