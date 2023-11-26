from django.db import models
from accounts.models import BaseUser
# Create your models here.
class BoosterRequest(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    desired_rank = models.CharField(max_length=100)  # You may want to use a more appropriate field for ranks
    additional_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Booster Request"