from django.db import models
from accounts.models import BaseUser
from django.utils import timezone

class AdminLogEntry(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    model = models.CharField(max_length=100, null=True, blank=True)
    details = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user} - {self.action} - {self.model} - {self.timestamp}'
