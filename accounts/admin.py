from django.contrib import admin
from django.contrib.admin.models import LogEntry
# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import BaseUser, BaseOrder, Wallet, Transaction, BoosterPercent, TokenForPay, Tip_data, PromoCode
from chat.models import  Room, Message
from accounts.models import Captcha
from django.utils.html import format_html

class AdminLog(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(LogEntry, AdminLog)


admin.site.register(Captcha)
class CustomUserAdmin(UserAdmin):
    # Customize the display fields for the user model
    list_display = ('username', 'email', 'is_active','is_booster','is_customer')
    search_fields = ('email', 'username',)
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password','is_online','last_online')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'country', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','is_booster','is_customer','is_admin')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'rest_password_code', 'activation_code')}),
    )
    # readonly_fields = ('show_history',)  # Make the history field read-only

    # def show_history(self, obj):
    #     return self.get_history(obj)
    
    # show_history.short_description = 'History'

admin.site.register(BaseUser ,CustomUserAdmin)
# admin.site.register(BaseOrder)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(BoosterPercent)
admin.site.register(TokenForPay)
admin.site.register(Tip_data)
admin.site.register(PromoCode)


class HasBoosterFilter(admin.SimpleListFilter):
    title = 'Has Booster'
    parameter_name = 'has_booster'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(booster__isnull=True)
        elif self.value() == 'no':
            return queryset.filter(booster__isnull=True)

@admin.register(BaseOrder)
class BaseOrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'status','details','booster', 'chat_link','finish_image_url']
    list_filter = ['game','is_done',"approved", HasBoosterFilter]
    search_fields = ['name', 'customer__username', 'booster__username']
    fieldsets = (
        ('Admin Info', {'fields': ('name','details','finish_image','approved')}),
        ('Order Info', {'fields': ('customer','booster','is_done')}),
        ('Order Price', {'fields': ('price', 'actual_price','money_owed')}),
        ('Extra Options', {'fields': ('duo_boosting', 'select_booster','turbo_boost','streaming','promo_code', 'captcha')}),
    )


    def finish_image_url(self, obj):
        if obj.finish_image:
            return format_html('<a href="{}" target="_blank">Finish Img</a>', obj.finish_image.url)
        return None

    finish_image_url.short_description = 'Image'


    def chat_link(self, obj):
        if not obj.is_drop:
            chat_url = f'/dashboard/chat/{obj.name}/'
            return format_html('<a href="{}" target="_blank">Open Chat</a>', chat_url)
        return None

    chat_link.short_description = 'Chat'