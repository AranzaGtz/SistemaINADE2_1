from rest_framework import serializers
from core.validations import *

class OrganizationManager(serializers.ModelSerializer):
    def validate_id(self, value):
        return validate_id(self.instance, value)

class AddressManager(serializers.ModelSerializer):
    def validate_id(self, value):
        return validate_id(self.instance, value)