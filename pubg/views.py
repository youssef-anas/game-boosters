from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from pubg.models import *
from pubg.controller.serializers import DivisionSerializer
from paypal.standard.forms import PayPalPaymentsForm
from pubg.controller.order_information import *
from accounts.models import TokenForPay
from django.contrib.auth.decorators import login_required
from booster.models import OrderRating
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from accounts.models import BaseUser
from pubg.utils import get_divisions_data, get_marks_data


def get_divisions_data_view(request):
    return JsonResponse(get_divisions_data(), safe=False)

def get_marks_data_view(request):
    return JsonResponse(get_marks_data(), safe=False)



def pubgGetBoosterByRank(request):
    extend_order = request.GET.get('extend')
    try:
        order_get_rank_value = PubgDivisionOrder.objects.get(order_id=extend_order).get_rank_value()
    except PubgDivisionOrder.DoesNotExist:
        order_get_rank_value = None

    ranks = PubgRank.objects.all().order_by('id')
    divisions = PubgTier.objects.all().order_by('id')
    divisions_list = list(divisions.values())
    
    # Feedbacks
    feedbacks = OrderRating.objects.filter(order__game_id = 3)
    game_pk_condition = Case(
      When(booster_orders__game__pk=3, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
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
      "order_get_rank_value": order_get_rank_value,
      "feedbacks": feedbacks,
      "boosters": boosters,
    }
    return render(request,'pubg/GetBoosterByRank.html', context)


# Paypal
@login_required
def view_that_asks_for_money(request):
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('pubg'))
      
    print('request POST:  ', request.POST)
    # try:
      # Division
    serializer = DivisionSerializer(data=request.POST)
    extend_order = request.POST.get('extend_order', '')
    if serializer.is_valid():
      extend_order_id = serializer.validated_data['extend_order']
      # Division
      order_info = get_division_order_result_by_rank(serializer.validated_data,extend_order_id)

      request.session['invoice'] = order_info['invoice']
      token = TokenForPay.create_token_for_pay(request.user,  order_info['invoice'])

      if request.user.is_superuser:
        # return request.build_absolute_uri(f"/customer/payment-success/{token}/"),
        return redirect(request.build_absolute_uri(f"/customer/payment-success/{token}/"))

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
    
    scheme = request.scheme
    host = request.get_host()
    full_url = f"{scheme}://{host}/pubg?extend={extend_order}"

    print(full_url)      

    return redirect(full_url)
  return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)