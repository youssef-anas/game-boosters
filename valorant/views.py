from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from valorant.models import *
from valorant.controller.serializers import DivisionSerializer, PlacementSerializer
from valorant.controller.order_information import *
from booster.models import OrderRating
from customer.models import Champion
from accounts.models import BaseUser
from django.db.models import Sum, Case, When, IntegerField
from .utils import get_valorant_divisions_data, get_valorant_marks_data, get_valorant_placements_data
from gameBoosterss.utils import NewMadBoostPayment

def valorant_divisions_data(request):
    divisions_data = get_valorant_divisions_data()
    return JsonResponse(divisions_data, safe=False)

def valorant_marks_data(request):
    marks_data = get_valorant_marks_data()
    return JsonResponse(marks_data, safe=False)

def valorant_placements_data(request):
    placements_data = get_valorant_placements_data()
    return JsonResponse(placements_data, safe=False)

def valorantGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = ValorantDivisionOrder.objects.get(order_id=extend_order)
  except:
    order = None
  ranks = ValorantRank.objects.all().order_by('id')
  divisions  = ValorantTier.objects.all().order_by('id')
  placements = ValorantPlacement.objects.all().order_by('id')
  champions = Champion.objects.filter(game__id =2).order_by('id')

  # Here I make condition when game_id = 2
  game_pk_condition = Case(
    When(booster_orders__game__pk=2, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
  )
  
  boosters = BaseUser.objects.filter(
    is_booster = True,
    booster__is_valo_player=True,
    booster__can_choose_me=True
  ).annotate(
    order_count=Sum(game_pk_condition)
  ).order_by('id')

  divisions_list = list(divisions.values())

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 2)
  
  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "placements": placements,
    "order":order,
    "feedbacks": feedbacks,
    'champions' : champions,
    'boosters': boosters,
  }
  return render(request,'valorant/GetBoosterByRank.html', context)


# class ValoPaymentAPiView(MadBoostPayment):
#     serializer_orderInfo_mapping = {
#         'D': [DivisionSerializer, get_division_order_result_by_rank],
#         'P': [PlacementSerializer, get_placement_order_result_by_rank],
#     }

class ValoPaymentAPiView(NewMadBoostPayment):
    serializer_mapping = {
        'D': DivisionSerializer,
        'P': PlacementSerializer,
    }