from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from leagueOfLegends.models import *
from leagueOfLegends.controller.serializers import DivisionSerializer, PlacementSerializer
from paypal.standard.forms import PayPalPaymentsForm
from leagueOfLegends.controller.order_information import *
from accounts.models import TokenForPay
from booster.models import OrderRating
from accounts.models import BaseUser
from customer.models import Champion
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce

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
    When(booster_division__game__pk=4, then=1),
    default=0,
    output_field=IntegerField()
    )
    
  boosters = BaseUser.objects.filter(
    is_booster = True,
    booster__is_lol_player=True,
    booster__can_choose_me=True
    ).annotate(
    average_rating=Coalesce(Avg('ratings_received__rate'), Value(0.0)),
    order_count=Sum(game_pk_condition)
    ).order_by('id')

  divisions_data = [
    [division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_IV_next]
    for division in divisions
  ]

  marks_data = [
    [mark.marks_0_20, mark.marks_21_40, mark.marks_41_60, mark.marks_61_80, mark.marks_81_99, mark.marks_series]
    for mark in marks
  ]

  placements_data = [
    placement.price
    for placement in placements
  ]

  with open('static/lol/data/divisions_data.json', 'w') as json_file:
    json.dump(divisions_data, json_file)

  with open('static/lol/data/marks_data.json', 'w') as json_file:
    json.dump(marks_data, json_file)

  with open('static/lol/data/placements_data.json', 'w') as json_file:
    json.dump(placements_data, json_file)

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

@login_required
def pay_with_paypal(request):
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('lol'))
      
    print('request POST:  ', request.POST)
    try:
      # Division
      if request.POST.get('game_type') == 'D':
        serializer = DivisionSerializer(data=request.POST)
      # Placement
      elif request.POST.get('game_type') == 'P':
        serializer = PlacementSerializer(data=request.POST)

      if serializer.is_valid():
        extend_order_id = serializer.validated_data['extend_order']
        # Division
        if request.POST.get('game_type') == 'D':
          order_info = get_division_order_result_by_rank(serializer.validated_data,extend_order_id)
          print('Order Info: ', order_info)
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
      # return JsonResponse({'error': serializer.errors}, status=400)
      messages.error(request, 'Ensure this value is greater than or equal to 10')
      return redirect(reverse_lazy('lol'))
    except Exception as e:
      return JsonResponse({'error': f'Error processing form data: {str(e)}'}, status=400)

  return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)

@login_required
def pay_with_cryptomus(request):
  if request.method == 'POST':
    context = {
      "data": request.POST
    }
    return render(request, "accounts/cryptomus.html", context,status=200)
  return render(request, "accounts/cryptomus.html", context={"data": "There is error"},status=200)