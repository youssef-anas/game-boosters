from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseBadRequest
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from paypal.standard.forms import PayPalPaymentsForm
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from wildRift.models import WildRiftRank, WildRiftTier, WildRiftMark, WildRiftPlacement, WildRiftDivisionOrder
import json
import uuid
from django.forms.models import model_to_dict
from .serializers import RankSerializer
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import BaseOrder
from accounts.models import BaseOrder, Room, Message, BoosterPercent

User = get_user_model()

division_names = ['','IV','III','II','I']  
rank_names = ['', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD', 'DIAMOND', 'MASTER']

def get_order_result_by_rank(data,extend_order_id):
    print('Data: ', data)
    current_rank = data['current_rank']
    current_division = data['current_division']
    marks = data['marks']
    desired_rank = data['desired_rank']
    desired_division = data['desired_division']
    total_percent = 0
    duo_boosting = data['duo_boosting']
    select_booster = data['select_booster']
    turbo_boost = data['turbo_boost']
    streaming = data['streaming']

    duo_boosting_value = 0
    select_booster_value = 0
    turbo_boost_value = 0
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

    if turbo_boost:
        total_percent += 0.20
        boost_options.append('TURBO BOOSTING')
        turbo_boost_value = 1
    if streaming:
        total_percent += 0.15
        boost_options.append('STREAMING')
        streaming_value = 1

    # Read data from JSON file
    with open('static/wildRift/data/divisions_data.json', 'r') as file:
        division_price = json.load(file)
        flattened_data = [item for sublist in division_price for item in sublist]
        flattened_data.insert(0,0)
    ##
    with open('static/wildRift/data/marks_data.json', 'r') as file:
        marks_data = json.load(file)
        marks_data.insert(0,[0,0,0,0,0,0,0])
    ##    
    start_division = ((current_rank-1)*4) + current_division
    end_division = ((desired_rank-1)*4)+ desired_division
    marks_price = marks_data[current_rank][marks]
    sublist = flattened_data[start_division:end_division ]
    total_sum = sum(sublist)
    price = total_sum - marks_price
    price += (price * total_percent)
    price = round(price, 2)
    if extend_order_id > 0:
        try:
            # get extend order 
            extend_order = BaseOrder.objects.get(id=extend_order_id)
            extend_order_price = extend_order.price
            price = round((price - extend_order_price), 2)
        except: ####
            pass
    booster_id = data['choose_booster']
    if booster_id > 0 :
       get_object_or_404(User,id=booster_id,is_booster=True)
    else:
        booster_id = 0
    #####################################
    invoice = f'wr-1-D-{current_rank}-{current_division}-{marks}-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{price}-{extend_order_id}-{timezone.now()}'
    invoice_with_timestamp = str(invoice)
    boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
    name = f'WILD RIFT, BOOSTING FROM {rank_names[current_rank]} {division_names[current_division]} MARKS {marks} TO {rank_names[desired_rank]} {division_names[desired_division]}{boost_string}'

    return({'name':name,'price':price,'invoice':invoice_with_timestamp})

@csrf_exempt
def wildRiftGetBoosterByRank(request):
    extend_order = request.GET.get('extend')
    try:
        order = WildRiftDivisionOrder.objects.get(order_id=extend_order)
    except:
        order = None
    ranks = WildRiftRank.objects.all().order_by('id')
    divisions  = WildRiftTier.objects.all().order_by('id')
    marks = WildRiftMark.objects.all().order_by('id')
    placements = WildRiftPlacement.objects.all().order_by('id')

    divisions_data = [
        [division.from_IV_to_III] if division.rank.rank_name == 'master' else
        [division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_IV_next]
        for division in divisions
    ]

    marks_data = [
        [0,mark.mark_1, mark.mark_2, mark.mark_3, mark.mark_4, mark.mark_5]
        for mark in marks
    ]

    with open('static/wildRift/data/divisions_data.json', 'w') as json_file:
        json.dump(divisions_data, json_file)

    with open('static/wildRift/data/marks_data.json', 'w') as json_file:
        json.dump(marks_data, json_file)

    divisions_list = list(divisions.values())
    context = {
        "ranks": ranks,
        "divisions": divisions_list,
        "placements": placements,
        "order":order,
    }
    return render(request,'wildRift/GetBoosterByRank.html', context)

@csrf_exempt
def view_that_asks_for_money(request):
    if request.method == 'POST':
        if request.user.is_authenticated :
            if request.user.is_booster:
                messages.error(request, "You are a booster!, You can't make order.")
                return redirect(reverse_lazy('wildrift'))
        
        print('request POST:  ', request.POST)
        try:
            serializer = RankSerializer(data=request.POST) 
            print('request POST', request.POST)
            if serializer.is_valid():
                extend_order_id = serializer.validated_data['extend_order']
                print(extend_order_id)
                order_info = get_order_result_by_rank(serializer.validated_data,extend_order_id)
                request.session['invoice'] = order_info['invoice']

                paypal_dict = {
                    "business": settings.PAYPAL_EMAIL,
                    "amount": order_info['price'],
                    "item_name": order_info['name'],
                    "invoice": order_info['invoice'],
                    "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                    "return": request.build_absolute_uri(f"/accounts/register/"),
                    "cancel_return": request.build_absolute_uri(f"/wildRift/payment-canceled/"),
                }
                # Create the instance.
                form = PayPalPaymentsForm(initial=paypal_dict)
                context = {"form": form}
                return render(request, "wildRift/paypal.html", context,status=200)
            # return JsonResponse({'error': serializer.errors}, status=400)
            messages.error(request, 'Ensure this value is greater than or equal to 10')
            return redirect(reverse_lazy('wildrift'))
        except Exception as e:
            return JsonResponse({'error': f'Error processing form data: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)

def payment_canceled(request):
    return HttpResponse('payment canceled')
