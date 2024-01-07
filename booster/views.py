from django.shortcuts import render, HttpResponse, get_object_or_404
from .forms import Registeration_Booster, ProfileEditForm, ProfileEditForm, PasswordEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from booster.models import Rating
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from booster.serializers import RatingSerializer, CanChooseMeSerializer
User = get_user_model()
from django.shortcuts import render, redirect , HttpResponse, get_object_or_404
from django.urls import reverse, reverse_lazy
from .forms import Registeration_Booster
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from wildRift.models import WildRiftDivisionOrder, WildRiftRank
from valorant.models import ValorantDivisionOrder, ValorantPlacementOrder, ValorantRank
from django.http import JsonResponse
from django.db.models import Sum
import json
from accounts.models import BaseOrder, Room, Message, Transaction, BoosterPercent
from django.http import HttpResponseBadRequest
from wildRift.reached_percent import wildrift_reached_percent
from valorant.reached_percent import valorant_reached_percent
from itertools import chain
from accounts.order_creator import create_order, refresh_order_page

def register_booster_view(request):
    form = Registeration_Booster()
    if request.method == 'POST':
        form = Registeration_Booster(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            print(user.email_verified_at)
            user.is_active = False  # Mark the user as inactive until they activate their account
            user.is_booster = True
            user.save()
            # Send activation email
            return HttpResponse(f'account created with username {user.username}')
        return render(request, 'booster/registeration_booster.html', {'form': form}) # return error 
    return render(request, 'booster/registeration_booster.html', {'form': form})

@login_required
def edit_booster_profile(request):
    profile_form = ProfileEditForm(instance=request.user)
    password_form = PasswordEditForm(user=request.user)

    if request.method == 'POST':
        if 'profile_submit' in request.POST:
            profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('edit.booster.profile')

        elif 'password_submit' in request.POST:
            password_form = PasswordEditForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Password changed successfully.')
                return redirect('edit.booster.profile')

    return render(request, 'booster/edit_profile.html', {'profile_form': profile_form, 'password_form': password_form})

# Orders Page
def jobs(request):
    orders = BaseOrder.objects.filter(booster__isnull=True)
    booster_percents = BoosterPercent.objects.get(pk=1)

    context = {
        "orders": orders,
        'booster_percents':booster_percents
    }
    return render(request,'booster/Orders.html', context)

def calm_order(request, game_name, id):
    order = get_object_or_404(BaseOrder, id=id)

    if (game_name == 'wildrift' and request.user.booster.is_wf_player) or \
        (game_name == 'valorant' and request.user.booster.is_valo_player):
        try:
            order.booster = request.user
            order.save()
        except Exception as e:
            print(f"Error updating order: {e}")
            return HttpResponseBadRequest(f"Error updating order{e}")
    else:
        messages.error(request, "You aren't play this game, Calm order for your game!")
        return redirect(reverse_lazy('orders.jobs'))
    refresh_order_page()
    return redirect(reverse_lazy('booster.orders'))

def profile_booster_view(request, booster_id):
    booster = get_object_or_404(User, id=booster_id,is_booster = True)
    ratings = Rating.objects.filter(booster=booster_id).order_by('-created_at')
    total_ratings = ratings.aggregate(Sum('rate'))['rate__sum']
    rate_count = ratings.count()
    customer_reviews = total_ratings / rate_count if rate_count > 0 else 0
    completed_orders = BaseOrder.objects.filter(is_done = True, booster=booster)
    completed_boosts_count = completed_orders.count()
    context = {
        "ratings":ratings,
        'booster':booster,
        'completed_boosts_count':completed_boosts_count,
        'customer_reviews':customer_reviews,
        'completed_orders':completed_orders,
        }
    return render(request, 'booster/booster_profile.html', context)


@login_required
def get_rate(request, order_id):
    order_obj = get_object_or_404(BaseOrder, id=order_id)
    customer = order_obj.customer
    booster = order_obj.booster
    if not (customer and booster):
        return HttpResponse(f"Can't set rate to order {order_id}, with customer {customer} and booster {booster}")
    if order_obj.is_done:
        if request.method == 'POST':
            serializer = RatingSerializer(data=request.POST)
            if serializer.is_valid():
                existing_rating = Rating.objects.filter(order=order_obj).first()
                if existing_rating:
                    return HttpResponse('Rate Already Added', status=status.HTTP_400_BAD_REQUEST)
                serializer.save(order=order_obj)
                return redirect('homepage.index')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('Method Not Allowed', status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse('Order Not Done', status=status.HTTP_400_BAD_REQUEST)
        
# this for only test and will remove it        
def rate_page(request, order_id):
    order = WildRiftDivisionOrder.objects.get(order__id=order_id)
    return render(request,'booster/rating_page.html', context={'order':order})

def booster_orders(request):
    # component = None
    # Wildrift
    wildrift_ranks = None
    if request.user.booster.is_wf_player:
        wildrift_orders = WildRiftDivisionOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        wildrift_ranks = WildRiftRank.objects.all()
        
    # Valorant
    valorant_ranks = None
    if request.user.booster.is_valo_player:
        valorant_division_orders = ValorantDivisionOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        valorant_placement_orders = ValorantPlacementOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        valorant_ranks = ValorantRank.objects.all()
     
    orders = list(chain(wildrift_orders, valorant_division_orders, valorant_placement_orders))
    
    
    orders_with_percentage = []
    rooms =[]
    messages=[]
    slugs=[]
    for order in orders:
        percentage = 0
        now_price = 0
        if order.order.game_type != 'P':
            with open(f'static/{order.order.game_name}/data/divisions_data.json', 'r') as file:
                division_data = json.load(file)
                division_price = [item for sublist in division_data for item in sublist]
                division_price.insert(0,0)
        
            with open(f'static/{order.order.game_name}/data/marks_data.json', 'r') as file:
                marks_data = json.load(file)
                marks_price = [item for sublist in marks_data for item in sublist]
                marks_price.insert(0,0)

                current_rank = order.current_rank.id
                current_division = order.current_division
                current_marks = order.current_marks

                reached_rank = order.reached_rank.id
                reached_division = order.reached_division
                reached_marks = order.reached_marks

                start_division = ((current_rank-1) * 4) + current_division
                now_division = ((reached_rank-1) * 4)+ reached_division
                sublist_div = division_price[start_division:now_division]

                start_marks = (((current_rank-1) * 4) + current_marks + 1) + 1
                now_marks = (((reached_rank-1) * 4) + reached_marks + 1) + 1
                sublist_marks = marks_price[start_marks:now_marks]

                done_sum_div = sum(sublist_div)
                done_sum_marks = sum(sublist_marks)

                done_sum = done_sum_div + done_sum_marks

                percentage = round((done_sum / order.order.price) * 100 , 2)
                if percentage >= 100 :
                    percentage = 100

                now_price = round(order.order.actual_price * (percentage / 100) , 2)

                order.order.money_owed = now_price
                order.order.save()

        current_room = Room.get_specific_room(order.order.customer, order.order.id)
        if current_room is not None:
            messages=Message.objects.filter(room=current_room) 
            slug = current_room.slug
            order_data = {
                'order': order,
                'percentage': percentage,
                'now_price': now_price,
                'user': request.user,
                'room': current_room,
                'messages': messages,
                'slug': slug,
            }
            orders_with_percentage.append(order_data)
        else:
            order_data = {
            'order': order,
            'percentage': percentage,
            'now_price': now_price,
            'user': request.user,
            'room': None,
            'messages': None,
            'slug': None,
            }
            orders_with_percentage.append(order_data)
            
 
    context = {
        'orders': orders_with_percentage,
        'wildrift_ranks': wildrift_ranks,
        'valorant_ranks': valorant_ranks,
    }
    return render(request, 'booster/booster-order.html', context=context)


class CanChooseMe(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user 

        instance = user

        instance.booster.can_choose_me = not instance.booster.can_choose_me
        instance.booster.save()

        serializer = CanChooseMeSerializer(instance)
        return JsonResponse(serializer.data)
    
@login_required
def booster_history(request):
    history = Transaction.objects.filter(user=request.user)
    return render(request, 'booster/booster_histoty.html', context={'history' : history})

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


def get_latest_price(request):
    order_id = request.GET.get('order_id')
    order = BaseOrder.objects.get(id=order_id)

    if order:
        time_difference = order.update_actual_price()
        order.save()
        latest_price = order.actual_price
        return JsonResponse({'actual_price': latest_price, 'time_difference':time_difference})
    else:
        return JsonResponse({'error': 'Order not found'}, status=404)
    
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

# Drop
def drop_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        game_id = request.POST.get('order_game_id')
        order = None

        if order_id:
            if int(game_id) == 1:
                order = get_object_or_404(WildRiftDivisionOrder, order_id=order_id)
            elif int(game_id) == 2:
                order = get_object_or_404(ValorantDivisionOrder, order_id=order_id)
            
            try:
                order.order.is_drop = True
                order.order.is_done = True

                invoice = order.order.invoice.split('-')
                invoice[3]= str(order.reached_rank.id) 
                invoice[4]= str(order.reached_division )
                invoice[5]= str(order.reached_marks)
                new_invoice = '-'.join(invoice)
                payer_id = order.order.payer_id
                customer = order.order.customer
                
                new_order = create_order(new_invoice,payer_id, customer, 'Continue', order.order.name)
                new_order.order.actual_price = order.order.actual_price-order.order.money_owed
                new_order.order.customer_gamename = order.order.customer_gamename
                new_order.order.customer_password = order.order.customer_password
                new_order.order.customer_server = order.order.customer_server
                new_order.order.save()
                order.order.save()
                order.save()
                return redirect(reverse_lazy('booster.orders'))
            except:
                return JsonResponse({'success': False})
    return JsonResponse({'success': False})

def update_rating(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        game_id  = request.POST.get('order_game_id')
        print('Game ID: ', game_id)
        # Order Model & Rank Model
        OrderModel = None
        RankModel = None
        if int(game_id) == 1:
            OrderModel = WildRiftDivisionOrder
            RankModel = WildRiftRank
        elif int(game_id) == 2:
            OrderModel = ValorantDivisionOrder
            RankModel = ValorantRank

        try:
            reached_rank_id = request.POST.get('reached_rank')
            reached_division = request.POST.get('reached_division')
            reached_marks = request.POST.get('reached_marks')
            if reached_rank_id and order_id and reached_division and reached_marks:
                order = get_object_or_404(OrderModel, order__id=order_id)
                reached_rank = get_object_or_404(RankModel, pk=reached_rank_id)
                order.reached_rank = reached_rank
                order.reached_division = reached_division 
                order.reached_marks = reached_marks 
                order.save()
                return redirect(reverse_lazy('booster.orders'))
        except:
            pass
    return JsonResponse({'success': False})