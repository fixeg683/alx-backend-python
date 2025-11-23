from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Use the actual fields on CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'get_phone_number', 'get_role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    # Add custom fields to fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('phone_number', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('phone_number', 'role')}),
    )

    # Methods to display custom fields in list_display
    def get_phone_number(self, obj):
        return obj.phone_number
    get_phone_number.short_description = 'Phone Number'

    def get_role(self, obj):
        return obj.role
    get_role.short_description = 'Role'
