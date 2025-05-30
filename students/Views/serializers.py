from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError
from students.models import Student, ClassName, StudentClass, Location, Schedule, Teacher
from students.Validations.validations_for_student import ValidationMixin
from students.Validations.validations_for_all import validate_max_size


def get_instance_by_id(model, pk, field_name):
    """Helper function to retrieve model instance by primary key or return as-is if already an instance."""
    if isinstance(pk, (int, str)):
        try:
            return model.objects.get(pk=pk)
        except model.DoesNotExist:
            raise DRFValidationError({field_name: f"{model.__name__} not found."})
    return pk


class StudentSerializer(ValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Nếu update (instance tồn tại) thì student_id thành read_only để không bắt buộc gửi
        if self.instance:
            self.fields['student_id'].read_only = True

    def validate(self, attrs):
        if self.instance and 'student_id' in attrs:
            raise serializers.ValidationError({
                'student_id': 'Student ID cannot be updated.'
            })
        return attrs


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
    def validate(self, data):
        room_number  = data.get('room_number')
        if not room_number:
            raise DRFValidationError({'schedule_id': 'This field is required.'})
        location_instance = get_instance_by_id(Location, room_number, 'schedule_id')
        if not hasattr(location_instance, 'max_size') or location_instance.max_size is None:
            raise DRFValidationError({'schedule_id': 'Schedule missing max_size field or value.'})
        try:
            validate_max_size(
                Schedule,
            'room_number',
                location_instance,
                location_instance.max_size,
                label='Location' )
        except DjangoValidationError as e:
            raise DRFValidationError({'room_number': e.messages})

        return data


class ClassNameSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer()
    class Meta:
        model = ClassName
        fields = ['class_id', 'class_name', 'teacher', 'schedule_id',' max_size', 'start_date', 'end_date', 'schedule']

    def validate(self, data):
        schedule_obj = data.get('schedule_id')

        if not schedule_obj:
            raise DRFValidationError({'schedule_id': 'This field is required.'})

        schedule_instance = get_instance_by_id(Schedule, schedule_obj, 'schedule_id')

        if not hasattr(schedule_instance, 'max_size') or schedule_instance.max_size is None:
            raise DRFValidationError({'schedule_id': 'Schedule missing max_size field or value.'})

        try:
            validate_max_size(
                ClassName,
                'schedule_id',
                schedule_instance,
                schedule_instance.max_size,
                label='Schedule'
            )
        except DjangoValidationError as e:
            raise DRFValidationError({'schedule_id': e.messages})

        return data


class StudentClassSerializer(serializers.ModelSerializer):
    class_info = ClassNameSerializer(source='class_id', read_only=True)
    class_name = ClassNameSerializer()
    student_name = serializers.CharField(source='student.name')  # hoặc student_id tùy bạn

    class Meta:
        model = StudentClass
        fields = [
            'student_id',
            'class_id',
            'registered_at',
            'learning_status',
            'class_name'

        ]

    def validate(self, data):
        class_instance = get_instance_by_id(ClassName, data.get('class_id'), 'class_id')
        student_instance = get_instance_by_id(Student, data.get('student_id'), 'student_id')

        try:
            validate_max_size(
                StudentClass,
                'class_id',
                class_instance,
                class_instance.max_size,
                label='Class'
            )
        except DjangoValidationError as e:
            raise DRFValidationError({'class_id': e.messages})

        if StudentClass.objects.filter(student_id=student_instance, class_id=class_instance).exists():
            raise DRFValidationError({
                'non_field_errors': ['Student already registered in this class.']
            })

        return data

class TeacherSerializer(ValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
