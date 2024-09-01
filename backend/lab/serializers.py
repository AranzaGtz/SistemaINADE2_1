from .models import (
    Laboratory, Equipment, SubEquipment, 
    InternalCustody, FilterMethod, Sample
)
from .managers import (
    LaboratoryManager, EquipmentManager, SubEquipmentManager,
    InternalCustodyManager, FilterMethodManager, SampleManager
)

class LaboratoryListSerializer(LaboratoryManager):
    class Meta:
        model = Laboratory
        fields = ['id', 'name', 'address']

class LaboratoryDetailSerializer(LaboratoryManager):
    class Meta:
        model = Laboratory
        fields = '__all__'

class EquipmentListSerializer(EquipmentManager):
    class Meta:
        model = Equipment
        fields = ['id', 'name']
    
class EquipmentDetailSerializer(EquipmentManager):
    class Meta:
        model = Equipment
        fields = '__all__'

class SubEquipmentListSerializer(SubEquipmentManager):
    class Meta:
        model = SubEquipment
        fields = ['id', 'name']
    
class SubEquipmentDetailSerializer(SubEquipmentManager):
    class Meta:
        model = SubEquipment
        fields = '__all__'
    
class InternalCustodyListSerializer(InternalCustodyManager):
    class Meta:
        model = InternalCustody
        fields = ['id', 'priority']

class InternalCustodyDetailSerializer(InternalCustodyManager):
    class Meta:
        model = InternalCustody
        fields = '__all__'

class FilterMethodListSerializer(FilterMethodManager):
    class Meta:
        model = FilterMethod
        fields = ['id', 'name']

class FilterMethodDetailSerializer(FilterMethodManager):
    class Meta:
        model = FilterMethod
        fields = '__all__'

class SampleListSerializer(SampleManager):
    class Meta:
        model = Sample
        fields = ['id', 'state_of_matter', 'filter_method']

class SampleDetailSerializer(SampleManager):
    class Meta:
        model = Sample
        fields = '__all__'