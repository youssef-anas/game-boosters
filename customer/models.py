from django.db import models
from games.models import Game
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