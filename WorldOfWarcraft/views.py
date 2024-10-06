from django.shortcuts import render
from django.http import JsonResponse
from WorldOfWarcraft.models import WorldOfWarcraftRpsPrice, WorldOfWarcraftArenaBoostOrder, WorldOfWarcraftBoss, WorldOfWarcraftBundle
from WorldOfWarcraft.controller.serializers import ArenaSerializer, RaidSimpleSerializer, RaidBundleSerializer, DungeonSimpleSerializer, RaidLevelSerializer
from booster.models import OrderRating
from django.db.models import Sum, Case, When, IntegerField
from accounts.models import BaseUser
from .utils import get_level_up_price, get_keyston_price
from gameBoosterss.utils import NewMadBoostPayment

def get_wow_prices_data_view(request):
    prices = WorldOfWarcraftRpsPrice.objects.all().first()
    prices_data = [prices.price_of_2vs2, prices.price_of_3vs3]
    return JsonResponse(prices_data, safe=False)


def wowGetBoosterByRank(request):
  level_up_price = get_level_up_price()
  dungeon_prices = get_keyston_price()
  extend_order = request.GET.get('extend')
  try:
    order = WorldOfWarcraftArenaBoostOrder.objects.get(order_id=extend_order)
  except:
    order = None

  prices = WorldOfWarcraftRpsPrice.objects.all().first()

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 6)
  
  game_pk_condition = Case(
    When(booster_orders__game__pk=6, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
    )
    
  boosters = BaseUser.objects.filter(
    is_booster = True,
    booster__is_wow_player=True,
    booster__can_choose_me=True
    ).annotate(
    order_count=Sum(game_pk_condition)
    ).order_by('id')
  

  bosses = WorldOfWarcraftBoss.objects.all()
  bundles = WorldOfWarcraftBundle.objects.all()
  
  context = {
    "order": order,
    "feedbacks": feedbacks,
    "rp2vs2": prices.price_of_2vs2,
    "rp3vs3": prices.price_of_3vs3,
    "boosters": boosters,
    "bosses": bosses,
    "bundles": bundles,
    'level_up_price': level_up_price,
    'dungeon_prices': dungeon_prices,
  }
  return render(request,'wow/GetBoosterByRank.html', context)

class WowPaymenApiView(NewMadBoostPayment):
    serializer_mapping = {
        'R': RaidSimpleSerializer,
        'A': ArenaSerializer,
        'RB': RaidBundleSerializer,
        'DU': DungeonSimpleSerializer,
        'F': RaidLevelSerializer,
    }