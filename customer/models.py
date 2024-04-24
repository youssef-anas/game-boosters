from django.db import models
from games.models import Game
from accounts.models import BaseUser
# Create your models here.

class Champion(models.Model):
    name = models.CharField(max_length=50)
    game = models.ForeignKey(Game, related_name='champions',on_delete=models.PROTECT)
    image = models.ImageField(upload_to=f'{game.name}/champions') 

    class Meta:
        unique_together = [['name', 'game']]

    def __str__(self) -> str:
        return f'{self.name} for {self.game.name}'
    
    def get_image_url(self):
        return f"{self.image.url}"
    
class CustomOrder(models.Model):
    customer = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='order_customer')
    email = models.EmailField(blank=True)
    game = models.ForeignKey(Game, related_name='custom_order',on_delete=models.PROTECT)
    order = models.TextField()

    def __str__(self) -> str:
        return f'{self.order} for {self.customer.username}'