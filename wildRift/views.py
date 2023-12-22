from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseBadRequest
from django.urls import reverse, reverse_lazy
from django.contrib import messages
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
from django.utils import timezone
from chat.models import Room, Message
from accounts.models import BaseOrder

User = get_user_model()

division_names = ['','IV','III','II','I']  
rank_names = ['', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD', 'DIAMOND', 'MASTER']

def get_order_result_by_rank(data):
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


    booster_id = data['choose_booster']
    if booster_id > 0 :
        booster = get_object_or_404(User,id=booster_id,is_booster=True)
        booster_id = booster.id
    else:
        booster_id = 0
    #####################################
    invoice = f'wr-1-{current_rank}-{current_division}-{marks}-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{price}-{timezone.now()}'
    invoice_with_timestamp = str(invoice)
    boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
    name = f'WILD RIFT, BOOSTING FROM {rank_names[current_rank]} {division_names[current_division]} MARKS {marks} TO {rank_names[desired_rank]} {division_names[desired_division]}{boost_string}'

    return({'name':name,'price':price,'invoice':invoice_with_timestamp})


@csrf_exempt
def wildRiftGetBoosterByRank(request):
    ranks = WildRiftRank.objects.all().order_by('id')
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


# Chat with user
def create_chat_with_user(user,booster):
    isRoomExist = Room.get_specific_room(user,booster)
    if not isRoomExist:
        return Room.create_room_with_booster(user,booster)
    else:
        return isRoomExist
    
def wildRiftOrders(request):
    divisions_order = WildRiftDivisionOrder.objects.filter(order__booster__isnull=True)
    placements_order = WildRiftPlacementOrder.objects.filter(booster__isnull=True)

    context = {
        "divisions_order": divisions_order,
        "placements_order": placements_order
    }
    return render(request,'wildRift/Orders.html', context)

def get_latest_price(request):
    order_id = request.GET.get('order_id')
    order = BaseOrder.objects.filter(id=order_id, booster__isnull=True).first()

    if order:
        order.update_actual_price()
        order.save()
        latest_price = order.actual_price
        return JsonResponse({'actual_price': latest_price})
    else:
        return JsonResponse({'error': 'Order not found'}, status=404)



def wildRiftOrderChat(request, order_type, id):
    # Check if Booster Have Less Than 3 Orders ?  -----
    if order_type == 'division':
        base_order = get_object_or_404(BaseOrder, id=id)
        order = get_object_or_404(WildRiftDivisionOrder, order=base_order)
    elif order_type == 'placement':
        order = get_object_or_404(WildRiftPlacementOrder, id=id)
    else:
        return HttpResponseBadRequest("Invalid Order Type")
    
    try:
        order.booster = request.user
        order.save()
        create_chat_with_user(order.customer,request.user)
    except Exception as e:
        print(f"Error updating order: {e}")
        return HttpResponseBadRequest("Error updating order")

    return redirect(reverse_lazy('booster.orders'))



@csrf_exempt
def view_that_asks_for_money(request):
    if request.method == 'POST':
        if request.user.is_authenticated :
            if request.user.is_booster:
                messages.error(request, "You are a booster!, You can't make order.")
                return redirect(reverse_lazy('wildrift'))
        
            user_has_uncompleted_order = BaseOrder.objects.filter(customer=request.user, is_done=False).exists()
            if user_has_uncompleted_order:
                messages.error(request, "You already have a uncompleted order!, You can't make another one until this finish")
                return redirect(reverse_lazy('wildrift'))
        
        print('request POST:  ', request.POST)
        try:
            serializer = RankSerializer(data=request.POST)
            print('request POST', request.POST)
            if serializer.is_valid():

                order_info = get_order_result_by_rank(serializer.validated_data)
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
                print(f'order {order_info["invoice"]} : {order_info}')
                return render(request, "wildRift/paypal.html", context,status=200)
            # return JsonResponse({'error': serializer.errors}, status=400)
            messages.error(request, 'Ensure this value is greater than or equal to 10')
            return redirect(reverse_lazy('wildrift'))
        except Exception as e:
            return JsonResponse({'error': f'Error processing form data: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)



# def payment_successed(request):
#     payer_id = request.GET.get('PayerID')
#     order_id = request.GET.get('order_id')
#     # Use the parameters as needed
#     print(f'Payment success with payer ID: {payer_id}')
    
#     # Perform additional actions, such as updating the order status, generating an invoice, etc.

#     # Redirect to a relevant page, e.g., the account registration page
#     return redirect(reverse('accounts.register'))
#     return HttpResponse(f'order id: {order_id} ---- payer_id {payer_id}')

def payment_canceled(request):
    order_id = request.GET.get('order_id')
    order = WildRiftDivisionOrder.objects.get(id = order_id).delete()
    return HttpResponse('payment canceled')





# @csrf_exempt
# def paypal_ipn_listener(sender, **kwargs):
#     ipn_obj = sender

#     # Check if the payment is completed
#     if ipn_obj.payment_status == "Completed":

#         payer_id = ipn_obj.payer_id
#         payer_email = ipn_obj.payer_email
#         order_name = ipn_obj.item_name
#         order_price = ipn_obj.mc_gross
#         order_invoice = ipn_obj.invoice
        
#         # print(f"Transaction ID: {ipn_obj.txn_id}")
#         # print(f"Payer ID: {ipn_obj.payer_id}")
#         # print(f"Payer Email: {ipn_obj.payer_email}")
#         # print(f"Payment Status: {ipn_obj.payment_status}")
#         # print(f"Gross Amount: {ipn_obj.mc_gross}")
#         # print(f"Currency: {ipn_obj.mc_currency}")
#         # print(f"Item Name: {ipn_obj.item_name}")
#         # print(f"Invoice ID: {ipn_obj.invoice}")
#         # print(f"Custom Field: {ipn_obj.custom}")
#         # print(f"Receiver Email: {ipn_obj.receiver_email}")
#         # print(f"Is Test IPN: {ipn_obj.test_ipn}")

#         buyer_first_name = ipn_obj.first_name
#         buyer_last_name = ipn_obj.last_name

#         # create a user account
#         user = create_user_account(payer_id, payer_email, buyer_first_name, buyer_last_name)
#         create_division_order(order_name,order_price,order_invoice,user)

# # Connect the signal to your IPN listener
# valid_ipn_received.connect(paypal_ipn_listener)

