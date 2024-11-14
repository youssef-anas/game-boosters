from django.contrib import admin
from django.contrib.admin.models import LogEntry
# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import BaseUser, BaseOrder, Wallet, Transaction, BoosterPercent, TokenForPay, Tip_data, PromoCode
from chat.models import  Room, Message
from accounts.models import Captcha
from django.utils.html import format_html


class NoDeleteAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False    
    
class NoDeleteEditAdmin(NoDeleteAdmin):
    def has_change_permission(self, request, obj=None):
        return False

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
    def has_delete_permission(self, request, obj=None):
            return False

admin.site.register(BaseUser ,CustomUserAdmin)    

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

class BaseOrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'status','details','booster', 'chat_link','finish_image_url']
    list_filter = ['game','is_done',"approved", HasBoosterFilter]
    readonly_fields = ['created_at']  
    search_fields = ['name', 'customer__username', 'booster__username']
    fieldsets = (
        ('Admin Info', {'fields': ('name','details','finish_image','approved', 'created_at')}),
        ('Order Info', {'fields': ('customer','booster','is_done')}),
        ('Order Price', {'fields': ('price', 'actual_price','money_owed','real_order_price')}),
        ('Extra Options', {'fields': ('duo_boosting', 'select_booster','turbo_boost','streaming','promo_code', 'captcha')}),
        ('Customer_info', {'fields': ('customer_gamename', 'customer_username','customer_server', 'customer_password')}),
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

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(BaseOrder, BaseOrderAdmin)


class TransactionAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            wallet, created = Wallet.objects.get_or_create(user=obj.user)
            money = wallet.money
            wallet.money = money + obj.amount
            wallet.save()
        super().save_model(request, obj, form, change)


# No edit No delete
# admin.site.register(Room, NoDeleteEditAdmin)
# admin.site.register(Message, NoDeleteEditAdmin)
# admin.site.register(Captcha, NoDeleteEditAdmin)
admin.site.register(TokenForPay)
admin.site.register(LogEntry, NoDeleteEditAdmin)
admin.site.register(Wallet, NoDeleteEditAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Tip_data, NoDeleteEditAdmin)

# No delete
admin.site.register(BoosterPercent, NoDeleteAdmin)
admin.site.register(PromoCode, NoDeleteAdmin)