from django.contrib import admin
from .models import (
    Laboratory, Equipment, SubEquipment, InternalCustody, FilterMethod, Sample
)

@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'address', 'phone', 'email', 'created_at', 'is_active')
    search_fields = ('name', 'organization__name', 'address', 'phone', 'email')
    list_filter = ('organization', 'is_active', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'organization', 'address', 'phone', 'email', 'is_active')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('id', 'created_at'),
        }),
    )
    readonly_fields = ('id', 'created_at',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'name', 'laboratory', 'created_at', 'is_active')
    search_fields = ('serial_number', 'name', 'laboratory__name')
    list_filter = ('laboratory', 'is_active', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('serial_number', 'name', 'description', 'laboratory', 'is_active')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('id', 'created_at'),
        }),
    )

@admin.register(SubEquipment)
class SubEquipmentAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'name', 'equipment', 'created_at', 'is_active')
    search_fields = ('serial_number', 'name', 'equipment__name')
    list_filter = ('equipment', 'is_active', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('serial_number', 'name', 'description', 'equipment', 'is_active')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('id', 'created_at'),
        }),
    )

@admin.register(InternalCustody)
class InternalCustodyAdmin(admin.ModelAdmin):
    list_display = ('id', 'priority', 'sample_type', 'final_disposition', 'work_order', 'created_at')
    search_fields = ('id', 'work_order__quotation__folio')
    list_filter = ('priority', 'sample_type', 'final_disposition', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('priority', 'sample_type', 'final_disposition', 'observations', 'work_order')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('id', 'created_at'),
        }),
    )

@admin.register(FilterMethod)
class FilterMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('id', 'created_at'),
        }),
    )

@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ('id', 'sampling_datetime', 'state_of_matter', 'quantity', 'unit', 'num_containers', 'internal_custody', 'filter_method', 'created_at')
    search_fields = ('id', 'internal_custody__id', 'filter_method__name')
    list_filter = ('state_of_matter', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('sampling_datetime', 'state_of_matter', 'quantity', 'unit', 'num_containers', 'internal_custody', 'filter_method')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('id', 'created_at'),
        }),
    )