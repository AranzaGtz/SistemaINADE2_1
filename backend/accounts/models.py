from django.db import models
from core.utils import generate_short_uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from .choices import Country, Role, Priority, Gender
from company.models import Organization
from datetime import date

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    email = models.EmailField(unique=True, max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    role = models.CharField(choices=Role.choices, default=Role.CUSTOMER, max_length=16)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email
    
class Title(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    name = models.CharField(max_length=64, null=False, blank=False)
    abbreviation = models.CharField(max_length=4, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Profile(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    gender = models.CharField(choices=Gender.choices, default=Gender.MALE, max_length=16, null=True, blank=True)
    date_of_birth = models.DateField(_("Date of Birth"), null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(choices=Country.choices, default=Country.MX, max_length=20, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def age(self):
        today = date.today()
        if self.date_of_birth:
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            return age
        return None

    def __str__(self):
        return self.user.email

class Support(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    subject = models.CharField(max_length=64, null=False, blank=False)
    message = models.CharField(max_length=128, null=True, blank=True)
    screenshot = models.ImageField(upload_to='support/', null=True, blank=True)
    priority = models.CharField(choices=Priority.choices, default=Priority.LOW, max_length=8)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support')
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} by {self.user.get_full_name()}"

class SupportResponse(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    message = models.CharField(max_length=128, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_response')
    support = models.ForeignKey(Support, on_delete=models.CASCADE, related_name='support_responses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

