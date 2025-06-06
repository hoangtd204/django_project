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
        if self.instance:
            self.fields['student_id'].read_only = True

    def update(self, instance, validated_data):
        validated_data.pop('student_id', None)
        return super().update(instance, validated_data)

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['room_number','building_name', 'max_size']

    extra_kwargs = {
        'room_number': {'required': False},
        'building_name': {'required': False},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            for field_name in self.fields:
                if field_name not in ('max_size'):
                    self.fields[field_name].read_only = True

    def update(self, instance, validated_data):
        for field_name in list(validated_data.keys()):
            if field_name not in ('max_size'):
                validated_data.pop(field_name)
        return super().update(instance, validated_data)


class ScheduleSerializer(serializers.ModelSerializer):
    room_number_inf = LocationSerializer(source='room_number', read_only=True)
    extra_kwargs = {
        'schedule_id': {'required': False},
        'room_number': {'required': False},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            for field_name in self.fields:
                if field_name != 'max_size':
                    self.fields[field_name].read_only = True

    def update(self, instance, validated_data):
        for field_name in list(validated_data.keys()):
            if field_name != 'max_size':
                validated_data.pop(field_name)
        return super().update(instance, validated_data)

    class Meta:
        model = Schedule
        fields = ['schedule_id', 'room_number', 'max_size', 'room_number_inf']



class ClassNameSerializer(serializers.ModelSerializer):
    schedule_info = ScheduleSerializer(source='schedule_id', read_only=True)

    class Meta:
        model = ClassName
        fields = ['class_id', 'class_name', 'teacher', 'schedule_id', 'max_size', 'start_date', 'end_date', 'status', 'schedule_info']
        extra_kwargs = {
            'class_id': {'required': False},
            'class_name': {'required': False},
            'teacher': {'required': False},
            'schedule_id': {'required': False},
            'start_date': {'required': False},
            'end_date': {'required': False},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            for field_name in self.fields:
                if field_name not in ('max_size', 'status'):
                    self.fields[field_name].read_only = True

    def update(self, instance, validated_data):
        for field_name in list(validated_data.keys()):
            if field_name not in ('max_size', 'status'):
                validated_data.pop(field_name)
        return super().update(instance, validated_data)

    def validate(self, data):
        if not self.instance or 'schedule_id' in data:
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
                    label='Schedule',
                    exclude_instance=self.instance
                )
            except DjangoValidationError as e:
                raise DRFValidationError({'schedule_id': e.messages})

        return data


class StudentClassSerializer(serializers.ModelSerializer):
    class_info = ClassNameSerializer(source='class_id', read_only=True)

    class Meta:
        model = StudentClass
        fields = [
            'student_id',
            'class_id',
            'registered_at',
            'learning_status',
            'class_info'
        ]

    def validate(self, data):
        class_instance = get_instance_by_id(ClassName, data.get('class_id'), 'class_id')
        student_instance = get_instance_by_id(Student, data.get('student_id'), 'student_id')
        print(f"{student_instance}")


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

        if student_instance.status != "studying":
            raise DRFValidationError({
                'student_id': [f"Student status must be 'studying'. Current status: '{student_instance.status}'."]
            })

        return data


class TeacherSerializer(ValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['teacher_id'].read_only = True

    def update(self, instance, validated_data):
        validated_data.pop('teacher_id', None)
        return super().update(instance, validated_data)

