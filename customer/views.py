from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from accounts.models import BaseOrder, BaseUser, BaseOrder, TokenForPay, Transaction, Tip_data
from customer.controllers.order_creator import create_order
from chat.models import Room, Message
from gameBoosterss.utils import refresh_order_page, send_change_data_msg
from accounts.tasks import update_database_task
from django_q.tasks import async_task
from django.utils import timezone
from customer.forms import EmailEditForm, ProfileEditForm, PasswordEditForm
from django.contrib import messages
from gameBoosterss.utils import get_boosters
import secrets
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from customer.controllers.serializers import *
from django.db.models import Q

@login_required
def customer_setting(request):
    profile_form = ProfileEditForm(instance=request.user)
    password_form = PasswordEditForm(user=request.user)
    email_edit_form = EmailEditForm(user=request.user)

    if request.method == 'POST':
        if 'profile_submit' in request.POST:
            profile_form = ProfileEditForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile Updated Successfully.')
                return redirect('customer.setting')

        elif 'password_submit' in request.POST:
            password_form = PasswordEditForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Password Changed Successfully.')
                return redirect('customer.setting')

        elif 'email_submit' in request.POST:
            email_edit_form = EmailEditForm(request.POST, user=request.user)
            if email_edit_form.is_valid():
                email_edit_form.save()
                messages.success(request, 'Email Updated Successfully.')
                return redirect('customer.setting')

    return render(request, 'customer/setting.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'email_edit_form': email_edit_form
    })


@login_required
def payment_sucess_view(request, token):
    # invoice = request.session.get('invoice')
    payer_id = request.GET.get("PayerID")
    token_object = TokenForPay.objects.get(token=token)
    invoice= token_object.invoice
    token_object.delete()
    invoice_values = invoice.split('-')
    booster_id = int(invoice_values[12])
    try:
        booster = BaseUser.objects.get(id=booster_id, is_booster=True)
    except BaseUser.DoesNotExist:
        booster = None
    order = create_order(invoice, payer_id, request.user)
    Room.create_room_with_admins(request.user, order.order.name)
    Room.create_room_with_booster(request.user, booster, order.order.name)
    refresh_order_page()
    async_task(update_database_task, order.order.id)
    return redirect(reverse('customer.orders.details', kwargs={'order_name': order.order.name}))
    

def customer_orders(request):
    base_orders = BaseOrder.objects.filter(
        customer=request.user,  # Filter orders for the current user
        is_drop=False,           # Exclude orders that are dropped
    ).exclude(
        order_rated__customer=request.user  # Exclude orders where the current user has rated the booster
    ).filter(
        Q(is_done=False) | Q(is_done=True)  # Include orders that are either not done or already done
    )

    orders = []

    for base_order in base_orders:
        content_type = base_order.content_type

        if content_type:
            order =  content_type.model_class().objects.get(order_id=base_order.object_id)
            orders.append(order)

    context = {
        "orders": orders
    }
    
    return render(request, 'customer/customer-orders.html', context=context)

# TODO fix error : order = BaseOrder.objects.filter(customer=customer).last()
@login_required
def customer_side(request, order_name):
    customer = request.user

    base_order = BaseOrder.objects.filter(
            customer=customer,
            name=order_name,
            is_drop=False, 
        ).exclude(
            order_rated__customer=customer
        ).filter(
            Q(is_done=False) | Q(is_done=True)  # Include orders that are either not done or already done
        ).order_by('id').last()
    if base_order:
        if base_order.is_done:
            return redirect(reverse_lazy('rate.page', kwargs={'order_id': base_order.id}))
        boosters = get_boosters(base_order.game.pk)     
        
        # Chat with admins
        admins_chat_slug = f'roomFor-{request.user.username}-admins-{base_order.name}'

        admins_room = Room.objects.get(slug=admins_chat_slug)
        admins_messages = Message.objects.filter(room=admins_room)

        game_order = base_order.related_order
        
        # Chat with booster
        specific_room = Room.get_specific_room(request.user, base_order.name)
        slug = specific_room.slug if specific_room else None
        if slug:
            room = Room.objects.get(slug=slug)
            chat_messages=Message.objects.filter(room=Room.objects.get(slug=slug)) 
            context = {
                'user':request.user,
                "slug":slug,
                'messages':chat_messages,
                'room':room,
                'boosters':boosters,
                'order':game_order,
                'admins_room':admins_room,
                'admins_room_name':admins_room,
                'admins_messages':admins_messages,
                'admins_chat_slug':admins_chat_slug
            }    
            template_name = 'customer/customer_side.html'
            return render(request, template_name, context)
        return  HttpResponse("error on creating chat")
    messages.error(request, "This order dosent belong to you, dont try to cheat (:")
    return  redirect(reverse('homepage.index'))


def choose_booster(request, order_id, booster_id):
    if request.method == 'POST':
        # TODO make it in kwrgs better than POST data

        if booster_id and order_id:
            order = get_object_or_404(BaseOrder, pk=order_id)
            booster = get_object_or_404(BaseUser, id=booster_id)
            order.booster = booster
            order.save()
            # TODO pass booster to chat model 
            return redirect(reverse('accounts.customer_side', kwargs={'order_name': order.name}))
    return JsonResponse({'success': False})


def set_customer_data(request):
    if request.method == 'POST':
        
        # TODO use serializer better to validate data
        serializer = BaseOrderSerializer(data=request.POST)
        order_id = request.POST.get('order_id')
        
        if serializer.is_valid():
            customer_gamename = serializer.validated_data.get('customer_gamename')
            customer_password = serializer.validated_data.get('customer_password')
            customer_server = serializer.validated_data.get('customer_server')
            customer_username = serializer.validated_data.get('customer_username')
            # booster = serializer.validated_data.get('chosen_booster_id')

            order = get_object_or_404(BaseOrder, pk=order_id)
            order.customer_gamename = customer_gamename
            order.customer_server = customer_server
            order.customer_username = customer_username

            order.message = None
            order.data_correct = True
            
            if customer_password:
                order.customer_password = serializer.validated_data.get('customer_password')
            order.save()

            room = Room.get_specific_room(request.user, order.name)
            
            message_change = Message.create_change_message(request.user,room)
            send_change_data_msg(message_change)

            # if booster:
            #     # pass the booster to chat
            #     pass
            return JsonResponse({
                'message': 'Data updated successfully!',
                'updated_data': serializer.data,
                'success': True
            })
        else:
            return JsonResponse({
                'message': 'Invalid data!',
                'errors': serializer.errors,
                'success': False
            }, status=400)
    
    return JsonResponse({'message': 'Invalid request!'}, status=400)


def tip_booster(request):
    if request.method == 'POST':
        tip = request.POST.get('tip')
        order_id = request.POST.get('order_id')
        booster = request.POST.get('booster')
        user = str(request.user.username)
        time = str(timezone.now())
        token = secrets.token_hex(14)
        token_with_data = '-'.join([user, tip, order_id, booster, token])
        token_for_pay, created = TokenForPay.objects.get_or_create(user=request.user, defaults={'token': token_with_data})
        
        if not created:
            token_for_pay.token = token_with_data
            token_for_pay.save()
    
        if tip and order_id and booster:
            invoice = f'tip-{user}-{tip}-{order_id}-{booster}-{time}'
            request.session['invoice'] = invoice
            paypal_dict = {
                "business": settings.PAYPAL_EMAIL,
                "amount": tip,
                "item_name": f"tip {booster}",
                "invoice": invoice,
                "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                "return": request.build_absolute_uri(f"/customer/tip-booster/success/{token_with_data}/"),
                "cancel_return": request.build_absolute_uri(f"/customer/tip-booster/cancel/{token_with_data}/{order_id}"),
            }
            # Create the instance.
            form = PayPalPaymentsForm(initial=paypal_dict)
            context = {"form": form}
            return render(request, "accounts/paypal.html", context,status=200)
        return JsonResponse({'success': False})
    
def success_tip(request,token):
    token_with_data = TokenForPay.get_token(token) 
    splited_token = token.split('-')
    username = splited_token[0]
    tip = int(splited_token[1])
    order_id = int(splited_token[2])
    order = BaseOrder.objects.get(id = order_id)
    booster = splited_token[3]
    payer_id = request.GET.get("PayerID")
    notice = f'Tip from {username}'
    invoice = request.session.get('invoice', 'unknown')
    if request.user == token_with_data.user and request.user.username == username and payer_id:
        room = Room.get_specific_room(request.user, order.name)
        msg = f'You Sent a tip of {tip}$, Thank you!'
        Message.create_tip_message(request.user,msg,room)
        token_with_data.delete()
        if invoice != 'unknown':
            request.session.pop('invoice')
        tip_data = Tip_data.create_tip(invoice, payer_id)
        booster_instance = BaseUser.objects.get(username=booster)
        Transaction.objects.create(user=booster_instance, amount=tip, order_id=order_id, notice=notice, tip=tip_data, status='Tip', type='DEPOSIT')
        booster_wallet = booster_instance.wallet
        booster_wallet.money += tip
        booster_wallet.save()
        return redirect(reverse('accounts.customer_orders', kwargs={'order_name': order.name}))
    return HttpResponse("error while adding tip to bosster, check your wallet and call page admin")

def cancel_tip(request, token, order_id):
    # TODO : check This Shehab --- I Cancel Return To Customer Side
    TokenForPay.delete_token(token)
    order = BaseOrder.objects.get(id=order_id)
    request.session['success_tip'] = 'false'
    return redirect(reverse('accounts.customer_orders', kwargs={'order_name': order.name}))


def payment_canceled(request):
    return HttpResponse('payment canceled')