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

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}, {self.postal_code}"

class Organization(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    name = models.CharField(max_length=64, null=False, blank=False)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    slogan = models.CharField(max_length=128, null=True, blank=True)
    rfc = models.CharField(max_length=16, null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Quotation(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    folio = models.CharField(max_length=16, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='quotations')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

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

class Service(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)

class Configuration(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, related_name='configuration')
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.MXN)
    vat = models.CharField(max_length=4, choices=VAT.choices, default=VAT.EIGHT_PERCENT)

    def __str__(self):
        return self.organization.name

class WorkOrder(models.Model):
    pass
