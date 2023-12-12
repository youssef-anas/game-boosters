from django.db import models
from accounts.models import BaseUser
from wildRift.models import WildRiftDivisionOrder

class Rating(models.Model):
    customer = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='ratings_given')
    booster = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='ratings_received')
    rate = models.IntegerField(default=0)
    text = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    game = models.IntegerField(default=1)
    anonymous = models.BooleanField(default=False)
    order = models.OneToOneField(WildRiftDivisionOrder, on_delete=models.CASCADE, related_name='order_rated')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Set customer and booster based on the associated order
        self.customer = self.order.customer
        self.booster = self.order.booster

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer.username} rated {self.booster.username} with {self.rate}'