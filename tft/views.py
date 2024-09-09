from django.shortcuts import render
from tft.models import *
from tft.controller.serializers import DivisionSerializer, PlacementSerializer
from tft.controller.order_information import get_division_order_result_by_rank, get_placement_order_result_by_rank
from booster.models import OrderRating
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from accounts.models import BaseUser
from gameBoosterss.utils import MadBoostPayment


def tftGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = TFTDivisionOrder.objects.get(order_id=extend_order)
  except:
    order = None
  ranks = TFTRank.objects.all().order_by('id')
  divisions  = TFTTier.objects.all().order_by('id')
  placements = TFTPlacement.objects.all().order_by('id')

  divisions_list = list(divisions.values())

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 5)
  game_pk_condition = Case(
    When(booster_orders__game__pk=5, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
  )
    
  boosters = BaseUser.objects.filter(
    is_booster = True,
    booster__is_tft_player=True,
    booster__can_choose_me=True
    ).annotate(
    order_count=Sum(game_pk_condition)
    ).order_by('id')
  

  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "placements": placements,
    "order": order,
    "feedbacks": feedbacks,
    "boosters": boosters,
  }
  return render(request,'tft/GetBoosterByRank.html', context)

class TFTPaymentAPiView(MadBoostPayment):
    serializer_orderInfo_mapping = {
        'D': [DivisionSerializer, get_division_order_result_by_rank],
        'P': [PlacementSerializer, get_placement_order_result_by_rank],
    }