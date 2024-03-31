from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from paypal.standard.forms import PayPalPaymentsForm
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from wildRift.models import *
import json
from wildRift.controller.serializers import RankSerializer
from customer.models import Champion
from wildRift.controller.order_information import *
from booster.models import OrderRating
from accounts.models import TokenForPay
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from accounts.models import BaseUser


def wildRiftGetBoosterByRank(request):
    extend_order = request.GET.get('extend')
    try:
        order = WildRiftDivisionOrder.objects.get(order_id=extend_order)
    except:
        order = None
    ranks = WildRiftRank.objects.all().order_by('id')
    divisions  = WildRiftTier.objects.all().order_by('id')
    marks = WildRiftMark.objects.all().order_by('id')
    champions = Champion.objects.filter(game__id =1).order_by('id')

    game_pk_condition = Case(
        When(booster_division__game__pk=1, then=1),
    default=0,
    output_field=IntegerField()
    )
    
    boosters = BaseUser.objects.filter(
        is_booster = True,
        booster__is_wf_player=True,
        booster__can_choose_me=True
        ).annotate(
        average_rating=Coalesce(Avg('ratings_received__rate'), Value(0.0)),
        order_count=Sum(game_pk_condition)
        ).order_by('id')


    divisions_data = [
        [division.from_IV_to_III] if division.rank.rank_name == 'master' else
        [division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_IV_next]
        for division in divisions
    ]

    marks_data = [
        [0,mark.mark_1, mark.mark_2, mark.mark_3, mark.mark_4, mark.mark_5, mark.mark_6]
        for mark in marks
    ]

    with open('static/wildRift/data/divisions_data.json', 'w') as json_file:
        json.dump(divisions_data, json_file)

    with open('static/wildRift/data/marks_data.json', 'w') as json_file:
        json.dump(marks_data, json_file)

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

            paypal_dict = {
                "business": settings.PAYPAL_EMAIL,
                "amount": order_info['price'],
                "item_name": order_info['name'],
                "invoice": order_info['invoice'],
                "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                "return": request.build_absolute_uri(f"/customer/payment-success/{token}/"),
                "cancel_return": request.build_absolute_uri(f"/customer/payment-canceled/{token}/"),
            }
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