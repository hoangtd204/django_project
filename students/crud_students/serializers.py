from rest_framework import serializers
from students.models import Student, ClassName, StudentClass, Location, Schedule, Teacher
from students.crud_students.Validations.validations_for_student import ValidationMixin



class StudentSerializer(ValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'





class ClassNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassName
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = '__all__'


class StudentClassSerializer(serializers.ModelSerializer):
    class_info = ClassNameSerializer(source='class_id', read_only=True)
    schedule_info = ScheduleSerializer(source='schedule', read_only=True)

    class Meta:
        model = StudentClass
        fields = [
            'student_id',
            'class_id',
            'schedule',
            'registered_at',
            'learning_status',
            'class_info',
            'schedule_info'
        ]

    def validate(self, data):
        student_id  = data.get('student_id')
        class_id  = data.get('class_id')


        if StudentClass.objects.filter(student_id=student_id, class_id=class_id).exists():
            raise serializers.ValidationError("This student already registered.")
        return data

class TeacherSerializer(ValidationMixin, serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'



