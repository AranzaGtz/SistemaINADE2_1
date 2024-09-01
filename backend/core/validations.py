import re
from django.core.validators import validate_email as django_validate_email
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
import django.utils.timezone as timezone

# Reusable validation functions

def validate_id(instance, value):
    if instance and instance.id != value:
        raise serializers.ValidationError("ID cannot be changed.")
    return value

def validate_text(value):
    value = value.strip()
    if not value:
        raise serializers.ValidationError("The text cannot be empty.")
    if not re.match(r'^[a-zA-Z]', value):
        raise serializers.ValidationError("The text must start with a letter.")
    if len(value) > 64:
        raise serializers.ValidationError("The text must not exceed 64 characters.")
    return value

def validate_content(value):
    value = value.strip()
    if not value:
        raise serializers.ValidationError("The content cannot be empty.")
    if len(value) > 128:
        raise serializers.ValidationError("The content must not exceed 128 characters.")
    return value

def validate_boolean(value):
    if not isinstance(value, bool):
        raise serializers.ValidationError("The value must be a boolean.")
    return value

def validate_phone(value):
    clean_phone = ''.join(filter(str.isdigit, value))
    if not clean_phone:
        raise serializers.ValidationError("The phone cannot be empty.")
    if len(clean_phone) > 20:
        raise serializers.ValidationError("The phone must not exceed 20 characters.")
    if len(clean_phone) < 10:
        raise serializers.ValidationError("The phone must have at least 10 characters.")
    return value

def validate_email(value):
    try:
        django_validate_email(value)
    except DjangoValidationError:
        raise serializers.ValidationError("Invalid email address.")
    return value

def validate_choices(model, value):
    if not model.objects.filter(id=value).exists():
        raise serializers.ValidationError(f"Invalid choice: {value} is not a valid option.")
    return value

def validate_price(value):
    if value < 0:
        raise serializers.ValidationError("Price cannot be negative.")
    if value > 100000.00:
        raise serializers.ValidationError("Price cannot exceed 100,000.00.")
    return value

def validate_rfc(value):
    '''rfc_pattern = r'^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$'
    if not re.match(rfc_pattern, value):
        raise serializers.ValidationError("Invalid RFC format.")'''
    return value

# Additional useful validators

def validate_positive_integer(value):
    if value <= 0:
        raise serializers.ValidationError("The value must be a positive integer.")
    return value

def validate_non_empty_list(value):
    if not isinstance(value, list) or not value:
        raise serializers.ValidationError("This field must be a non-empty list.")
    return value

def validate_date_not_in_future(value):
    if value > timezone.now().date():
        raise serializers.ValidationError("The date cannot be in the future.")
    return value
