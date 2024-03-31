from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.conf import settings
from dota2.models import *
from dota2.controller.serializers import *
from paypal.standard.forms import PayPalPaymentsForm
from dota2.controller.order_information import *
from accounts.models import TokenForPay
from booster.models import OrderRating
import json
from accounts.models import BaseUser
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce

def dota2GetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = Dota2RankBoostOrder.objects.get(order_id=extend_order)
  except:
    order = None

  division_row = Dota2MmrPrice.objects.all().first()
  division_prices = [division_row.price_0_2000, division_row.price_2000_3000, division_row.price_3000_4000, division_row.price_4000_5000, division_row.price_5000_5500, division_row.price_5500_6000, division_row.price_6000_extra]


  placement_prices = []
  placement_rows = Dota2Placement.objects.all()

  for row in placement_rows:
    placement_prices.append(row.price)

  prices_data = {
    "division": division_prices,
    "placement": placement_prices,
  }
  game_pk_condition = Case(
    When(booster_division__game__pk=10, then=1),
    default=0,
    output_field=IntegerField()
  )
  
  boosters = BaseUser.objects.filter(
      is_booster = True,
      booster__is_dota2_player=True,
      booster__can_choose_me=True
    ).annotate(
      average_rating=Coalesce(Avg('ratings_received__rate'), Value(0.0)),
      order_count=Sum(game_pk_condition)
    ).order_by('id')

  ranks_images = [rank.rank_image.url for rank in Dota2Rank.objects.all()]
  ranks_images = json.dumps(ranks_images)

  with open('static/dota2/data/prices.json', 'w') as json_file:
    json.dump(prices_data, json_file)

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