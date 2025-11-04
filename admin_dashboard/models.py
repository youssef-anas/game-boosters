from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import BaseUser

User = get_user_model()

class BoosterComment(models.Model):
    """Model to store admin comments for boosters"""
    booster = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='admin_comments', limit_choices_to={'is_booster': True})
    admin = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='comments_made', limit_choices_to={'is_staff': True})
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.admin.username} for {self.booster.username}"

class BoosterCommission(models.Model):
    """Model to store booster commission rates"""
    booster = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='commission_rates', limit_choices_to={'is_booster': True})
    percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Commission percentage (0-100)")
    notes = models.TextField(blank=True, null=True)
    set_by = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='commissions_set', limit_choices_to={'is_staff': True})
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.booster.username} - {self.percentage}% commission"

class ManagerComment(models.Model):
    """Model to store admin comments for managers (staff users)"""
    manager = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='manager_admin_comments', limit_choices_to={'is_staff': True})
    admin = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='manager_comments_made', limit_choices_to={'is_staff': True})
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.admin.username} for manager {self.manager.username}"

class PricingEntry(models.Model):
    game_key = models.CharField(max_length=64, db_index=True)
    service_id = models.IntegerField()
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=255, blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("game_key", "service_id")
        indexes = [
            models.Index(fields=["game_key", "service_id"]),
        ]

    def __str__(self) -> str:
        return f"{self.game_key} - Service {self.service_id}: {self.price}"

