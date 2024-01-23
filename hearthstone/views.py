from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from hearthstone.models import *
from hearthstone.serializers import DivisionSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
User = get_user_model()

division_names = ['','X','IX','VIII','VII','VI','V','IV','III','II','I']
rank_names = ['UNRANK', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'LEGEND']

def get_division_order_result_by_rank(data,extend_order_id):
  print('Data: ', data)
  # Division
  current_rank = data['current_rank']
  current_division = data['current_division']
  marks = data['marks']
  desired_rank = data['desired_rank']
  desired_division = data['desired_division']

  total_percent = 0
  duo_boosting = data['duo_boosting']
  select_booster = data['select_booster']
  speed_up_boost = data['speed_up_boost']
  choose_legends = data['choose_legends']
  streaming = data['streaming']

  duo_boosting_value = 0
  select_booster_value = 0
  speed_up_boost_value = 0
  choose_legends_value = 0
  streaming_value = 0

  boost_options = []

  if duo_boosting:
    total_percent += 0.65
    boost_options.append('DUO BOOSTING')
    duo_boosting_value = 1

  if select_booster:
    total_percent += 0.05
    boost_options.append('SELECT BOOSTING')
    select_booster_value = 1

  if speed_up_boost:
    total_percent += 0.20
    boost_options.append('SPEED UP BOOST')
    speed_up_boost_value = 1
  
  if streaming:
    total_percent += 0.15
    boost_options.append('STREAMING')
    streaming_value = 1

  if choose_legends:
    total_percent += 0.0
    boost_options.append('CHOOSE LEGENDS')
    choose_legends_value = 1

  # Read data from JSON file
  with open('static/hearthstone/data/divisions_data.json', 'r') as file:
    division_price = json.load(file)
    flattened_data = [item for sublist in division_price for item in sublist]
    flattened_data.insert(0,0)
  ##
  with open('static/hearthstone/data/marks_data.json', 'r') as file:
    marks_data = json.load(file)
    marks_data.insert(0,[0,0,0])
  ##    
  start_division = ((current_rank-1) * 10) + current_division
  end_division = ((desired_rank-1) * 10)+ desired_division
  marks_price = marks_data[current_rank][marks]
  sublist = flattened_data[start_division:end_division ]
  total_sum = sum(sublist)
  price = total_sum - marks_price
  price += (price * total_percent)
  price = round(price, 2)
  print('Price', price)

  if extend_order_id > 0:
    try:
      extend_order = BaseOrder.objects.get(id=extend_order_id)
      extend_order_price = extend_order.price
      price = round((price - extend_order_price), 2)
      print('Price', price)
    except:
      pass

  booster_id = data['choose_booster']
  if booster_id > 0 :
    get_object_or_404(User,id=booster_id,is_booster=True)
  else:
    booster_id = 0

  invoice = f'hearthstone-7-D-{current_rank}-{current_division}-{marks}-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-0-{streaming_value}-{booster_id}-{price}-{extend_order_id}-{choose_legends_value}-{speed_up_boost_value}-{timezone.now()}'
  print('Invoice', invoice)

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'HEARTHSTONE, BOOSTING FROM {rank_names[current_rank]} {division_names[current_division]} MARKS {marks} TO {rank_names[desired_rank]} {division_names[desired_division]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

# Create your views here.
@csrf_exempt
def hearthstoneGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = HearthstoneDivisionOrder.objects.get(order_id=extend_order)
  except:
    order = None
  ranks = HearthstoneRank.objects.all().order_by('id')
  divisions  = HearthstoneTier.objects.all().order_by('id')
  marks = HearthstoneMark.objects.all().order_by('id')

  divisions_data = [
    [division.from_X_to_IX, division.from_IX_to_VIII, division.from_VIII_to_VII, division.from_VII_to_VI, division.from_VI_to_V, division.from_V_to_IV, division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_IV_next]
    for division in divisions
  ]

  marks_data = [
    [mark.marks_3, mark.marks_2, mark.marks_1]
    for mark in marks
  ]

  with open('static/hearthstone/data/divisions_data.json', 'w') as json_file:
    json.dump(divisions_data, json_file)

  with open('static/hearthstone/data/marks_data.json', 'w') as json_file:
    json.dump(marks_data, json_file)

  divisions_list = list(divisions.values())
  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "order":order,
  }
  return render(request,'hearthstone/GetBoosterByRank.html', context)

# Paypal
@csrf_exempt
def view_that_asks_for_money(request):
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('hearthstone'))
      
    print('request POST:  ', request.POST)
    try:
      # Division
      if request.POST.get('game_type') == 'D':
        serializer = DivisionSerializer(data=request.POST)

      if serializer.is_valid():
        extend_order_id = serializer.validated_data['extend_order']
        # Division
        if request.POST.get('game_type') == 'D':
          order_info = get_division_order_result_by_rank(serializer.validated_data,extend_order_id)
          print('Order Info: ', order_info)

        request.session['invoice'] = order_info['invoice']

        paypal_dict = {
          "business": settings.PAYPAL_EMAIL,
          "amount": order_info['price'],
          "item_name": order_info['name'],
          "invoice": order_info['invoice'],
          "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
          "return": request.build_absolute_uri(f"/accounts/register/"),
          "cancel_return": request.build_absolute_uri(f"/hearthstone/payment-canceled/"),
        }
        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form}
        return render(request, "hearthstone/paypal.html", context,status=200)
      # return JsonResponse({'error': serializer.errors}, status=400)
      messages.error(request, 'Ensure this value is greater than or equal to 10')
      return redirect(reverse_lazy('hearthstone'))
    except Exception as e:
      return JsonResponse({'error': f'Error processing form data: {str(e)}'}, status=400)

  return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)

# Cancel Payment
def payment_canceled(request):
  return HttpResponse('payment canceled')