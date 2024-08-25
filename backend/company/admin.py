from django.contrib import admin
from .models import Address, Organization, Configuration
# Register your models here.

admin.site.register(Address)
admin.site.register(Organization)
admin.site.register(Configuration)