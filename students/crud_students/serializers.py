import re
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from students.models import Student, ClassName, StudentClass


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def validate_student_id(self, value):
        if not re.match(r'^PH\d{5}$', value):
            raise serializers.ValidationError('Student ID must start with "PH" followed by 5 digits (ex: PH12345)')
        return value

    def validate_name(self, value):
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError('Only letters (A–Z, a–z) and spaces are allowed.')
        return value

    def validate_age(self, value):
        if value < 10 or value > 100:
            raise serializers.ValidationError('Age must be between 10 and 100.')
        return value

    def validate_major(self, value):
        majors = [choice[0] for choice in Student.MAJOR_CHOICES]
        if value not in majors:
            raise serializers.ValidationError(f'Major must be one of {majors}')
        return value

    def to_internal_value(self, value):
        allowed = set(self.fields.keys())
        incoming = set(value.keys())
        extra = incoming - allowed
        if extra:
            raise serializers.ValidationError(
                {field: "This field is not allowed." for field in extra}
            )
        return super().to_internal_value(value)


class ClassNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassName
        fields = '__all__'

    def to_internal_value(self, value):
        allowed = set(self.fields.keys())
        incoming = set(value.keys())
        extra = incoming - allowed
        if extra:
            raise serializers.ValidationError(
                {field: "This field is not allowed." for field in extra}
            )
        return super().to_internal_value(value)


class StudentClassSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = StudentClass
        fields = '__all__'

    def to_internal_value(self, value):
        allowed = set(self.fields.keys())
        incoming = set(value.keys())
        extra = incoming - allowed
        if extra:
            raise serializers.ValidationError(
                {field: "This field is not allowed." for field in extra}
            )
        return super().to_internal_value(value)

    def validate(self, data):
        student = data.get('student')
        name = data.get('classname')

        if StudentClass.objects.filter(student=student, classname=name).exists():
            raise serializers.ValidationError("The student has already registered for this class.")

        current_count = StudentClass.objects.filter(classname=name).count()
        if current_count >= name.max_size:
            raise serializers.ValidationError("The class has reached its maximum number of students.")

        return data

    def get_status(self, obj):
        today = timezone.now().date()
        if obj.start_date and obj.end_date:
            if today < obj.start_date:
                return "not_started"
            elif obj.start_date <= today <= obj.end_date:
                return "open"
            else:
                return "done"
        return "unknown"
