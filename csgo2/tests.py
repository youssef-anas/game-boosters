from django.test import TestCase
from .models import Csgo2Rank, Csgo2Tier

class SetUp(TestCase):
    ranks = [
    Csgo2Rank(rank_name='Silver I', rank_image='csgo2/images/silver1.png'),
    Csgo2Rank(rank_name='Silver II', rank_image='csgo2/images/silver2.png'),
    Csgo2Rank(rank_name='Silver III', rank_image='csgo2/images/silver3.png'),
    Csgo2Rank(rank_name='Silver IV', rank_image='csgo2/images/silver4.png'),
    Csgo2Rank(rank_name='Silver Elite', rank_image='csgo2/images/silver_elite.png'),
    Csgo2Rank(rank_name='SE Master', rank_image='csgo2/images/se_master.png'),
    Csgo2Rank(rank_name='Gold NV I', rank_image='csgo2/images/gold_nova1.png'),
    Csgo2Rank(rank_name='Gold NV II', rank_image='csgo2/images/gold_nova2.png'),
    Csgo2Rank(rank_name='Gold NV III', rank_image='csgo2/images/gold_nova3.png'),
    Csgo2Rank(rank_name='Gold NV Master', rank_image='csgo2/images/gold_nova_master.png'),
    Csgo2Rank(rank_name='Master Grd I', rank_image='csgo2/images/master_guardian1.png'),
    Csgo2Rank(rank_name='Master Grd II', rank_image='csgo2/images/master_guardian2.png'),
    Csgo2Rank(rank_name='Master Grd Elite', rank_image='csgo2/images/master_guardian_elite.png'),
    Csgo2Rank(rank_name='D Master Grd', rank_image='csgo2/images/distinguished_master_guardian.png'),
    Csgo2Rank(rank_name='Leg Eagle', rank_image='csgo2/images/legendary_eagle.png'),
    Csgo2Rank(rank_name='Leg Eagle Master', rank_image='csgo2/images/legendary_eagle_master.png'),
    Csgo2Rank(rank_name='Supre Master FC', rank_image='csgo2/images/supreme_master_first_class.png'),
    Csgo2Rank(rank_name='Global Elite', rank_image='csgo2/images/global_elite.png')
    ]
    
    tiers = [
        Csgo2Tier(rank_id=1, from_I_to_I_next=10),
        Csgo2Tier(rank_id=2, from_I_to_I_next=15),
        Csgo2Tier(rank_id=3, from_I_to_I_next=20),
        Csgo2Tier(rank_id=4, from_I_to_I_next=25),
        Csgo2Tier(rank_id=5, from_I_to_I_next=30),
        Csgo2Tier(rank_id=6, from_I_to_I_next=35),
        Csgo2Tier(rank_id=7, from_I_to_I_next=40),
        Csgo2Tier(rank_id=8, from_I_to_I_next=45),
        Csgo2Tier(rank_id=9, from_I_to_I_next=50),
        Csgo2Tier(rank_id=10, from_I_to_I_next=55),
        Csgo2Tier(rank_id=11, from_I_to_I_next=60),
        Csgo2Tier(rank_id=12, from_I_to_I_next=65),
        Csgo2Tier(rank_id=13, from_I_to_I_next=70),
        Csgo2Tier(rank_id=14, from_I_to_I_next=75),
        Csgo2Tier(rank_id=15, from_I_to_I_next=80),
        Csgo2Tier(rank_id=16, from_I_to_I_next=85),
        Csgo2Tier(rank_id=17, from_I_to_I_next=90),
        Csgo2Tier(rank_id=18, from_I_to_I_next=95)
    ]


    ranks_queryset = Csgo2Rank.objects.bulk_create(ranks)
    price_queryset = Csgo2Tier.objects.bulk_create(tiers)