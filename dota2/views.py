from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.conf import settings
from dota2.models import *
from dota2.controller.serializers import *
from dota2.controller.order_information import *
from accounts.models import TokenForPay
from booster.models import OrderRating
import json
from accounts.models import BaseUser
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from dota2.utils import get_division_prices, get_placement_prices
from gameBoosterss.utils import PaypalPayment, cryptomus_payment


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


# Paypal
@login_required
def pay_with_paypal(request):
  if request.method == 'POST' and request.user.is_authenticated:
    if request.user.is_booster:
      messages.error(request, "You are a booster!, You can't make order.")
      return redirect(reverse_lazy('dota2'))
      # Division
    if request.POST.get('game_type') == 'A':
      serializer = RankBoostSerializer(data=request.POST)
    # Placement
    elif request.POST.get('game_type') == 'P':
      serializer = PlacementSerializer(data=request.POST)
    
    if serializer.is_valid():
      extend_order_id = serializer.validated_data['extend_order']
      # Division
      if request.POST.get('game_type') == 'A':
        order_info = get_rank_boost_order_result_by_rank(serializer.validated_data,extend_order_id)
      # Placement
      elif request.POST.get('game_type') == 'P':
        order_info = get_palcement_order_result_by_rank(serializer.validated_data,extend_order_id)

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
          return redirect(reverse_lazy('dota2'))
    
    for field, errors in serializer.errors.items():
      for error in errors:
          messages.error(request, f"{error}")
    return redirect(reverse_lazy('dota2'))

  return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)

@login_required
def pay_with_cryptomus(request):
  if request.method == 'POST':
    context = {
      "data": request.POST
    }
    return render(request, "accounts/cryptomus.html", context,status=200)
  return render(request, "accounts/cryptomus.html", context={"data": "There is error"},status=200)