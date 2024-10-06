from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from mobileLegends.models import *
from mobileLegends.controller.serializers import DivisionSerializer, PlacementSerializer
from mobileLegends.controller.order_information import *
from accounts.models import TokenForPay
from django.contrib.auth.decorators import login_required
from booster.models import OrderRating
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from accounts.models import BaseUser
from .utils import get_mobile_legends_divisions_data, get_mobile_legends_marks_data, get_mobile_legends_placements_data
from gameBoosterss.utils import NewMadBoostPayment



def get_mobile_legends_divisions_view(request):
    divisions_data = get_mobile_legends_divisions_data()
    return JsonResponse(divisions_data, safe=False)

def get_mobile_legends_marks_view(request):
    marks_data = get_mobile_legends_marks_data()
    return JsonResponse(marks_data, safe=False)

def get_mobile_legends_placements_view(request):
    placements_data = get_mobile_legends_placements_data()
    return JsonResponse(placements_data, safe=False)



# Create your views here.
def MobileLegendsGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order_get_rank_value = MobileLegendsDivisionOrder.objects.get(order_id=extend_order).get_rank_value()
  except:
    order_get_rank_value = None
  ranks = MobileLegendsRank.objects.all().order_by('id')
  divisions  = MobileLegendsTier.objects.all().order_by('id')
  placements = MobileLegendsPlacement.objects.all().order_by('id')

  divisions_list = list(divisions.values())
  
  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 8)
  game_pk_condition = Case(
    When(booster_orders__game__pk=8, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
  )
    
  boosters = BaseUser.objects.filter(
      is_booster = True,
      booster__is_mobleg_player=True,
      booster__can_choose_me=True
      ).annotate(
      order_count=Sum(game_pk_condition)
      ).order_by('id')

  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "placements": placements,
    "order_get_rank_value":order_get_rank_value,
    "feedbacks": feedbacks,
    "boosters" : boosters,
  }
  return render(request,'mobileLegends/GetBoosterByRank.html', context)

class MobLegPaymentAPiView(NewMadBoostPayment):
    serializer_mapping = {
        'D': DivisionSerializer,
        'P': PlacementSerializer
    }
