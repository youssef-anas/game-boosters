from django.db import models

# Create your models here.
class Game(models.Model):
  name = models.CharField(max_length=100)
  link = models.CharField(max_length=100)

  logo_image = models.ImageField(upload_to='games/logos/', blank=True, null=True)
  banner_image = models.ImageField(upload_to='games/banners/', blank=True, null=True)
  name_image = models.ImageField(upload_to='games/names/', blank=True, null=True)

  def __str__(self):
    return self.name
  
  def get_logo_image_url(self):
    return self.logo_image.url
  
  def get_banner_image_url(self):
    return self.banner_image.url
  
  def get_name_image_url(self):
    return self.name_image.url