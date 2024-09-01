from rest_framework import serializers
from core.validations import (
    validate_text, validate_content, validate_phone,
)
from core.managers import BaseManager

class AddressManager(BaseManager):
    def validate_street(self, value):
        return validate_content(self.instance, value)
    
    def validate_city(self, value):
        return validate_text(self.instance, value)

    def validate_state(self, value):
        return validate_text(self.instance, value)
    
    # country, postal_code ... 


class OrganizationManager(BaseManager):
    def validate_name(self, value):
        return validate_text(self.instance, value)
    
    # logo

    def validate_slogan(self, value):
        return validate_content(self.instance, value)
    
    # rfc, website

    def validate_phone(self, value):
        return validate_phone(self.instance, value)


    
class QuotationManager(BaseManager):
    # folio, start_date, end_date
    pass
    
class WorkOrderManager(BaseManager):
    pass
    
class MethodManager(BaseManager):
    def validate_name(self, value):
        return validate_text(self.instance, value)
    
    def validate_description(self, value):
        return validate_content(self.instance, value)

class ServiceManager(BaseManager):
    def validate_name(self, value):
        return validate_text(self.instance, value)
    
    def validate_description(self, value):
        return validate_content(self.instance, value)
    
    # cost

class ConceptManager(BaseManager):
    pass
    
class ConfigurationManager(BaseManager):
    pass