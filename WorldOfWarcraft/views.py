from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.conf import settings
from WorldOfWarcraft.models import *
from WorldOfWarcraft.controller.serializers import ArenaSerializer
from paypal.standard.forms import PayPalPaymentsForm
from WorldOfWarcraft.controller.order_information import get_arena_order_result_by_rank
from booster.models import OrderRating
import json
from accounts.models import TokenForPay
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from accounts.models import BaseUser


def wowGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = WorldOfWarcraftArenaBoostOrder.objects.get(order_id=extend_order)
  except:
    order = None

  prices = WorldOfWarcraftRpsPrice.objects.all().first()

  prices_data = [prices.price_of_2vs2, prices.price_of_3vs3]

  with open('static/wow/data/prices.json', 'w') as json_file:
    json.dump(prices_data, json_file)

    
  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 6)
  
  game_pk_condition = Case(
        When(booster_division__game__pk=6, then=1),
    default=0,
    output_field=IntegerField()
    )
    
  boosters = BaseUser.objects.filter(
    is_booster = True,
    booster__is_wow_player=True,
    booster__can_choose_me=True
    ).annotate(
    average_rating=Coalesce(Avg('ratings_received__rate'), Value(0.0)),
    order_count=Sum(game_pk_condition)
    ).order_by('id')
  
  context = {
    # "ranks": ranks,
    "order": order,
    "feedbacks": feedbacks,
    "rp2vs2": prices.price_of_2vs2,
    "rp3vs3": prices.price_of_3vs3,
    "boosters": boosters,
  }
  return render(request,'wow/GetBoosterByRank.html', context)


# Paypal
@login_required
def pay_with_paypal(request):
  if request.method == 'POST' and request.user.is_authenticated:
    if request.user.is_booster:
      messages.error(request, "You are a booster!, You can't make order.")
      return redirect(reverse_lazy('wow'))
  print('request POST:  ', request.POST)

  # Division
  serializer = ArenaSerializer(data=request.POST)

  if serializer.is_valid():
    extend_order_id = serializer.validated_data['extend_order']
    # Arena
    order_info = get_arena_order_result_by_rank(serializer.validated_data,extend_order_id)

    request.session['invoice'] = order_info['invoice']
    token = TokenForPay.create_token_for_pay(request.user,  order_info['invoice'])

    paypal_dict = {
        "business": settings.PAYPAL_EMAIL,
        "amount": order_info['price'],
        "item_name": order_info['name'],
        "invoice": order_info['invoice'],
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(f"/customer/payment-success/{token}/"),
        "cancel_return": request.build_absolute_uri(f"/customer/payment-canceled/{token}/"),
    }
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "accounts/paypal.html", context,status=200)
  for field, errors in serializer.errors.items():
    for error in errors:
      messages.error(request, f"{field}: {error}")
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