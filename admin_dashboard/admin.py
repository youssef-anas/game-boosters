from django.contrib import admin
from .models import BoosterComment, BoosterCommission

@admin.register(BoosterComment)
class BoosterCommentAdmin(admin.ModelAdmin):
    list_display = ['booster', 'admin', 'comment', 'created_at']
    list_filter = ['created_at', 'admin']
    search_fields = ['booster__username', 'admin__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

@admin.register(BoosterCommission)
class BoosterCommissionAdmin(admin.ModelAdmin):
    list_display = ['booster', 'percentage', 'set_by', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'set_by']
    search_fields = ['booster__username', 'set_by__username', 'notes']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

