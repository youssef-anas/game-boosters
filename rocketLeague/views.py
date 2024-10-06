from django.shortcuts import render, redirect
from django.http import JsonResponse
from rocketLeague.models import *
from rocketLeague.controller.serializers import *
from rocketLeague.controller.order_information import *
from booster.models import OrderRating
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from accounts.models import BaseUser
from .utils import (
    get_rocket_league_divisions_data,
    get_rocket_league_placements_data,
    get_rocket_league_seasonals_data,
    get_rocket_league_tournaments_data
)
from gameBoosterss.utils import NewMadBoostPayment

def rocket_league_divisions_data_api(request):
    divisions_data = get_rocket_league_divisions_data()
    return JsonResponse(divisions_data, safe=False)

def rocket_league_placements_data_api(request):
    placements_data = get_rocket_league_placements_data()
    return JsonResponse(placements_data, safe=False)

def rocket_league_seasonals_data_api(request):
    seasonals_data = get_rocket_league_seasonals_data()
    return JsonResponse(seasonals_data, safe=False)

def rocket_league_tournaments_data_api(request):
    tournaments_data = get_rocket_league_tournaments_data()
    return JsonResponse(tournaments_data, safe=False)



def rocketLeagueGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = RocketLeagueDivisionOrder.objects.get(order_id=extend_order)
  except:
    order = None
  ranks = RocketLeagueRank.objects.all().order_by('id')
  divisions  = RocketLeagueDivision.objects.all().order_by('id')
  placements = RocketLeaguePlacement.objects.all().order_by('id')
  seasonals = RocketLeagueSeasonal.objects.all().order_by('id')
  tournaments = RocketLeagueTournament.objects.all().order_by('id')

  divisions_list = list(divisions.values())

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 9)
  game_pk_condition = Case(
    When(booster_orders__game__pk=9, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
    )
    
  boosters = BaseUser.objects.filter(
    is_booster = True,
    booster__is_rl_player=True,
    booster__can_choose_me=True
    ).annotate(
    order_count=Sum(game_pk_condition)
    ).order_by('id')
  
  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "placements": placements,
    "seasonals": seasonals,
    "tournaments": tournaments,
    "order":order,
    "feedbacks": feedbacks,
    "boosters": boosters,
  }
  return render(request,'rocketLeague/GetBoosterByRank.html', context)

# Paypal
class RocketLeaguePaymentAPiView(NewMadBoostPayment):
    serializer_mapping = {
        'D': DivisionSerializer,
        'P': PlacementSerializer,
        'S': SeasonalSerializer,
        'T': TournamentSerializer,
    }