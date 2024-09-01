from .models import (
    Organization, Address, Quotation, 
    WorkOrder, Method, Service,
    Concept, Configuration
)
from .managers import (
    OrganizationManager, AddressManager, QuotationManager,
    WorkOrderManager, MethodManager, ServiceManager, 
    ConceptManager, ConfigurationManager
)

class AddressListSerializer(AddressManager):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'country']

class AddressDetailSerializer(AddressManager):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class OrganizationListSerializer(OrganizationManager):
    address = AddressListSerializer(read_only=True)
    class Meta:
        model = Organization
        fields = ['id', 'name', 'address']

class OrganizationDetailSerializer(OrganizationManager):
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ['is_active', 'created_at', 'updated_at']

class QuotationListSerializer(QuotationManager):
    class Meta:
        model = Quotation
        fields = ['id', 'folio']

class QuotationDetailSerializer(QuotationManager):
    class Meta:
        model = Quotation
        fields = '__all__'
        read_only_fields = ['is_active', 'created_at', 'updated_at']