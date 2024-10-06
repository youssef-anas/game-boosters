from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from leagueOfLegends.models import *
from leagueOfLegends.controller.serializers import DivisionSerializer, PlacementSerializer
from leagueOfLegends.controller.order_information import *
from accounts.models import TokenForPay
from booster.models import OrderRating
from accounts.models import BaseUser
from customer.models import Champion
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from leagueOfLegends.utils import get_lol_placements_data, get_lol_marks_data, get_lol_divisions_data
from gameBoosterss.utils import NewMadBoostPayment

def get_lol_divisions_data_view(request):
    divisions_data = get_lol_divisions_data()
    return JsonResponse(divisions_data, safe=False)

def get_lol_marks_data_view(request):
    marks_data = get_lol_marks_data()
    return JsonResponse(marks_data, safe=False)

def get_lol_placements_data_view(request):
    placements_data = get_lol_placements_data()
    return JsonResponse(placements_data, safe=False)


def leagueOfLegendsGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = LeagueOfLegendsDivisionOrder.objects.get(order_id=extend_order)
  except:
    order = None
  ranks = LeagueOfLegendsRank.objects.all().order_by('id')
  divisions  = LeagueOfLegendsTier.objects.all().order_by('id')
  marks = LeagueOfLegendsMark.objects.all().order_by('id')
  placements = LeagueOfLegendsPlacement.objects.all().order_by('id')
  champions = Champion.objects.filter(game__id =4).order_by('id')

  game_pk_condition = Case(
    When(booster_orders__game__pk=4, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
  )
    
  boosters = BaseUser.objects.filter(
    is_booster = True,
    booster__is_lol_player=True,
    booster__can_choose_me=True
    ).annotate(
    order_count=Sum(game_pk_condition)
    ).order_by('id')

  divisions_list = list(divisions.values())

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 4)

  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "placements": placements,
    "order":order,
    "feedbacks": feedbacks,
    'boosters': boosters,
    'champions': champions,
  }
  return render(request,'leagueOfLegends/GetBoosterByRank.html', context)

class LOLPaymentAPiView(NewMadBoostPayment):
    serializer_mapping = {
        'D': DivisionSerializer,
        'P': PlacementSerializer,
    }