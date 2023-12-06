from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseBadRequest
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from wildRift.models import WildRiftRank, WildRiftTier, WildRiftMark, WildRiftPlacement, WildRiftDivisionOrder, WildRiftPlacementOrder
import json
import uuid
from django.forms.models import model_to_dict
from .serializers import RankSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received
from django.contrib.auth import get_user_model
User = get_user_model()
# from .models import Buyer 


division_names = ['','IV','III','II','I']  
rank_names = ['', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD', 'DIAMOND', 'MASTER']

def get_order_result_by_rank(data):
    current_rank = data['current_rank']
    current_division = data['current_division']
    marks = data['marks']
    desired_rank = data['desired_rank']
    desired_division = data['desired_division']
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

    name = f'WILD RIFT, BOOSTING FROM {rank_names[current_rank]} {division_names[current_division]} MARKS {marks} TO {rank_names[desired_rank]} {division_names[desired_division]}'

    return({'name':name,'price':price})


@csrf_exempt
def wildRiftGetBoosterByRank(request):
    ranks = WildRiftRank.objects.all()
    divisions  = WildRiftTier.objects.all().order_by('id')
    marks = WildRiftMark.objects.all().order_by('id')
    placements = WildRiftPlacement.objects.all().order_by('id')

    divisions_data = [
        [division.from_IV_to_III] if division.rank.rank_name == 'master' else
        [division.from_IV_to_III, division.from_III_to_II, division.from_II_to_II, division.from_I_to_IV_next]
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
        "placements": placements
    }
    return render(request,'wildRift/GetBoosterByRank.html', context)



def wildRiftOrders(request):
    divisions_order = WildRiftDivisionOrder.objects.filter(booster__isnull=True)
    placements_order = WildRiftPlacementOrder.objects.filter(booster__isnull=True)

    context = {
        "divisions_order": divisions_order,
        "placements_order": placements_order
    }
    return render(request,'wildRift/Orders.html', context)

def wildRiftOrderChat(request, order_type, id):
    if order_type == 'division':
        order = get_object_or_404(WildRiftDivisionOrder, id=id)
    elif order_type == 'placement':
        order = get_object_or_404(WildRiftPlacementOrder, id=id)
    else:
        return HttpResponseBadRequest("Invalid Order Type")
    
    try:
        order.booster = request.user
        order.save()
    except Exception as e:
        print(f"Error updating order: {e}")
        return HttpResponseBadRequest("Error updating order")
    
    context = {
        'order_type': order_type,
        'order': order
    }

    return render(request, 'wildRift/Chat.html', context)



@csrf_exempt
def view_that_asks_for_money(request):
    if request.method == 'POST':
        try:
            serializer = RankSerializer(data=request.POST)
            if serializer.is_valid():
                data = serializer.validated_data
                order_info = get_order_result_by_rank(data)
                dynamic_invoice = str(uuid.uuid4())
                paypal_dict = {
                    "business": settings.PAYPAL_EMAIL,
                    "amount": order_info['price'],
                    "item_name": order_info['name'],
                    "invoice": dynamic_invoice,
                    "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                    "return": request.build_absolute_uri(reverse('wildrift.payment.success')),
                    "cancel_return": request.build_absolute_uri(reverse('wildrift.payment.canceled')),
                }
                # Create the instance.
                form = PayPalPaymentsForm(initial=paypal_dict)
                context = {"form": form}
                print(f'order {dynamic_invoice} : {order_info}')

                # buyer = Buyer.objects.create(
                #     invoice=dynamic_invoice,
                #     name=order_info['name'],  # Replace with actual field names
                #     price=order_info['price'],  # Replace with actual field names
                #     # Add other fields as needed...
                # )
                return render(request, "wildRift/paypal.html", context,status=200)
            return JsonResponse({'error': serializer.errors}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error processing form data: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)



def payment_successed(request):
    payer_id = request.GET.get('PayerID')
    print(payer_id)
    return HttpResponse(f'payment Success with payer ID : {payer_id}')
    # return redirect(reverse('accounts.register'))

def payment_canceled(request):
    return HttpResponse('payment canceled')


def create_user_account(payer_id, payer_email, buyer_first_name, buyer_last_name):
    # Check if a user with the same payer_id already exists
    user = User.objects.filter(username=payer_id).first()

    # If not, create a new user account
    if not user:
        user = User.objects.create_user(username=payer_id, email=payer_email, password='iti123456', first_name=buyer_first_name,
        last_name=buyer_last_name,)
        print(f'user created with, {user}')

    return HttpResponse(f'you have account with you trnaction id username {payer_id} and name {buyer_first_name}')


@csrf_exempt
def paypal_ipn_listener(sender, **kwargs):
    ipn_obj = sender

    # Check if the payment is completed
    if ipn_obj.payment_status == "Completed":

        payer_id = ipn_obj.payer_id
        payer_email = ipn_obj.payer_email
        
        print(f"Transaction ID: {ipn_obj.txn_id}")
        print(f"Payer ID: {ipn_obj.payer_id}")
        print(f"Payer Email: {ipn_obj.payer_email}")
        print(f"Payment Status: {ipn_obj.payment_status}")
        print(f"Gross Amount: {ipn_obj.mc_gross}")
        print(f"Currency: {ipn_obj.mc_currency}")
        print(f"Item Name: {ipn_obj.item_name}")
        print(f"Invoice ID: {ipn_obj.invoice}")
        print(f"Custom Field: {ipn_obj.custom}")
        print(f"Receiver Email: {ipn_obj.receiver_email}")
        print(f"Is Test IPN: {ipn_obj.test_ipn}")
        buyer_first_name = ipn_obj.first_name
        buyer_last_name = ipn_obj.last_name

        # create a user account
        create_user_account(payer_id, payer_email, buyer_first_name, buyer_last_name)

# Connect the signal to your IPN listener
valid_ipn_received.connect(paypal_ipn_listener)