from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.conf import settings
from dota2.models import *
from dota2.controller.serializers import *
from dota2.controller.order_information import get_rank_boost_order_result_by_rank, get_palcement_order_result_by_rank
from accounts.models import TokenForPay
from booster.models import OrderRating
import json
from accounts.models import BaseUser
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from dota2.utils import get_division_prices, get_placement_prices
from gameBoosterss.utils import NewMadBoostPayment


def division_prices_view(request):
    division_prices = get_division_prices()
    return JsonResponse(division_prices, safe=False)

def placement_prices_view(request):
    placement_prices = get_placement_prices()
    return JsonResponse(placement_prices, safe=False)



def dota2GetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = Dota2RankBoostOrder.objects.get(order_id=extend_order)
  except:
    order = None

  division_prices = get_division_prices()
  placement_prices = get_placement_prices()

  game_pk_condition = Case(
    When(booster_orders__game__pk=10, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
  )
  
  boosters = BaseUser.objects.filter(
      is_booster = True,
      booster__is_dota2_player=True,
      booster__can_choose_me=True
    ).annotate(
      order_count=Sum(game_pk_condition)
    ).order_by('id')

  ranks_images = [rank.rank_image.url for rank in Dota2Rank.objects.all()]
  ranks_images = json.dumps(ranks_images)

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 10)

  context = {
    "order":order,
    "feedback": feedbacks,
    "division_price": division_prices,
    "placement_prices": placement_prices,
    "ranks_images": ranks_images,
    "boosters": boosters,
  }

  return render(request,'dota2/GetBoosterByRank.html', context)


class DOTA2PaymentAPiView(NewMadBoostPayment):
    serializer_mapping = {
        'A': RankBoostSerializer,
        'P': PlacementSerializer,
    }