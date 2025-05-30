from django.core.exceptions import ValidationError as DjangoValidationError

def validate_max_size(related_model, foreign_key_field, parent_instance, parent_max_size, label):

    filter_kwargs = {foreign_key_field: parent_instance}
    count = related_model.objects.filter(**filter_kwargs).count()

    if count >= parent_max_size:
        raise DjangoValidationError(f"{label} is full (max size is {parent_max_size})")
