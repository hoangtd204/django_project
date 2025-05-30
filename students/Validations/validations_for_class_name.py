from django.core.exceptions import ValidationError
from students.models import Schedule


def validate_class_max_size(schedule_id, class_max_size):
    try:
        schedule = Schedule.objects.get(schedule_id=schedule_id)
    except Schedule.DoesNotExist:
        raise ValidationError(f"Schedule with id {schedule_id} does not exist.")

    if class_max_size >= schedule.max_size:
        raise ValidationError(
            f"Class max_size ({class_max_size}) cannot exceed Schedule max_size ({schedule.max_size}).")

