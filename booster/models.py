from django.db import models
from accounts.models import BaseUser, BaseOrder
from wildRift.models import WildRiftRank
from valorant.models import ValorantRank
from pubg.models import PubgRank
from leagueOfLegends.models import LeagueOfLegendsRank
from tft.models import TFTRank
from hearthstone.models import HearthstoneRank
from rocketLeague.models import RocketLeagueRank
from mobileLegends.models import MobileLegendsRank
from WorldOfWarcraft.models import WorldOfWarcraftRank
from overwatch2.models import Overwatch2Rank
from dota2.models import Dota2Rank
from csgo2.models import Csgo2Rank
from honorOfKings.models import HonorOfKingsRank
from games.models import Game
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

class OrderRating(models.Model):
    customer = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='ratings_given')
    booster = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='ratings_received', limit_choices_to={'is_booster': True})
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
    booster = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='booster', null=True,  limit_choices_to={'is_booster': True})
    profile_image_url = models.CharField(null=True, blank=True)
    profile_image = models.ImageField(blank= True,null=True,)
    about_you = models.TextField(max_length=1000,null=True, blank=True)
    can_choose_me = models.BooleanField(default=True ,blank=True)

    languages = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    games = models.ManyToManyField(Game, related_name='games')

    paypal_account = models.EmailField(max_length=254, null=True, unique=True, blank=False)

    discord_id = models.CharField(max_length=300, default="", blank=True, null=True)
    email_verified_at = models.DateTimeField(null=True,blank=True)

    is_wr_player = models.BooleanField(default=False)
    achived_rank_wr = models.ForeignKey(WildRiftRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='wr_rank')

    is_valo_player = models.BooleanField(default=False)
    achived_rank_valo = models.ForeignKey(ValorantRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='valo_rank')

    is_pubg_player = models.BooleanField(default=False)
    achived_rank_pubg = models.ForeignKey(PubgRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='pubg_rank')

    is_lol_player = models.BooleanField(default=False)
    achived_rank_lol = models.ForeignKey(LeagueOfLegendsRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='lol_rank')

    is_tft_player = models.BooleanField(default=False)
    achived_rank_tft = models.ForeignKey(TFTRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='tft_rank')

    is_wow_player = models.BooleanField(default=False)
    achived_rank_wow = models.ForeignKey(WorldOfWarcraftRank, on_delete = models.SET_NULL, null=True, blank=True, related_name='wow_rank')

    is_hearthstone_player = models.BooleanField(default=False)
    achived_rank_hearthstone = models.ForeignKey(HearthstoneRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='hearthstone_rank')

    is_mobleg_player = models.BooleanField(default=False)
    achived_rank_mobleg = models.ForeignKey(MobileLegendsRank, on_delete = models.SET_NULL, null=True, blank=True, related_name='mobleg_rank')

    is_rl_player = models.BooleanField(default=False)
    achived_rank_rl= models.ForeignKey(RocketLeagueRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='rl_rank')

    is_dota2_player = models.BooleanField(default=False)
    achived_rank_dota2 = models.ForeignKey(Dota2Rank, on_delete = models.SET_NULL, null=True, blank=True, related_name='dota2_rank')

    is_hok_player = models.BooleanField(default=False)
    achived_rank_hok = models.ForeignKey(HonorOfKingsRank, on_delete = models.SET_NULL, null=True, blank=True, related_name='hok_rank')

    is_overwatch2_player = models.BooleanField(default=False)
    achived_rank_overwatch2 = models.ForeignKey(Overwatch2Rank, on_delete = models.SET_NULL, null=True, blank=True, related_name='overwatch2_rank')

    is_csgo2_player = models.BooleanField(default=False)
    achived_rank_csgo2 = models.ForeignKey(Csgo2Rank, on_delete = models.SET_NULL, null=True, blank=True, related_name='csgo2_rank')
       
    
    def __str__(self):
        return f'{self.booster.username}'
    
    def get_languages_as_string(self):
        return ','.join(self.languages)

    def set_languages_from_list(self, text_list):
        self.languages = ','.join(text_list)
    
    def save(self, *args, **kwargs):
        # When saving a Booster instance, set is_booster to True for the associated BaseUser
        self.booster.is_booster = True
        self.profile_image = self.profile_image_url
        self.booster.save()
        super().save(*args, **kwargs)

    def get_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return None

    
class BoosterPortfolio(models.Model):
    booster         = models.ForeignKey(Booster, related_name='booster_portfolio', on_delete=models.CASCADE)
    image           = models.ImageField(upload_to='booster/images')

    def get_image_url(self):
        return f"/media/{self.image}"
    
    def __str__(self):
        return f'Portfolio of {self.booster.booster.username}'

class WorkWithUs(models.Model):
    nickname        = models.CharField(max_length=30)
    email           = models.EmailField()
    discord_id      = models.CharField(max_length=100)
    languages       = models.CharField(max_length=300)
    game            = models.ManyToManyField(Game)
    rank            = models.CharField(max_length=300)
    server          = models.CharField(max_length=100)

    def __str__(self):
        return self.nickname


class Photo(models.Model):
    booster         = models.ForeignKey(WorkWithUs, related_name='photos', on_delete=models.CASCADE)
    image           = models.ImageField(upload_to='booster/images')