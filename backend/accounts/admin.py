from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    User, Profile, Support, SupportResponse
)

# Register your models here.
class UserAdminCustom(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "organization",
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {"classes": ("wide",), "fields": ("email", "first_name", "last_name", "password1", "password2"),},
        ),
    )
    list_display = ("email", "first_name", "last_name", "role", "organization")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    readonly_fields = ['date_joined', 'last_login']

admin.site.register(User, UserAdminCustom)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'date_of_birth', 'phone', 'country', 'is_active')
    search_fields = ('user__email', 'phone', 'country')
    list_filter = ('gender', 'country', 'is_active')
    readonly_fields = ('id',)
    fieldsets = (
        (None, {
            'fields': ('user', 'gender', 'date_of_birth', 'phone', 'address', 'country', 'is_active')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('id',),
        }),
    )

class SupportResponseInline(admin.StackedInline):
    model = SupportResponse
    extra = 1

@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'priority', 'is_resolved', 'created_at', 'updated_at')
    search_fields = ('subject', 'user__email', 'message')
    list_filter = ('priority', 'is_resolved', 'created_at', 'updated_at')
    inlines = [SupportResponseInline]
    fieldsets = (
        (None, {
            'fields': ('subject', 'message', 'screenshot', 'priority', 'user', 'is_resolved')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('id',),
        }),
    )

@admin.register(SupportResponse)
class SupportResponseAdmin(admin.ModelAdmin):
    list_display = ('support', 'user', 'message', 'created_at', 'updated_at')
    search_fields = ('support__subject', 'user__email', 'message')
    list_filter = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('support', 'user', 'message')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('id',),
        }),
    )