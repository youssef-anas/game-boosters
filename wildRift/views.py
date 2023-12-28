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
from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import BaseOrder
from accounts.order_creator import create_order
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
    if extend_order_id > 0:
        try:
            # get extend order 
            extend_order = BaseOrder.objects.get(id=extend_order_id)
            extend_order_price = extend_order.price
            price = price - extend_order_price
        except: ####
            pass
    booster_id = data['choose_booster']
    if booster_id > 0 :
       get_object_or_404(User,id=booster_id,is_booster=True)
    else:
        booster_id = 0
    #####################################
    invoice = f'wr-1-{current_rank}-{current_division}-{marks}-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{price}-{extend_order_id}-{timezone.now()}'
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

    
def wildRiftOrders(request):
    divisions_order = WildRiftDivisionOrder.objects.filter(order__booster__isnull=True)
    placements_order = WildRiftPlacementOrder.objects.filter(booster__isnull=True)
    booster_percents = BoosterPercent.objects.get(pk=1)

    context = {
        "divisions_order": divisions_order,
        "placements_order": placements_order,
        'booster_percents':booster_percents
    }
    return render(request,'wildRift/Orders.html', context)

def get_latest_price(request):
    order_id = request.GET.get('order_id')
    order = BaseOrder.objects.filter(id=order_id, booster__isnull=True).first()

    if order:
        time_difference = order.update_actual_price()
        order.save()
        latest_price = order.actual_price
        return JsonResponse({'actual_price': latest_price, 'time_difference':time_difference})
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
        base_order.booster = request.user
        base_order.save()
    except Exception as e:
        print(f"Error updating order: {e}")
        return HttpResponseBadRequest(f"Error updating order{e}")

    return redirect(reverse_lazy('booster.orders'))



@csrf_exempt
def view_that_asks_for_money(request):
    if request.method == 'POST':
        if request.user.is_authenticated :
            if request.user.is_booster:
                messages.error(request, "You are a booster!, You can't make order.")
                return redirect(reverse_lazy('wildrift'))
        
            # user_has_uncompleted_order = BaseOrder.objects.filter(customer=request.user, is_done=False).exists()
            # if user_has_uncompleted_order:
            #     messages.error(request, "You already have a uncompleted order!, You can't make another one until this finish")
            #     return redirect(reverse_lazy('wildrift'))
        
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


def update_rating(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        reached_rank_id = request.POST.get('reached_rank')
        reached_division = request.POST.get('reached_division')
        reached_marks = request.POST.get('reached_marks')
        if reached_rank_id and order_id and reached_division and reached_marks:
            order = get_object_or_404(WildRiftDivisionOrder, order__id=order_id)
            reached_rank = get_object_or_404(WildRiftRank, pk=reached_rank_id)
            order.reached_rank = reached_rank
            order.reached_division = reached_division 
            order.reached_marks = reached_marks 
            order.save()
            return redirect(reverse_lazy('booster.orders'))
    return JsonResponse({'success': False})

def upload_finish_image(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            order = get_object_or_404(BaseOrder, id=order_id)
            finish_image = request.FILES.get('finish_image')
            if finish_image:
                order.finish_image = finish_image
                order.is_done = True
                order.save()
                return redirect(reverse_lazy('booster.orders'))
    return JsonResponse({'success': False})

def drop_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            order = get_object_or_404(WildRiftDivisionOrder, order_id=order_id)
            order.order.is_drop = True
            order.order.is_done = True

            invoice = order.order.invoice.split('-')
            invoice[2]= str(order.reached_rank.id) 
            invoice[3]= str(order.reached_division )
            invoice[4]= str(order.reached_marks)
            new_invoice = '-'.join(invoice)
            payer_id = order.order.payer_id
            customer = order.order.customer
            
            new_order = create_order(new_invoice,payer_id, customer, 'Continue')
            new_order.order.name = order.order.name
            new_order.order.actual_price = order.order.actual_price-order.order.money_owed
            new_order.order.customer_gamename = order.order.customer_gamename
            new_order.order.customer_password = order.order.customer_password
            new_order.order.customer_server = order.order.customer_server
            new_order.order.save()
            order.order.save()
            order.save()
            return redirect(reverse_lazy('booster.orders'))
    return JsonResponse({'success': False})

def confirm_details(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            order = get_object_or_404(BaseOrder, id=order_id)
            order.message = None
            order.data_correct = True
            order.save()
            return redirect(reverse_lazy('booster.orders'))
    return JsonResponse({'success': False})

def ask_customer(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            order = get_object_or_404(BaseOrder, id=order_id)
            order.message = 'Pleace Specify Your Details'
            order.data_correct = False
            order.save()
            return redirect(reverse_lazy('booster.orders'))
    return JsonResponse({'success': False})
