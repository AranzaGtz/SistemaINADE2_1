from rest_framework import serializers
from core.validations import (
    validate_id, validate_text, validate_phone,
    validate_content, validate_email, validate_choices
)
from .choices import (
    Priority, SampleType, FinalDisposition,
    StateOfMatter
)

class LaboratoryManager(serializers.ModelSerializer):
    def validate_id(self, value):
        return validate_id(self.instance, value)

    def validate_name(self, value):
        return validate_text(value)

    def validate_address(self, value):
        return validate_content(value)
    
    def validate_phone(self, value):
        return validate_phone(value)
    
    def validate_email(self, value):
        return validate_email(value)

class EquipmentManager(serializers.ModelSerializer):
    def validate_id(self, value):
        return validate_id(self.instance, value)

    def validate_name(self, value):
        return validate_text(value)
    
    def validate_description(self, value):
        return validate_content(value)
    
class SubEquipmentManager(serializers.ModelSerializer):
    def validate_id(self, value):
        return validate_id(self.instance, value)

    def validate_name(self, value):
        return validate_text(value)
    
    def validate_description(self, value):
        return validate_content(value)

class InternalCustodyManager(serializers.ModelSerializer):
    def validate_id(self, value):
        return validate_id(self.instance, value)

    def validate_priority(self, value):
        return validate_choices(Priority, value)
    
    def validate_sample_type(self, value):
        return validate_choices(SampleType, value)
    
    def validate_final_disposition(self, value):
        return validate_choices(FinalDisposition, value)

    def validate_observations(self, value):
        return validate_content(value)

class FilterMethodManager(serializers.ModelSerializer):
    def validate_id(self, value):
        return validate_id(self.instance, value)

    def validate_name(self, value):
        return validate_text(value)
    
    def validate_description(self, value):
        return validate_content(value)

class SampleManager(serializers.ModelSerializer):
    def validate_id(self, value):
        return validate_id(self.instance, value)

    def validate_state_of_matter(self, value):
        return validate_choices(StateOfMatter, value)
    
    # validate quantity, unit, num_containers ...