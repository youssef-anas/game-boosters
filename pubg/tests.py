from django.test import TestCase
from pubg.models import PubgRank, PubgTier, PubgMark

# Create your tests here.
class SetUp(TestCase):
  ranks = [
    PubgRank(rank_name = 'bronze', rank_image = 'pubg/images/bronze.webp'),
    PubgRank(rank_name = 'silver', rank_image = 'pubg/images/silver.webp'),
    PubgRank(rank_name = 'gold', rank_image = 'pubg/images/gold.webp'),
    PubgRank(rank_name = 'platinum', rank_image = 'pubg/images/platinum.webp'),
    PubgRank(rank_name = 'diamond', rank_image = 'pubg/images/diamond.webp'),
    PubgRank(rank_name = 'crown', rank_image = 'pubg/images/diamond.webp'),
    PubgRank(rank_name = 'ace', rank_image = 'pubg/images/diamond.webp'),
    PubgRank(rank_name = 'ace master', rank_image = 'pubg/images/master.webp'),
    PubgRank(rank_name = 'ace domenater', rank_image = 'pubg/images/master.webp'),
  ]

  tiers = [
      PubgTier(rank_id=1, from_V_to_VI=5.0, from_VI_to_III=5.0, from_III_to_II=5.0, from_II_to_I=5.0, from_I_to_V_next=5.0),
      PubgTier(rank_id=2, from_V_to_VI=5.5, from_VI_to_III=6.0, from_III_to_II=5.5, from_I_to_V_next=5.0, from_II_to_I=10.0),
      PubgTier(rank_id=3, from_V_to_VI=6.5, from_VI_to_III=6.5, from_III_to_II=6.5, from_I_to_V_next=6.0, from_II_to_I=15.0),
      PubgTier(rank_id=4, from_V_to_VI=10.0, from_VI_to_III=10.0, from_III_to_II=10.0, from_I_to_V_next=10.0, from_II_to_I=20.0),
      PubgTier(rank_id=5, from_V_to_VI=15.0, from_VI_to_III=15.0, from_III_to_II=15.0, from_I_to_V_next=16.0, from_II_to_I=25.0),
      PubgTier(rank_id=6, from_V_to_VI=15.0, from_VI_to_III=15.0, from_III_to_II=15.0, from_I_to_V_next=16.0, from_II_to_I=30.0),
      PubgTier(rank_id=7, from_V_to_VI=15.0, from_VI_to_III=15.0, from_III_to_II=15.0, from_I_to_V_next=16.0, from_II_to_I=35.0),
      PubgTier(rank_id=8, from_V_to_VI=15.0, from_VI_to_III=15.0, from_III_to_II=15.0, from_I_to_V_next=16.0, from_II_to_I=40.0),
      PubgTier(rank_id=9, from_V_to_VI=17.0, from_VI_to_III=19.0, from_III_to_II=21.0, from_I_to_V_next=30.0, from_II_to_I=40.0)
  ]


  marks = [
      PubgMark(rank_id=1, marks_0_20=0.0, marks_21_40=1.0, marks_41_60=2.0, marks_61_80=3.0, marks_81_100=4.0),
      PubgMark(rank_id=2, marks_0_20=0.0, marks_21_40=1.5, marks_41_60=3.0, marks_61_80=4.5, marks_81_100=6.0),
      PubgMark(rank_id=3, marks_0_20=0.0, marks_21_40=2.0, marks_41_60=4.0, marks_61_80=6.0, marks_81_100=8.0),
      PubgMark(rank_id=4, marks_0_20=0.0, marks_21_40=2.5, marks_41_60=5.0, marks_61_80=7.5, marks_81_100=10.0),
      PubgMark(rank_id=5, marks_0_20=0.0, marks_21_40=3.0, marks_41_60=6.0, marks_61_80=9.0, marks_81_100=12.0),
      PubgMark(rank_id=6, marks_0_20=0.0, marks_21_40=3.5, marks_41_60=7.0, marks_61_80=10.5, marks_81_100=14.0),
      PubgMark(rank_id=7, marks_0_20=0.0, marks_21_40=4.0, marks_41_60=8.0, marks_61_80=12.0, marks_81_100=16.0),
      PubgMark(rank_id=8, marks_0_20=0.0, marks_21_40=4.5, marks_41_60=9.0, marks_61_80=13.5, marks_81_100=18.0),
      PubgMark(rank_id=9, marks_0_20=0.0, marks_21_40=4.5, marks_41_60=9.0, marks_61_80=13.5, marks_81_100=18.0),
  ]

  ranks_queryset = PubgRank.objects.bulk_create(ranks)
  tiers_queryset = PubgTier.objects.bulk_create(tiers)
  marks_queryset = PubgMark.objects.bulk_create(marks)