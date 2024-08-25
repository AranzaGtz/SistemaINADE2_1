import re
from rest_framework import serializers

def validate_id(instance, value):
    if instance and instance.id != value:
        raise serializers.ValidationError("ID cannot be changed.")
    return value

def validate_name(value):
    if not value.strip():
        raise serializers.ValidationError("The name cannot be empty.")
    if not re.match(r'^[a-zA-Z]', value):
        raise serializers.ValidationError("The name must start with a letter.")
    if len(value) > 64:
        raise serializers.ValidationError("The name must not exceed 64 characters.")
    return value

def validate_phone(value):
    clean_phone = ''.join(filter(str.isdigit, value))
    if not clean_phone.strip():
        raise serializers.ValidationError("The phone cannot be empty.")
    if len(clean_phone) > 20:
        raise serializers.ValidationError("The phone must not exceed 20 characters.")
    if len(clean_phone) < 10:
        raise serializers.ValidationError("The phone must have at least 10 characters.")
    return value