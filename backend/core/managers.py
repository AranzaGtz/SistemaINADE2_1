from rest_framework import serializers
from .validations import validate_id

class BaseManager(serializers.ModelSerializer):
    def validate_id(self, value):
        return validate_id(self.instance, value)