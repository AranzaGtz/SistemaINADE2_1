from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, Profile
from .choices import Role
from company.models import Organization, Address

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
@receiver(pre_save, sender=User)
def ensure_organization_exists(sender, instance, **kwargs):
    if instance.role == Role.CUSTOMER and not instance.organization:
        address = Address.objects.create(
            street="Street",
            city="City",
            state="State",
            country="Country",
            postal_code="00000"
        )
        organization = Organization.objects.create(
            name=f"{instance.first_name}'s Organization",
            logo=None,
            slogan="Your slogan",
            rfc="Your RFC",
            address=address,
            website="http://default.org",
            phone="0000000000"
        )
        instance.organization = organization