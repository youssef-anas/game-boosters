from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from hearthstone.models import *
from hearthstone.controller.serializers import DivisionSerializer
from paypal.standard.forms import PayPalPaymentsForm
from hearthstone.controller.order_information import *
from booster.models import OrderRating
from accounts.models import TokenForPay
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from accounts.models import BaseUser

# Create your views here.
def hearthstoneGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = HearthstoneDivisionOrder.objects.get(order_id=extend_order)
  except:
    order = None
  ranks = HearthstoneRank.objects.all().order_by('id')
  divisions  = HearthstoneTier.objects.all().order_by('id')
  marks = HearthstoneMark.objects.all().order_by('id')

  divisions_data = [
    [division.from_X_to_IX, division.from_IX_to_VIII, division.from_VIII_to_VII, division.from_VII_to_VI, division.from_VI_to_V, division.from_V_to_IV, division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_IV_next]
    for division in divisions
  ]

  marks_data = [
    [0, mark.marks_3, mark.marks_2, mark.marks_1]
    for mark in marks
  ]

  with open('static/hearthstone/data/divisions_data.json', 'w') as json_file:
    json.dump(divisions_data, json_file)

  with open('static/hearthstone/data/marks_data.json', 'w') as json_file:
    json.dump(marks_data, json_file)

  divisions_list = list(divisions.values())

   # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 7)
  game_pk_condition = Case(
    When(booster_orders__game__pk=7, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
  )
    
  boosters = BaseUser.objects.filter(
      is_booster = True,
      booster__is_hearthstone_player=True,
      booster__can_choose_me=True
      ).annotate(
      order_count=Sum(game_pk_condition)
      ).order_by('id')
  
  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "order": order,
    "feedbacks": feedbacks,
    "boosters":boosters,
  }
  return render(request,'hearthstone/GetBoosterByRank.html', context)

# Paypal
@login_required
def pay_with_paypal(request):
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('hearthstone'))
      
    print('request POST:  ', request.POST)
    # Division
    if request.POST.get('game_type') == 'D':
      serializer = DivisionSerializer(data=request.POST)

    if serializer.is_valid():
      extend_order_id = serializer.validated_data['extend_order']
      # Division
      if request.POST.get('game_type') == 'D':
        order_info = get_division_order_result_by_rank(serializer.validated_data,extend_order_id)
        print('Order Info: ', order_info)

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
    return redirect(reverse_lazy('hearthstone'))
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