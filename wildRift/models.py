from django.db import models

# # Create your models here.

# class Wild_rift_rc(models.Model):
#     # rc = rank_price
#     iron_rc = models.FloatField(default=2.54)
#     bronze_rc = models.FloatField(default=4.15)
#     silver_rc = models.FloatField(default=5.80)
#     gold_rc = models.FloatField(default=9.06)
#     gold_rc_from_II_to_I = models.FloatField(default=12.95)
#     gold_rc_from_I_to_platinum = models.FloatField()
#     platinum_rc = models.FloatField(default=12.95)
#     platinum_rc_from_I_to_emerald = models.FloatField(default=19.42)
#     emerald_rc = models.FloatField(default=27.78)
#     diamond_rc_from_IV_to_III = models.FloatField(default=48.12)
#     diamond_rc_from_III_to_II = models.FloatField(default=53.45)
#     diamond_rc_from_II_to_I = models.FloatField(default=76.80)
#     diamond_rc_from_I_to_master = models.FloatField(default=85.32)

#     def save(self, *args, **kwargs):
#         self.Gold_rc_from_I_to_Platinum = self.Gold_rc_from_II_to_I
#         super().save(*args, **kwargs)


# class Wild_rift_mc():
#     # mc = mark cost 
#     iron_mc = models.FloatField(default=0.38) # 6.70
#     bronze_mc = models.FloatField(default=0.41) # 10.10
#     silver_mc = models.FloatField(default=0.58) # 10.00
#     gold_mc = models.FloatField(default=0.88) # 10.29
#     platinum_mc = models.FloatField(default=1.04) # 12.451
#     platinum_mc_from_I_to_emerald = models.FloatField(default=1.50)# 12.946
#     emerald_mc = models.FloatField(default=1.94)

# wildRift/models.py



class WildRiftRank(models.Model):
    rank_name = models.CharField(max_length=25)
    rank_image = models.ImageField(upload_to='wildRift/images/', blank=True, null=True)

    def __str__(self):
        return self.rank_name
    
    def get_image_url(self):
        return f"/media/{self.rank_image}"

class WildRiftTier(models.Model):
    rank = models.OneToOneField('WildRiftRank', related_name='tier', on_delete=models.CASCADE)
    from_IV_to_III = models.FloatField(default=0)
    from_III_to_II = models.FloatField(default=0)
    from_II_to_II = models.FloatField(default=0)
    from_I_to_IV_next = models.FloatField(default=0)

    def __str__(self):
        return f"Tiers for {self.rank.rank_name}"

class WildRiftMark(models.Model):
    class MarkChoices(models.IntegerChoices):
        MARK_2 = 2, '2 Marks'
        MARK_3 = 3, '3 Marks'
        MARK_4 = 4, '4 Marks'
        MARK_5 = 5, '5 Marks'
        MARK_6 = 6, '6 Marks'

    rank = models.OneToOneField('WildRiftRank', related_name='mark', on_delete=models.CASCADE)
    tier = models.OneToOneField(WildRiftTier, related_name='tier_mark', on_delete=models.CASCADE)
    mark_number = models.IntegerField(choices=MarkChoices.choices)
    mark_1 = models.FloatField(default=0)
    mark_2 = models.FloatField(default=0)
    mark_3 = models.FloatField(default=0)
    mark_4 = models.FloatField(default=0)
    mark_5 = models.FloatField(default=0)



    def __str__(self):
        return f"Mark {self.mark_number} for Tiers: {self.tier} in Rank: {self.rank.rank_name}"
    

class WildRiftPlacement(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField(upload_to='wildRift/images/', blank=True, null=True)
    price = models.FloatField()


    def __str__(self):
        return self.name
    
    def get_image_url(self):
        return f"/media/{self.image}"