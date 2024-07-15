from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.conf import settings
from WorldOfWarcraft.models import *
from WorldOfWarcraft.controller.serializers import ArenaSerializer, RaidSimpleSerializer, RaidBundleSerializer
from WorldOfWarcraft.controller.order_information import get_arena_order_result_by_rank, get_raid_simple_price_by_bosses
from booster.models import OrderRating
from django.db.models import Sum, Case, When, IntegerField
from accounts.models import TokenForPay, BaseUser
from gameBoosterss.utils import mainPayment

def get_wow_prices_data_view(request):
    prices = WorldOfWarcraftRpsPrice.objects.all().first()
    prices_data = [prices.price_of_2vs2, prices.price_of_3vs3]
    return JsonResponse(prices_data, safe=False)


def wowGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = WorldOfWarcraftArenaBoostOrder.objects.get(order_id=extend_order)
  except:
    order = None

  prices = WorldOfWarcraftRpsPrice.objects.all().first()

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 6)
  
  game_pk_condition = Case(
    When(booster_orders__game__pk=6, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
    )
    
  boosters = BaseUser.objects.filter(
    is_booster = True,
    booster__is_wow_player=True,
    booster__can_choose_me=True
    ).annotate(
    order_count=Sum(game_pk_condition)
    ).order_by('id')
  

  bosses = WorldOfWarcraftBoss.objects.all()
  bundles = WorldOfWarcraftBundle.objects.all()
  
  context = {
    # "ranks": ranks,
    "order": order,
    "feedbacks": feedbacks,
    "rp2vs2": prices.price_of_2vs2,
    "rp3vs3": prices.price_of_3vs3,
    "boosters": boosters,
    "bosses": bosses,
    "bundles": bundles,
  }
  return render(request,'wow/GetBoosterByRank.html', context)


# Paypal
@login_required
def pay_with_paypal(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)

    if request.user.is_booster:
        messages.error(request, "You are a booster! You can't make an order.")
        return redirect(reverse_lazy('wow'))

    if request.POST.get('game_type') == 'R':
        serializer = RaidSimpleSerializer(data=request.POST)
    elif request.POST.get('game_type') == 'A':
        serializer = ArenaSerializer(data=request.POST)
    elif request.POST.get('game_type') == 'RB':
        serializer = RaidBundleSerializer(data=request.POST)    

    if not serializer.is_valid():
        for field, errors in serializer.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
        return redirect(reverse_lazy('wow'))
    print("serializer valid", serializer.validated_data)
    # return HttpResponse({
    #     'success': True,
    #     "data": serializer.validated_data
    # })
    if request.POST.get('game_type') == 'A':
      extend_order_id = serializer.validated_data.get('extend_order')
      order_info = get_arena_order_result_by_rank(serializer.validated_data, extend_order_id)
    elif request.POST.get('game_type') == 'R':
      order_info = get_raid_simple_price_by_bosses(serializer.validated_data)  
    elif request.POST.get('game_type') == 'RB':
      # order_info = get_raid_simple_price_by_bosses(serializer.validated_data)  
      raise NotImplementedError

    if not order_info:
        messages.error(request, "Order information could not be retrieved.")
        return redirect(reverse_lazy('wow'))
    
    token = TokenForPay.create_token_for_pay(request.user,  order_info['invoice'])
    payment = mainPayment(order_info, request, token)

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                return redirect(approval_url)
    else:
        messages.error(request, "There was an issue connecting to PayPal. Please try again later.")
        return redirect(reverse_lazy('wow'))

# Cryptomus
@login_required
def pay_with_cryptomus(request):
  if request.method == 'POST':
    context = {
      "data": request.POST
    }
    return render(request, "accounts/cryptomus.html", context,status=200)
  return render(request, "accounts/cryptomus.html", context={"data": "There is error"},status=400)