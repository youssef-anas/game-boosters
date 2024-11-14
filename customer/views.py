from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from accounts.models import BaseOrder, BaseUser, BaseOrder, TokenForPay, Transaction, Tip_data, Wallet
from customer.controllers.order_creator import create_order
from chat.models import Room, Message
from gameBoosterss.utils import refresh_order_page, send_change_data_msg, send_available_to_play_mail, tipPayment
# from accounts.tasks import update_database_task
# from django_q.tasks import async_task
from django.utils import timezone
from customer.forms import EmailEditForm, ProfileEditForm, PasswordEditForm, CustomOrderForm
from django.contrib import messages
from gameBoosterss.utils import get_boosters
import secrets
from django.conf import settings
from customer.controllers.serializers import *
from django.db.models import Q
from booster.models import OrderRating
from games.models import Game
from customer.models import CustomOrder
import ast, random

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
    payer_id = request.GET.get("PayerID", None)
    token_object = get_object_or_404(TokenForPay, token=token)
    # invoice= token_object.invoice
    # invoice_values = invoice.split('-')
    # booster_id = int(invoice_values[12])

    order_info = ast.literal_eval(token_object.game_info)

    booster_id = order_info['base_order']['booster_id']
    GameType = token_object.content_type.model_class()

    game_order_info = order_info['game_order']

    champions = game_order_info.pop('champions', None)

    bosses = game_order_info.pop('bosses', None)

    status = 'New'
    if order_info['base_order'].get('status', None):
        status = order_info['base_order']['status']
        order_info['base_order'].pop('status', None)

    base_order = BaseOrder.objects.create(**order_info['base_order'], invoice='invoice', payer_id=payer_id, customer=request.user, status=status, content_type=token_object.content_type)
    game_order = GameType.objects.create(**game_order_info, order=base_order)
    
    if champions:
        game_order.champions.set(champions)
    if bosses:
        game_order.bosses.set(bosses)    

    base_order.object_id = game_order.pk
    base_order.captcha_id =  random.randint(1, 2000)
    game_order.save_with_processing()


    if hasattr(order_info['extra_order'], 'extend_order'):
        extend_order_id = order_info['extra_order']['extend_order']
        try :
            extend_order = BaseOrder.objects.get(id = extend_order_id)
            extend_order.is_done = True
            extend_order.save()
        except:
            pass
    
    Transaction.objects.create (
        user= request.user,
        amount=order_info['extra_order']['price'],
        order=base_order,
        status=status,  
        type='WITHDRAWAL',
        notice=f'{base_order.details} - {base_order.name}'
    )
    wallet , created = Wallet.objects.get_or_create(user = request.user)
    wallet.money += float(order_info['extra_order']['price'])
    wallet.save()


    
    try:
        booster = BaseUser.objects.get(id=booster_id, is_booster=True)
    except BaseUser.DoesNotExist:
        booster = None
    # order = create_order(invoice, payer_id, request.user)
    
    Room.create_room_with_admins(request.user, game_order.order.name)
    Room.create_room_with_booster(request.user, booster, game_order.order.name)
    refresh_order_page()
    # token_object.delete()
    # async_task(update_database_task, order.order.id)
    return redirect(reverse('customer.filldata', kwargs={'order_name': game_order.order.name}))
    

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
            order =  content_type.model_class().objects.get(order = base_order)
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
    messages.error(request, "This order dosent belong to you (:")
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
            # customer_server = serializer.validated_data.get('customer_server')
            customer_username = serializer.validated_data.get('customer_username')
            # booster = serializer.validated_data.get('chosen_booster_id')

            order = get_object_or_404(BaseOrder, pk=order_id)
            order.customer_gamename = customer_gamename
            # order.customer_server = customer_server
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
        token_for_pay = TokenForPay.create_token_for_pay(request.user, token_with_data)
    
        if tip and order_id and booster:
            invoice = f'tip-{user}-{tip}-{order_id}-{booster}-{time}'
            request.session['invoice'] = invoice

        payment = tipPayment(tip, request, token_for_pay)
        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
        else:
            messages.error(request, "There was an issue connecting to PayPal. Please try again later.")
            return redirect(reverse_lazy('homepage.index'))
        return JsonResponse({'success': False})
    
def success_tip(request, token):
    token_object = get_object_or_404(TokenForPay, token=token)
    invoice= token_object.invoice

    
    splited_token = invoice.split('-')
    username = splited_token[0]
    tip = int(splited_token[1])
    order_id = int(splited_token[2])
    order = BaseOrder.objects.get(id = order_id)
    booster = splited_token[3]
    payer_id = request.GET.get("PayerID")
    notice = f'Tip from {username}'

    if request.user == token_object.user and request.user.username == username and payer_id:
        room = Room.get_specific_room(request.user, order.name)
        msg = f'You Sent a tip of {tip}$, Thank you!'
        Message.create_tip_message(request.user,msg,room)
        token_object.delete()
        if invoice != 'unknown':
            request.session.pop('invoice')
        tip_data = Tip_data.create_tip(invoice, payer_id)
        booster_instance = BaseUser.objects.get(username=booster)
        Transaction.objects.create(user=booster_instance, amount=tip, order_id=order_id, notice=notice, tip=tip_data, status='Tip', type='DEPOSIT')
        booster_wallet = booster_instance.wallet
        booster_wallet.money += tip
        booster_wallet.save()
        return redirect(reverse('customer.orders.details', kwargs={'order_name': order.name}))
    return HttpResponse("error while adding tip to bosster, check your wallet and call page admin")

def cancel_tip(request, token, order_id):
    # TODO : check This Shehab --- I Cancel Return To Customer Side
    TokenForPay.delete_token(token)
    order = BaseOrder.objects.get(id=order_id)
    request.session['success_tip'] = 'false'
    return redirect(reverse('customer.orders.details', kwargs={'order_name': order.name}))


def payment_canceled(request, token):
    return redirect(reverse("homepage.index"))

def custom_order(request, game_id):
    # game = Game.objects.get(pk=game_id)
    feedbacks = OrderRating.objects.filter(order__game_id=game_id)

    if request.method == 'POST':
        form = CustomOrderForm(request.POST)
        if form.is_valid():
            # Process form data and save order
            order_text = form.cleaned_data['order']
            email = form.cleaned_data['email']
            # Assuming you have access to the current user
            customer = request.user
            # Create the order
            new_order = CustomOrder.objects.create(customer=customer, game_id=game_id, order=order_text, email=email)
            messages.success(request, f'Your Order Send Successfully')
            return redirect(reverse('custom.order', kwargs={'game_id': game_id}))
        else:
            # Form has errors, display error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = CustomOrderForm()

    context = {
        'game_id': game_id,
        'feedbacks': feedbacks,
        'form': form,
    }
    return render(request, 'customer/custom-order.html', context)


from django.views.generic import FormView
from django.urls import reverse
from .forms import BaseOrderForm
from accounts.models import BaseOrder

class BaseOrderFormView(FormView):
    template_name = 'customer/set_data.html'
    form_class = BaseOrderForm

    def get_success_url(self):
        return reverse('customer.orders.details', kwargs={'order_name': self.kwargs['order_name']})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        order_name = self.kwargs.get('order_name')
        if order_name:
            order = BaseOrder.objects.filter(name=order_name).order_by('id').last()
            kwargs['instance'] = order
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
        
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_name = self.kwargs.get('order_name')
        if order_name:
            order = BaseOrder.objects.filter(name=order_name).order_by('id').last()
            context['order'] = order
        return context
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

class AvailableToPlayMail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user
        cache_key = f"available_to_play_mail_{user.id}_{id}"
        block_duration = timedelta(minutes=14)

        # Check if the user has made a request within the last 5 minutes
        last_request_time = cache.get(cache_key)
        if last_request_time:
            time_since_last_request = datetime.now() - last_request_time
            if time_since_last_request < block_duration:
                remaining_time = block_duration - time_since_last_request
                minutes, seconds = divmod(remaining_time.seconds, 60)
                return Response({
                    'message': 'You can only send an available to play mail every 5 minutes.',
                    'remaining_time': f'{minutes} minutes, {seconds} seconds'
                }, status=403)

        host = request.get_host()
        order = get_object_or_404(BaseOrder, Q(pk=id) & (Q(customer=user) | Q(booster=user)))
        client_url = f"{request.scheme}://{host}"
        send_available_to_play_mail(user, order, client_url)

        # Update the cache with the current request time
        cache.set(cache_key, datetime.now(), timeout=block_duration.seconds)

        return Response({'message': 'Available to play mail sent successfully'})