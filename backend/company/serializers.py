from .models import Organization, Address
from .managers import OrganizationManager, AddressManager

class AddressListSerializer(AddressManager):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'country']

class AddressDetailSerializer(AddressManager):
    class Meta:
        model = Address
        fields = '__all__'

class OrganizationListSerializer(OrganizationManager):
    address = AddressListSerializer(read_only=True)
    class Meta:
        model = Organization
        fields = ['id', 'name', 'address']

class OrganizationDetailSerializer(OrganizationManager):
    class Meta:
        model = Organization
        fields = '__all__'