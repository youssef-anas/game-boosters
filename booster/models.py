from django.db import models
from accounts.models import BaseUser, BaseOrder
from wildRift.models import WildRiftDivisionOrder, WildRiftRank
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class Rating(models.Model):
    customer = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='ratings_given')
    booster = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='ratings_received')
    rate = models.IntegerField(default=0)
    text = models.TextField(null=True, max_length=500)
    game = models.IntegerField(default=1)
    anonymous = models.BooleanField(default=False)
    order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, related_name='order_rated')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Set customer and booster based on the associated order
        self.customer = self.order.customer
        self.booster = self.order.booster

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer.username} rated {self.booster.username} with {self.rate}'
    

class Booster(models.Model):
    booster = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='user', null=True)
    image = models.ImageField(null=True,upload_to='media/booster/', blank= True)
    about_you = models.TextField(max_length=1000,null=True, blank=True)
    can_choose_me = models.BooleanField(default=True ,blank=True)
    email_verified_at = models.DateTimeField(null=True,blank=True)
    is_wf_player = models.BooleanField(default=False)
    is_valo_player = models.BooleanField(default=False)
    achived_rank_wr = models.ForeignKey(WildRiftRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='wr_rank')
    achived_rank_valo = models.ForeignKey(WildRiftRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='valo_rank')


    def __str__(self):
        return f'{self.booster.username}'
    
    def save(self, *args, **kwargs):
        # When saving a Booster instance, set is_booster to True for the associated BaseUser
        self.booster.is_booster = True
        self.booster.save()
        super().save(*args, **kwargs)


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
    ]
    STATUS = [
        (0, "Drop"),
        (1, "Done")
    ]
    user = models.ForeignKey(Booster, on_delete=models.CASCADE)
    amount = models.FloatField(default=0, validators=[MinValueValidator(0)])
    order = models.ForeignKey(BaseOrder, on_delete=models.CASCADE, related_name='from_order')
    notice = models.TextField(default='There is no any notice')
    status = models.IntegerField(choices=STATUS, default=1)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)

    def __str__(self):
        return f'{self.user.username} {self.type} {self.amount}$'