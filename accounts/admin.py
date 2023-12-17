from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import BaseUser, Wallet

class CustomUserAdmin(UserAdmin):
    # Customize the display fields for the user model
    list_display = ('username', 'email', 'is_staff', 'is_booster', 'is_active', 'achived_rank')
    search_fields = ('email', 'username',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'achived_rank')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email_verified_at', "image", 'country', 'about_you', 'can_choose_me')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_booster', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(BaseUser ,CustomUserAdmin)
admin.site.register(Wallet)