from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from wildRift.models import *
import json
from wildRift.controller.serializers import RankSerializer
from customer.models import Champion
from wildRift.controller.order_information import *
from booster.models import OrderRating
from accounts.models import TokenForPay
from django.db.models import Count, Sum, Case, When, FloatField, F, Q, Avg, IntegerField
from django.db.models.functions import Coalesce
from accounts.models import BaseUser
from .utils import get_wildrift_divisions_data, get_wildrift_marks_data
from gameBoosterss.utils import mainPayment

def get_wildrift_divisions_data_view(request):
    divisions_data = get_wildrift_divisions_data()
    return JsonResponse(divisions_data, safe=False)

def get_wildrift_marks_data_view(request):
    marks_data = get_wildrift_marks_data()
    return JsonResponse(marks_data, safe=False)



def wildRiftGetBoosterByRank(request):
    extend_order = request.GET.get('extend')
    try:
        order = WildRiftDivisionOrder.objects.get(order_id=extend_order)
    except:
        order = None
    ranks = WildRiftRank.objects.all().order_by('id')
    divisions  = WildRiftTier.objects.all().order_by('id')
    champions = Champion.objects.filter(game__id =1).order_by('id')

    game_pk_condition = Case(
        When(booster_orders__game__pk=1, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
        default=0,
        output_field=IntegerField()
    )

    boosters = BaseUser.objects.filter(
        is_booster=True,
        booster__is_wr_player=True,
        booster__can_choose_me=True
    ).annotate(
        order_count=Sum(game_pk_condition)
    ).order_by('id')

    divisions_list = list(divisions.values())

    # Feedbacks
    feedbacks = OrderRating.objects.filter(order__game_id = 1)
    context = {
        "ranks": ranks,
        "divisions": divisions_list,
        "order": order,
        "feedbacks": feedbacks,
        'champions' : champions,
        'boosters': boosters,
    }
    return render(request,'wildRift/GetBoosterByRank.html', context)

@login_required
def pay_with_paypal(request):
    if request.method == 'POST' and request.user.is_authenticated:
        if request.user.is_booster:
            messages.error(request, "You are a booster!, You can't make order.")
            return redirect(reverse_lazy('wildRift'))
        
        serializer = RankSerializer(data=request.POST) 
        if serializer.is_valid():
            extend_order_id = serializer.validated_data['extend_order']
            
            order_info = get_order_result_by_rank(serializer.validated_data,extend_order_id)
            request.session['invoice'] = order_info['invoice']
            token = TokenForPay.create_token_for_pay(request.user,  order_info['invoice'])

            payment = mainPayment(order_info, request, token)
            if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = str(link.href)
                        return redirect(approval_url)
            else:
                messages.error(request, "There was an issue connecting to PayPal. Please try again later.")
                return redirect(reverse_lazy('wildRift'))
        
        for field, errors in serializer.errors.items():
            for error in errors:
                messages.error(request, f"{error}")
        return redirect(reverse_lazy('wildRift'))
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