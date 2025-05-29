import re
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from students.models import Student, ClassName, StudentClass, Location, Schedule, Teacher
from students.crud_students.validations import StudentValidationMixin



class StudentSerializer(StudentValidationMixin, serializers.ModelSerializer):
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
    major = serializers.ChoiceField(choices=MAJOR_CHOICES)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    class Meta:
        model = Student
        fields = '__all__'


class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = '__all__'


class ClassNameSerializer(StudentValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = ClassName
        fields = '__all__'




class TeacherSerializer(StudentValidationMixin, serializers.ModelSerializer):
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
    major = serializers.ChoiceField(choices=MAJOR_CHOICES)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    class Meta:
        model = Teacher
        fields = '__all__'


class LocationSerializer(StudentValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'



class ScheduleSerializer(StudentValidationMixin, serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = '__all__'