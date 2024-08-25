from django.db import models
from core.utils import generate_short_uuid
from .choices import (
    Priority, FinalDisposition, SampleType, StateOfMatter
)
from company.models import Organization, WorkOrder

# Create your models here.
class Laboratory(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    name = models.CharField(max_length=64, null=False, blank=False)
    address = models.CharField(max_length=128, null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='laboratories')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.address:
            self.address = self.organization.address
        if not self.phone:
            self.phone = self.organization.phone
        super(Laboratory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Equipment(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    serial_number = models.CharField(max_length=64, unique=True, null=False, blank=False)
    name = models.CharField(max_length=64, null=False, blank=False)
    description = models.CharField(max_length=128, null=True, blank=True)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name='equipments')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class SubEquipment(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    serial_number = models.CharField(max_length=64, unique=True, null=False, blank=False)
    name = models.CharField(max_length=64, null=False, blank=False)
    description = models.CharField(max_length=128, null=True, blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='sub_equipments')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class InternalCustody(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    priority = models.CharField(choices=Priority.choices, default=Priority.A, max_length=25)
    sample_type = models.CharField(choices=SampleType.choices, default=SampleType.COMPOSITION, max_length=15)
    final_disposition = models.CharField(choices=FinalDisposition.choices, default=FinalDisposition.RETURN_TO_CLIENT, max_length=20)
    observations = models.CharField(max_length=128, null=True, blank=True)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='internal_custody')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

class FilterMethod(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    name = models.CharField(max_length=64, null=False, blank=False)
    description = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Sample(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    sampling_datetime = models.DateTimeField(null=True, blank=True)
    state_of_matter = models.CharField(choices=StateOfMatter.choices, default=StateOfMatter.SOLID, max_length=7)
    quantity = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=4)
    num_containers = models.IntegerField(null=True, blank=True)
    internal_custody = models.ForeignKey(InternalCustody, on_delete=models.CASCADE, related_name='samples')
    filter_method = models.OneToOneField(FilterMethod, on_delete=models.CASCADE, related_name='sample', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.sampling_datetime:
            self.sampling_datetime = self.internal_custody.created_at
        if self.state_of_matter == StateOfMatter.SOLID:
            self.unit = 'kg'
        elif self.state_of_matter == StateOfMatter.LIQUID:
            self.unit = 'l'
        super(Sample, self).save(*args, **kwargs)

    def __str__(self):
        return self.id