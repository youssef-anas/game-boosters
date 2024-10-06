from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from csgo2.models import Csgo2Rank, Csgo2Tier, Csgo2DivisionOrder, CsgoFaceitPrice, Csgo2PremierOrder, Csgo2PremierPrice
from csgo2.controller.serializers import *
from csgo2.controller.order_information import *
from accounts.models import TokenForPay, BaseOrder
from django.contrib.auth.decorators import login_required
from booster.models import OrderRating
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from accounts.models import BaseUser
from csgo2.utils import get_division_prices, get_premier_prices, get_faceit_prices
from gameBoosterss.utils import NewMadBoostPayment


def get_division_prices_view(request):
  divisions_data = get_division_prices()
  return JsonResponse(divisions_data, safe=False)

def get_premier_prices_view(request):
    premier_prices = get_premier_prices()
    return JsonResponse(premier_prices, safe=False)

def get_faceit_prices_view(request):
    faceit_data = get_faceit_prices()
    return JsonResponse(faceit_data, safe=False)


def csgo2GetBoosterByRank(request):
  order_get_rank_value = None
  extend_order = request.GET.get('extend')

  if extend_order:
    try:
      order = BaseOrder.objects.get(id = extend_order, customer= request.user)
      extend_order_type = order.game_type
      if extend_order_type == 'D':
        order_get_rank_value = Csgo2DivisionOrder.objects.get(order_id=extend_order).get_rank_value()
      elif extend_order_type == 'A':
        order_get_rank_value = Csgo2PremierOrder.objects.get(order_id=extend_order).get_rank_value()

    except Exception as e:
      print(e)
      return redirect('homepage.index')
    
  ranks = Csgo2Rank.objects.all().order_by('id')
  divisions  = Csgo2Tier.objects.all().order_by('id')

  premier_prices = get_premier_prices()
  faceit_data = get_faceit_prices()

  divisions_list = list(divisions.values())

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 12)

  game_pk_condition = Case(
    When(booster_orders__game__pk=13, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
  )
    
  boosters = BaseUser.objects.filter(
      is_booster = True,
      booster__is_csgo2_player=True,
      booster__can_choose_me=True
      ).annotate(
      order_count=Sum(game_pk_condition)
      ).order_by('id')

  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "order_get_rank_value": order_get_rank_value,
    "premier_prices": premier_prices,
    "faceit_prices": faceit_data,
    "feedbacks": feedbacks,
    "boosters": boosters,
  }
  return render(request,'csgo2/GetBoosterByRank.html', context)

class CSGO2PaymentAPiView(NewMadBoostPayment):
    serializer_mapping = {
        'D': DivisionSerializer,
        'A': PremierSerializer,
        'F': FaceitSerializer,
    }