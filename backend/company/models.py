from django.db import models
from core.utils import generate_short_uuid
from django.utils import timezone
from .choices import Currency, VAT

# Create your models here.
class Address(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    street = models.CharField(max_length=128, null=False, blank=False)
    city = models.CharField(max_length=64, null=False, blank=False)
    state = models.CharField(max_length=64, null=False, blank=False)
    country = models.CharField(max_length=64, null=False, blank=False)
    postal_code = models.CharField(max_length=16, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def get_direction(self):
        return f"{self.street}, {self.postal_code}, {self.city}, {self.state}, {self.country}"

    def __str__(self):
        return self.get_direction()

class Organization(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    name = models.CharField(max_length=64, null=False, blank=False)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    slogan = models.CharField(max_length=128, null=True, blank=True)
    rfc = models.CharField(max_length=16, null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Quotation(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    folio = models.CharField(max_length=16, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.folio:
            self.folio = str(self.id)
        if not self.start_date:
            self.start_date = self.created_at
        if not self.end_date:
            self.end_date = self.start_date + timezone.timedelta(days=1)
        super(Quotation, self).save(*args, **kwargs)

    def __str__(self):
        return self.organization.name

class WorkOrder(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='work_order')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Work Order from {self.quotation.folio}"

class Method(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    name = models.CharField(max_length=64, unique=True, null=False, blank=False)
    description = models.CharField(max_length=128, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    name = models.CharField(max_length=64, null=False, blank=False)
    description = models.CharField(max_length=128, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='quotations')
    method = models.OneToOneField(Method, on_delete=models.CASCADE, related_name='service')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __save__(self, *args, **kwargs):
        if not self.cost:
            self.cost = 500.00
        super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Concept(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='quotation_services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='quotation_services')
    overridden_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.overridden_cost:
            self.overridden_cost = self.service.cost
        super(Concept, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.service.name} in {self.quotation.folio}"


class Configuration(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, related_name='configuration')
    currency = models.CharField(max_length=4, choices=Currency.choices, default=Currency.MXN)
    vat = models.CharField(max_length=4, choices=VAT.choices, default=VAT.EIGHT_PERCENT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organization.name