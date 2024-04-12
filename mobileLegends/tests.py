from django.test import TestCase
from mobileLegends.models import *

# Create your tests here.
class SetUp(TestCase):
  ranks = [
    MobileLegendsRank(rank_name = 'warrior', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'elite', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'master', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'grandmaster', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'epic', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'legend', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'mythic', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'mythical honor', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'mythical glory', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'mythical immortal', rank_image = 'lol/images/platinum.webp'),
  ]

  marks = [
    MobileLegendsMark(rank_id =1, star_1 =2, star_2 =4, star_3= 6, star_4= 0, star_5 =0),
    MobileLegendsMark(rank_id =2, star_1 =2, star_2 =4, star_3= 6, star_4= 0, star_5 =0),

    MobileLegendsMark(rank_id =3, star_1 =2, star_2 =4, star_3= 6, star_4= 8, star_5 =0),

    MobileLegendsMark(rank_id =4, star_1 =2, star_2 =4, star_3= 6, star_4= 8, star_5 =10),
    MobileLegendsMark(rank_id =5, star_1 =2, star_2 =4, star_3= 6, star_4= 8, star_5 =10),
    MobileLegendsMark(rank_id =6, star_1 =2, star_2 =4, star_3= 6, star_4= 8, star_5 =10),

    MobileLegendsMark(rank_id =7, star_1 =0, star_2 =0, star_3= 0, star_4= 0, star_5 =0),
    MobileLegendsMark(rank_id =8, star_1 =0, star_2 =0, star_3= 0, star_4= 0, star_5 =0),
    MobileLegendsMark(rank_id =9, star_1 =0, star_2 =0, star_3= 0, star_4= 0, star_5 =0),
    MobileLegendsMark(rank_id =10, star_1 =0, star_2 =0, star_3= 0, star_4= 0, star_5 =0),
  ]

  ranks_queryset = MobileLegendsRank.objects.bulk_create(ranks)
  marks_queryset = MobileLegendsMark.objects.bulk_create(marks)
#   placements_queryset = LeagueOfLegendsPlacement.objects.bulk_create(placements)
#   tiers_queryset = LeagueOfLegendsTier.objects.bulk_create(tiers)