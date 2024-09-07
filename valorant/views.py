from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from valorant.models import *
from valorant.controller.serializers import DivisionSerializer, PlacementSerializer
from valorant.controller.order_information import *
from booster.models import OrderRating
from accounts.models import TokenForPay
from customer.models import Champion
from accounts.models import BaseUser
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from .utils import get_valorant_divisions_data, get_valorant_marks_data, get_valorant_placements_data
from gameBoosterss.utils import PaypalPayment, cryptomus_payment

def valorant_divisions_data(request):
    divisions_data = get_valorant_divisions_data()
    return JsonResponse(divisions_data, safe=False)

def valorant_marks_data(request):
    marks_data = get_valorant_marks_data()
    return JsonResponse(marks_data, safe=False)

def valorant_placements_data(request):
    placements_data = get_valorant_placements_data()
    return JsonResponse(placements_data, safe=False)

def valorantGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = ValorantDivisionOrder.objects.get(order_id=extend_order)
  except:
    order = None
  ranks = ValorantRank.objects.all().order_by('id')
  divisions  = ValorantTier.objects.all().order_by('id')
  placements = ValorantPlacement.objects.all().order_by('id')
  champions = Champion.objects.filter(game__id =2).order_by('id')

  # Here I make condition when game_id = 2
  game_pk_condition = Case(
    When(booster_orders__game__pk=2, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
  )
  
  boosters = BaseUser.objects.filter(
    is_booster = True,
    booster__is_valo_player=True,
    booster__can_choose_me=True
  ).annotate(
    order_count=Sum(game_pk_condition)
  ).order_by('id')

  divisions_list = list(divisions.values())

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 2)
  
  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "placements": placements,
    "order":order,
    "feedbacks": feedbacks,
    'champions' : champions,
    'boosters': boosters,
  }
  return render(request,'valorant/GetBoosterByRank.html', context)

@login_required
def pay_with_paypal(request):
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('valorant'))
      # Division
      if request.POST.get('game_type') == 'D':
        serializer = DivisionSerializer(data=request.POST)
      # Placement
      elif request.POST.get('game_type') == 'P':
        serializer = PlacementSerializer(data=request.POST)

      if serializer.is_valid():
        extend_order_id = 0
        # Division
        if request.POST.get('game_type') == 'D':
          extend_order_id = serializer.validated_data['extend_order']
          order_info = get_division_order_result_by_rank(serializer.validated_data,extend_order_id)
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
            return redirect(reverse_lazy('valorant'))

      
      # return JsonResponse({'error': serializer.errors}, status=400)
      for field, errors in serializer.errors.items():
        for error in errors:
            messages.error(request, f"{error}")
      return redirect(reverse_lazy('valorant'))
  return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)

@login_required
def pay_with_cryptomus(request):
  if request.method == 'POST':
    context = {
      "data": request.POST
    }
    return render(request, "accounts/cryptomus.html", context,status=200)
  return render(request, "accounts/cryptomus.html", context={"data": "There is error"},status=200)