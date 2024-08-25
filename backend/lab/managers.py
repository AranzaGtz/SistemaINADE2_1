from rest_framework import serializers
from core.validations import *

class LaboratoryManager(serializers.ModelSerializer):
    def validate_id(self, value):
        return validate_id(self.instance, value)

    def validate_name(self, value):
        return validate_name(value)
    
    def validate_phone(self, value):
        return validate_phone(value)

class EquipmentManager(serializers.ModelSerializer):
    def validate_id(self, value):
        return validate_id(self.instance, value)

    def validate_name(self, value):
        return validate_name(value)
    
class SubEquipmentManager(serializers.ModelSerializer):
    def validate_id(self, value):
        return validate_id(self.instance, value)

    def validate_name(self, value):
        return validate_name(value)