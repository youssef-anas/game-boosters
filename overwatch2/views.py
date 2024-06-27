from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from overwatch2.models import Overwatch2DivisionOrder, Overwatch2Rank, Overwatch2Mark, Overwatch2Tier, Overwatch2Placement
from overwatch2.controller.serializers import DivisionSerializer, PlacementSerializer
from paypal.standard.forms import PayPalPaymentsForm
from overwatch2.controller.order_information import *
from accounts.models import TokenForPay, BaseOrder
from django.contrib.auth.decorators import login_required
from booster.models import OrderRating
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from accounts.models import BaseUser
from .utils import get_overwatch2_divisions_data, get_overwatch2_marks_data, get_overwatch2_placements_data



def get_overwatch2_divisions(request):
    divisions_data = get_overwatch2_divisions_data()
    return JsonResponse(divisions_data, safe=False)

def get_overwatch2_marks(request):
    marks_data = get_overwatch2_marks_data()
    return JsonResponse(marks_data, safe=False)

def get_overwatch2_placements(request):
    placements_data = get_overwatch2_placements_data()
    return JsonResponse(placements_data, safe=False)



def overwatch2GetBoosterByRank(request):
  order_get_rank_value = None
  extend_order = request.GET.get('extend')
  if extend_order:
    try:
      BaseOrder.objects.get(id = extend_order, customer= request.user)
      order_get_rank_value = Overwatch2DivisionOrder.objects.get(order_id=extend_order).get_rank_value()
    except Exception as e:
      print(e)
      return redirect('homepage.index')
  ranks = Overwatch2Rank.objects.all().order_by('id')
  divisions  = Overwatch2Tier.objects.all().order_by('id')
  marks = Overwatch2Mark.objects.all().order_by('id')
  placements = Overwatch2Placement.objects.all().order_by('id')

  divisions_data = [
    [division.from_V_to_IV ,division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_V_next]
    for division in divisions
  ]
  
  marks_data = [
    [mark.mark_1, mark.mark_2, mark.mark_3, mark.mark_4, mark.mark_5]
    for mark in marks
  ]
  placements_data = [
    placement.price
    for placement in placements
  ]

  with open('static/overwatch2/data/divisions_data.json', 'w') as json_file:
    json.dump(divisions_data, json_file)

  with open('static/overwatch2/data/marks_data.json', 'w') as json_file:
    json.dump(marks_data, json_file)

  with open('static/overwatch2/data/placements_data.json', 'w') as json_file:
    json.dump(placements_data, json_file)

  divisions_list = list(divisions.values())

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 12)

  game_pk_condition = Case(
    When(booster_orders__game__pk=12, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
  )
    
  boosters = BaseUser.objects.filter(
      is_booster = True,
      booster__is_overwatch2_player=True,
      booster__can_choose_me=True
      ).annotate(
      order_count=Sum(game_pk_condition)
      ).order_by('id')


  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "placements": placements,
    "order_get_rank_value":order_get_rank_value,
    "feedbacks": feedbacks,
    "boosters": boosters,
  }
  return render(request,'overwatch2/GetBoosterByRank.html', context)

# Paypal
@login_required
def view_that_asks_for_money(request):
  if request.method == 'POST' and request.user.is_authenticated :
    if request.user.is_booster:
      messages.error(request, "You are a booster!, You can't make order.")
      return redirect(reverse_lazy('overwatch2'))
    
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
      return render(request, "mobileLegends/paypal.html", context,status=200)
    
    for field, errors in serializer.errors.items():
      for error in errors:
        messages.error(request, f"{error}")
    return redirect(reverse_lazy('overwatch2'))
  
  return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)
