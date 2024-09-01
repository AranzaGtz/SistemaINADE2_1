from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Organization, Configuration, Quotation, WorkOrder

@receiver(post_save, sender=Organization)
def create_organization_configuration(sender, instance, created, **kwargs):
    if created:
        Configuration.objects.create(organization=instance)