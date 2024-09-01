from django.contrib import admin
from .models import Address, Organization, Configuration, Quotation, WorkOrder, Method, Service, Concept

# Register your models here.
    
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'state', 'country', 'postal_code')
    search_fields = ('street', 'city', 'state', 'country')
    list_filter = ('city', 'state', 'country')

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'rfc', 'website', 'phone', 'created_at')
    search_fields = ('name', 'rfc')
    list_filter = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'logo', 'slogan', 'rfc', 'address', 'website', 'phone')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created_at',),
        }),
    )
    readonly_fields = ('created_at',)

class QuotationInline(admin.TabularInline):
    model = Quotation
    extra = 1

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('folio', 'organization', 'start_date', 'end_date', 'is_accepted', 'created_at')
    search_fields = ('folio', 'organization__name')
    list_filter = ('is_accepted', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('folio', 'organization', 'start_date', 'end_date', 'is_accepted')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created_at', 'is_active'),
        }),
    )

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'quotation', 'created_at', 'is_active')
    search_fields = ('quotation__folio',)
    list_filter = ('is_active', 'created_at')

@admin.register(Method)
class MethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'cost', 'organization', 'method', 'created_at', 'is_active')
    search_fields = ('name', 'organization__name', 'method__name')
    list_filter = ('organization', 'method', 'is_active', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'cost', 'organization', 'method')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created_at', 'is_active'),
        }),
    )

@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = ('id', 'quotation', 'service', 'overridden_cost')
    search_fields = ('quotation__folio', 'service__name')
    list_filter = ('quotation', 'service')

@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('organization', 'currency', 'vat')
    search_fields = ('organization__name',)
    list_filter = ('currency', 'vat')
    fieldsets = (
        (None, {
            'fields': ('organization', 'currency', 'vat')
        }),
    )
