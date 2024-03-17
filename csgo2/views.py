from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from csgo2.models import Csgo2Rank, Csgo2Tier, Csgo2DivisionOrder, Csgo2Mark
from csgo2.controller.serializers import DivisionSerializer
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
      BaseOrder.objects.get(id = extend_order, customer= request.user)
      order_get_rank_value = Csgo2DivisionOrder.objects.get(order_id=extend_order).get_rank_value()
    except Exception as e:
      print(e)
      return redirect('homepage.index')
  ranks = Csgo2Rank.objects.all().order_by('id')
  divisions  = Csgo2Tier.objects.all().order_by('id')
  marks = Csgo2Mark.objects.all().order_by('id')

  divisions_data = [
    [division.from_I_to_I_next ]
    for division in divisions
  ]
  
  with open('static/csgo2/data/divisions_data.json', 'w') as json_file:
    json.dump(divisions_data, json_file)



  divisions_list = list(divisions.values())

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 12)

  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "order_get_rank_value":order_get_rank_value,
    "feedbacks": feedbacks
  }
  return render(request,'csgo2/GetBoosterByRank.html', context)

# Paypal
@login_required
def view_that_asks_for_money(request):
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('overwatch2'))
    try:
      # Division
      if request.POST.get('game_type') == 'D':
        serializer = DivisionSerializer(data=request.POST)
    #   # Placement
    #   elif request.POST.get('game_type') == 'P':
    #     serializer = PlacementSerializer(data=request.POST)

      if serializer.is_valid():
        extend_order_id = serializer.validated_data['extend_order']
        # Division
        if request.POST.get('game_type') == 'D':
          order_info = get_division_order_result_by_rank(serializer.validated_data,extend_order_id)
        # Placement
        # elif request.POST.get('game_type') == 'P':
        #   order_info = get_palcement_order_result_by_rank(serializer.validated_data,extend_order_id)

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
      # return JsonResponse({'error': serializer.errors}, status=400)
      messages.error(request, 'Ensure this value is greater than or equal to 10')
      return redirect(reverse_lazy('csg2'))
    except Exception as e:
      return JsonResponse({'error': f'Error processing form data: {str(e)}'}, status=400)

  return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)
