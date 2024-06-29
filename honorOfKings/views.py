from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from honorOfKings.models import *
from honorOfKings.controller.serializers import DivisionSerializer
from paypal.standard.forms import PayPalPaymentsForm
from honorOfKings.controller.order_information import *
from booster.models import OrderRating
from accounts.models import TokenForPay
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from accounts.models import BaseUser
from honorOfKings.utils import get_hok_divisions_data, get_hok_marks_data


def get_hok_divisions_data_view(request):
    divisions_data = get_hok_divisions_data()
    return JsonResponse(divisions_data, safe=False)

def get_hok_marks_data_view(request):
    marks_data = get_hok_marks_data()
    return JsonResponse(marks_data, safe=False)


def honerOfKingeGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = HonorOfKingsDivisionOrder.objects.get(order_id=extend_order)
  except:
    order = None
  ranks = HonorOfKingsRank.objects.all().order_by('id')
  divisions  = HonorOfKingsTier.objects.all().order_by('id')
  divisions_list = list(divisions.values())

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 11)
  game_pk_condition = Case(
    When(booster_orders__game__pk=11, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
  )
    
  boosters = BaseUser.objects.filter(
      is_booster = True,
      booster__is_hok_player=True,
      booster__can_choose_me=True
      ).annotate(
      order_count=Sum(game_pk_condition)
      ).order_by('id')
  
  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "order":order,
    "feedbacks": feedbacks,
    "boosters": boosters,
  }
  return render(request,'honorOfKings/GetBoosterByRank.html', context)

# Paypal
@login_required
def pay_with_paypal(request):
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('hok'))
      
    print('request POST:  ', request.POST)
    serializer = DivisionSerializer(data=request.POST)

    if serializer.is_valid():
      extend_order_id = serializer.validated_data['extend_order']
    
      order_info = get_division_order_result_by_rank(serializer.validated_data,extend_order_id)
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
          messages.error(request, f"{error}")
    return redirect(reverse_lazy('hok'))

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