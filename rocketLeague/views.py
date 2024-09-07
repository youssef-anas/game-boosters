from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from rocketLeague.models import *
from rocketLeague.controller.serializers import *
from rocketLeague.controller.order_information import *
from booster.models import OrderRating
from accounts.models import TokenForPay
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from accounts.models import BaseUser
from .utils import (
    get_rocket_league_divisions_data,
    get_rocket_league_placements_data,
    get_rocket_league_seasonals_data,
    get_rocket_league_tournaments_data
)
from gameBoosterss.utils import PaypalPayment, cryptomus_payment

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
@login_required
def pay_with_paypal(request):
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('rocketLeague'))
    # Division
    if request.POST.get('game_type') == 'D':
      serializer = DivisionSerializer(data=request.POST)
    # Placement
    elif request.POST.get('game_type') == 'P':
      serializer = PlacementSerializer(data=request.POST)
    # Seasonal
    elif request.POST.get('game_type') == 'S':
      serializer = SeasonalSerializer(data=request.POST)
    # Tournament
    elif request.POST.get('game_type') == 'T':
      serializer = TournamentSerializer(data=request.POST)

    if serializer.is_valid():
      # Division
      extend_order_id = 0
      if request.POST.get('game_type') == 'D':
        order_info = get_division_order_result_by_rank(serializer.validated_data,extend_order_id)
        extend_order_id = serializer.validated_data['extend_order']
      # Placement
      elif request.POST.get('game_type') == 'P':
        order_info = get_palcement_order_result_by_rank(serializer.validated_data,extend_order_id)
      # Seasonal
      elif request.POST.get('game_type') == 'S':
        order_info = get_seasonal_order_result_by_rank(serializer.validated_data,extend_order_id)
      # Tournament
      elif request.POST.get('game_type') == 'T':
        order_info = get_tournament_order_result_by_rank(serializer.validated_data,extend_order_id)

      request.session['invoice'] = order_info['invoice']
      token = TokenForPay.create_token_for_pay(request.user,  order_info['invoice'])

      if request.POST.get('cryptomus', None) != None :
        payment = cryptomus_payment(order_info, request, token)
      else:
        payment = PaypalPayment(order_info, request, token)
      if payment:
          return JsonResponse({'url': payment})
      else:
          messages.error(request, "There was an issue connecting to PayPal. Please try again later.")
          return redirect(reverse_lazy('rocketLeague'))
    for field, errors in serializer.errors.items():
      for error in errors:
        messages.error(request, f"{error}")
    return redirect(reverse_lazy('rocketLeague'))
  return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)

# Cryptomus
@login_required
def pay_with_cryptomus(request):
  if request.method == 'POST':
    context = {
      "data": request.POST
    }
    return render(request, "accounts/cryptomus.html", context,status=200)
  return render(request, "accounts/cryptomus.html", context={"data": "There is error"},status=200)