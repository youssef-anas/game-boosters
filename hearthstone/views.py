from django.shortcuts import render
from django.http import JsonResponse
from hearthstone.models import *
from hearthstone.controller.serializers import DivisionSerializer, BattleSerializer
from hearthstone.controller.order_information import *
from booster.models import OrderRating
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from accounts.models import BaseUser
from hearthstone.utils import get_hearthstone_divisions_data, get_hearthstone_marks_data, get_hearthstone_battle_prices
from gameBoosterss.utils import NewMadBoostPayment



def get_hearthstone_divisions_data_view(request):
    divisions_data = get_hearthstone_divisions_data()
    return JsonResponse(divisions_data, safe=False)

def get_hearthstone_marks_data_view(request):
    marks_data = get_hearthstone_marks_data()
    return JsonResponse(marks_data, safe=False)



def hearthstoneGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = HearthstoneDivisionOrder.objects.get(order_id=extend_order)
  except:
    try:
      order = HearthStoneBattleOrder.objects.get(order_id=extend_order)
    except:
      order = None

  ranks = HearthstoneRank.objects.all().order_by('id')
  divisions  = HearthstoneTier.objects.all().order_by('id')
  divisions_list = list(divisions.values())

  battle_prices = get_hearthstone_battle_prices()

   # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 7)
  game_pk_condition = Case(
    When(booster_orders__game__pk=7, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
  )
    
  boosters = BaseUser.objects.filter(
      is_booster = True,
      booster__is_hearthstone_player=True,
      booster__can_choose_me=True
      ).annotate(
      order_count=Sum(game_pk_condition)
      ).order_by('id')
  
  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "order": order,
    "feedbacks": feedbacks,
    "boosters":boosters,
    "battle_prices": battle_prices,
  }
  return render(request,'hearthstone/GetBoosterByRank.html', context)


class HearthstonePaymentAPiView(NewMadBoostPayment):
    serializer_mapping = {
        'D': DivisionSerializer,
        'A': BattleSerializer,
    }