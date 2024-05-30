from django.db import models

class Blog(models.Model):
    main_image      = models.ImageField(upload_to='blog/')
    main_image2      = models.ImageField(upload_to='blog/')
    header          = models.CharField(max_length=130)
    youtube_link    = models.URLField(max_length=255)

    order_image     = models.ImageField(upload_to='blog/')
    order_image2    = models.ImageField(upload_to='blog/')
    order_name      = models.CharField(max_length=255)
    order_link      = models.CharField(max_length=255)

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk}'
    
    def get_main_image(self):
        if self.main_image:
            return self.main_image.url
        
    def get_main_image2(self):
        if self.main_image2:
            return self.main_image2.url

    def get_order_image(self):
        if self.order_image:
            return self.order_image.url

    def get_order_image2(self):
        if self.order_image2:
            return self.order_image2.url        
            


class SubHeader(models.Model):
    sub_header      = models.CharField(max_length=350)
    is_top          = models.BooleanField(default=True)
    blog            = models.ForeignKey(Blog, related_name='blog', on_delete=models.CASCADE, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)