from django.contrib import admin
from .models import Laboratory, Equipment, SubEquipment, InternalCustody, FilterMethod, Sample
# Register your models here.

admin.site.register(Laboratory)
admin.site.register(Equipment)
admin.site.register(SubEquipment)
admin.site.register(InternalCustody)
admin.site.register(FilterMethod)
admin.site.register(Sample)