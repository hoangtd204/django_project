from django.core.exceptions import ValidationError as DjangoValidationError

def validate_max_size(related_model, foreign_key_field, parent_instance, parent_max_size, label, exclude_instance=None):
    filter_kwargs = {foreign_key_field: parent_instance}
    qs = related_model.objects.filter(**filter_kwargs)

    if exclude_instance:
        qs = qs.exclude(pk=exclude_instance.pk)

    if qs.count() >= parent_max_size:
        raise DjangoValidationError(f"{label} is full (max size is {parent_max_size})")
