import re
from rest_framework import serializers

class StudentValidationMixin:
    # def validate_student_id(self, value):
    #     if not re.match(r'^PH\d{5}$', value):
    #         raise serializers.ValidationError('Student ID must start with "PH" followed by 5 digits (ex: PH12345)')
    #     return value

    def validate_name(self, value):
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError('Only letters (A–Z, a–z) and spaces are allowed.')
        return value

    def validate_age(self, value):
        if value < 10 or value > 100:
            raise serializers.ValidationError('Age must be between 10 and 100.')
        return value

    def validate_major(self, value):
        majors = [choice[0] for choice in self.Meta.model.MAJOR_CHOICES]
        if value not in majors:
            raise serializers.ValidationError(f'Major must be one of {majors}')
        return value

    def validate_gender(self, value):
        genders = [choice[0] for choice in self.Meta.model.GENDER_CHOICES]
        if value not in genders:
            raise serializers.ValidationError(f'Gender must be one of {genders}')
        return value

    def validate_email(self, value):
        if any(c.isupper() for c in value):
            raise serializers.ValidationError("Email must not contain uppercase letters.")

        if ' ' in value:
            raise serializers.ValidationError("Email must not contain spaces.")

        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Email must end with '@gmail.com'.")

        username = value.split('@')[0]

        if not re.fullmatch(r'[a-z0-9]+', username):
            raise serializers.ValidationError("Email must contain only lowercase letters and digits before '@'.")
        return value

    def validate_status(self, value):
        status = [choice[0] for choice in self.Meta.model.STATUS_CHOICES]
        if value not in status:
            raise serializers.ValidationError(f'Status must be one of {status}')
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
