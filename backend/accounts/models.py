from django.db import models
from core.utils import generate_short_uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from .choices import Country, Role
from company.models import Organization
from datetime import date

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    email = models.EmailField(_("Email Address"), unique=True, max_length=64)
    first_name = models.CharField(_("First Name"), max_length=64)
    last_name = models.CharField(_("Last Name"), max_length=64, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    role = models.CharField(choices=Role.choices, default=Role.CUSTOMER, max_length=16)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name']

    objects = CustomUserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    id = models.CharField(primary_key=True, default=generate_short_uuid, max_length=8, editable=False, unique=True)
    date_of_birth = models.DateField(_("Date of Birth"), null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(choices=Country.choices, default=Country.MX, max_length=20, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_active = models.BooleanField(default=True)

    def calculate_age(self):
        today = date.today()
        if self.date_of_birth:
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            return age
        return None

    def __str__(self):
        return self.user.email