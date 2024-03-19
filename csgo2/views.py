from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from csgo2.models import Csgo2Rank, Csgo2Tier, Csgo2DivisionOrder, CsgoFaceitPrice, Csgo2PremierOrder, Csgo2PremierPrice
from csgo2.controller.serializers import *
from paypal.standard.forms import PayPalPaymentsForm
from csgo2.controller.order_information import *
from accounts.models import TokenForPay, BaseOrder
from django.contrib.auth.decorators import login_required
from booster.models import OrderRating

def csgo2GetBoosterByRank(request):
  order_get_rank_value = None
  extend_order = request.GET.get('extend')

  if extend_order:
    try:
      order = BaseOrder.objects.get(id = extend_order, customer= request.user)
      extend_order_type = order.game_type
      if extend_order_type == 'D':
        order_get_rank_value = Csgo2DivisionOrder.objects.get(order_id=extend_order).get_rank_value()
      elif extend_order_type == 'A':
        order_get_rank_value = Csgo2PremierOrder.objects.get(order_id=extend_order).get_rank_value()

    except Exception as e:
      print(e)
      return redirect('homepage.index')
    
  ranks = Csgo2Rank.objects.all().order_by('id')
  divisions  = Csgo2Tier.objects.all().order_by('id')

  divisions_data = [
    [division.from_I_to_I_next ]
    for division in divisions
  ]
  
  with open('static/csgo2/data/divisions_data.json', 'w') as json_file:
    json.dump(divisions_data, json_file)

  premier_row = Csgo2PremierPrice.objects.all().first()
  premier_prices = [premier_row.price_0_4999, premier_row.price_5000_7999, premier_row.price_8000_11999, premier_row.price_12000_18999, premier_row.price_19000_20999, premier_row.price_21000_24999, premier_row.price_25000_30000]
  
  with open('static/csgo2/data/premier_data.json', 'w') as json_file:
    json.dump(premier_prices, json_file)

  faceit_prices = CsgoFaceitPrice.objects.all().first()

  faceit_data = [
    0, faceit_prices.from_1_to_2, faceit_prices.from_2_to_3, faceit_prices.from_3_to_4, faceit_prices.from_4_to_5, faceit_prices.from_5_to_6, faceit_prices.from_6_to_7, faceit_prices.from_7_to_8, faceit_prices.from_8_to_9, faceit_prices.from_9_to_10
  ]

  with open('static/csgo2/data/faceit_data.json', 'w') as json_file:
    json.dump(faceit_data, json_file)

  divisions_list = list(divisions.values())

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 12)

  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "order_get_rank_value": order_get_rank_value,
    "premier_prices": premier_prices,
    "faceit_prices": faceit_data,
    "feedbacks": feedbacks
  }
  return render(request,'csgo2/GetBoosterByRank.html', context)

# Paypal
@login_required
def pay_with_paypal(request):
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('overwatch2'))
    try:
      # Division
      if request.POST.get('game_type') == 'D':
        serializer = DivisionSerializer(data=request.POST)
      # Premier
      elif request.POST.get('game_type') == 'A':
        serializer = PremierSerializer(data=request.POST)
      # Faceit
      elif request.POST.get('game_type') == 'F':
        serializer = FaceitSerializer(data=request.POST)

      if serializer.is_valid():
        extend_order_id = serializer.validated_data['extend_order']
        # Division
        if request.POST.get('game_type') == 'D':
          order_info = get_division_order_result_by_rank(serializer.validated_data,extend_order_id)
        # Premier
        if request.POST.get('game_type') == 'A':
          order_info = get_premier_order_result_by_rank(serializer.validated_data,extend_order_id)
        # Faceit
        elif request.POST.get('game_type') == 'F':
          order_info = get_faceit_order_result_by_rank(serializer.validated_data,extend_order_id)

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
      return JsonResponse({'error': serializer.errors}, status=400)
      # messages.error(request, 'Ensure this value is greater than or equal to 10')
      # return redirect(reverse_lazy('csgo2'))
    except Exception as e:
      return JsonResponse({'error': f'Error processing form data: {str(e)}'}, status=400)

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