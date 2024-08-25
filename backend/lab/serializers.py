from .models import Laboratory, SubEquipment, Equipment
from .managers import LaboratoryManager, EquipmentManager, SubEquipmentManager

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