from django.shortcuts import render, HttpResponse, get_object_or_404
from .controller.forms import Registeration_Booster, ProfileEditForm, ProfileEditForm, PasswordEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from booster.models import OrderRating
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from booster.controller.serializers import RatingSerializer, CanChooseMeSerializer
User = get_user_model()
from django.shortcuts import render, redirect , HttpResponse, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from wildRift.models import WildRiftDivisionOrder, WildRiftRank
from valorant.models import ValorantDivisionOrder, ValorantPlacementOrder, ValorantRank
from pubg.models import PubgDivisionOrder, PubgRank
from leagueOfLegends.models import LeagueOfLegendsDivisionOrder, LeagueOfLegendsPlacementOrder, LeagueOfLegendsRank
from tft.models import TFTDivisionOrder, TFTPlacementOrder, TFTRank
from hearthstone.models import HearthstoneDivisionOrder, HearthstoneRank
from rocketLeague.models import RocketLeagueRankedOrder, RocketLeaguePlacementOrder, RocketLeagueSeasonalOrder, RocketLeagueTournamentOrder, RocketLeagueRank
from django.http import JsonResponse
from django.db.models import Sum
import json
from accounts.models import BaseOrder, Room, Message, Transaction, BoosterPercent
from django.http import HttpResponseBadRequest
from itertools import chain
from accounts.controller.order_creator import create_order, refresh_order_page

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

    if (game_name == 'wildRift' and request.user.booster.is_wf_player) or \
        (game_name == 'valorant' and request.user.booster.is_valo_player) or \
        (game_name == 'pubg' and request.user.booster.is_pubg_player) or \
        (game_name == 'lol' and request.user.booster.is_lol_player) or \
        (game_name == 'tft' and request.user.booster.is_tft_player) or \
        (game_name == 'hearthstone' and request.user.booster.is_hearthstone_player) or \
        (game_name == 'rocketLeague' and request.user.booster.is_rl_player)   :
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
    ratings = OrderRating.objects.filter(booster=booster_id).order_by('-created_at')
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
                existing_rating = OrderRating.objects.filter(order=order_obj).first()
                if existing_rating:
                    return HttpResponse('Rate Already Added', status=status.HTTP_400_BAD_REQUEST)
                serializer.save(order=order_obj)
                return redirect('homepage.index')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('Method Not Allowed', status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse('Order Not Done', status=status.HTTP_400_BAD_REQUEST)
        
# this for only test and will remove it ----      
def rate_page(request, order_id):
    order = BaseOrder.objects.get(id=order_id)
    return render(request,'booster/rating_page.html', context={'order':order})

def booster_orders(request):
    # Wildrift
    wildrift_orders = []
    wildrift_ranks = None
    if request.user.booster.is_wf_player:
        wildrift_orders = WildRiftDivisionOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        wildrift_ranks = WildRiftRank.objects.all()
        wildrift_divide_number = [4, 6]
        
    # Valorant
    valorant_division_orders = []
    valorant_placement_orders = []
    valorant_ranks = None
    if request.user.booster.is_valo_player:
        valorant_division_orders = ValorantDivisionOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        valorant_placement_orders = ValorantPlacementOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        valorant_ranks = ValorantRank.objects.all()
        valorant_divide_number = [3, 5]

    # PUBG
    pubg_division_orders = []   
    pubg_ranks = None
    if request.user.booster.is_pubg_player:
        pubg_division_orders = PubgDivisionOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        pubg_ranks = PubgRank.objects.all()
        pubg_divide_number = [4, 5]

    # LOL
    lol_division_orders = []
    lol_placement_orders = []
    lol_ranks = None
    if request.user.booster.is_lol_player:
        lol_division_orders = LeagueOfLegendsDivisionOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        lol_placement_orders = LeagueOfLegendsPlacementOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        lol_ranks = LeagueOfLegendsRank.objects.all()
        lol_divide_number = [4, 6]

    # TFT
    tft_division_orders = []
    tft_placement_orders = []
    tft_ranks = None
    if request.user.booster.is_tft_player:
        tft_division_orders = TFTDivisionOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        tft_placement_orders = TFTPlacementOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        tft_ranks = TFTRank.objects.all()
        tft_divide_number = [4, 5]

    # Hearthstone
    hearthstone_orders = []
    hearthstone_ranks = None
    if request.user.booster.is_hearthstone_player:
        hearthstone_orders = HearthstoneDivisionOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        hearthstone_ranks = HearthstoneRank.objects.all()
        hearthstone_divide_number = [10, 3]
    
    # Rocket League
    rocketLeague_division_orders = []
    rocketLeague_placement_orders = []
    rocketLeague_seasonal_orders = []
    rocketLeague_tournament_orders = []
    rocketLeague_ranks = None
    if request.user.booster.is_rl_player:
        rocketLeague_division_orders = RocketLeagueRankedOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        rocketLeague_placement_orders = RocketLeaguePlacementOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        rocketLeague_seasonal_orders = RocketLeagueSeasonalOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        rocketLeague_tournament_orders = RocketLeagueTournamentOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')

        rocketLeague_ranks = RocketLeagueRank.objects.all()
        rocketLeague_divide_number = [3, 0]
     
    orders = list(chain(wildrift_orders, valorant_division_orders, valorant_placement_orders, pubg_division_orders, lol_division_orders, lol_placement_orders, tft_division_orders, tft_placement_orders, hearthstone_orders, rocketLeague_division_orders, rocketLeague_placement_orders, rocketLeague_seasonal_orders, rocketLeague_tournament_orders))
    
    
    orders_with_percentage = []
    rooms =[]
    messages=[]
    slugs=[]
    for order in orders:
        percentage = 0
        now_price = 0
        if order.order.game_type != 'P' and order.order.game_type != 'S' and order.order.game_type != 'T':

            divide_number = [0, 0]
            if int(order.order.game_id) == 1:
                divide_number = wildrift_divide_number
            elif int(order.order.game_id) == 2:
                divide_number = valorant_divide_number
            elif int(order.order.game_id) == 3:
                divide_number = pubg_divide_number
            elif int(order.order.game_id) == 4:
                divide_number = lol_divide_number
            elif int(order.order.game_id) == 5:
                divide_number = tft_divide_number
            elif int(order.order.game_id) == 6:
                pass
            elif int(order.order.game_id) == 7:
                divide_number = hearthstone_divide_number
            elif int(order.order.game_id) == 9:
                divide_number = rocketLeague_divide_number

            with open(f'static/{order.order.game_name}/data/divisions_data.json', 'r') as file:
                division_data = json.load(file)
                division_price = [item for sublist in division_data for item in sublist]
                division_price.insert(0,0)

            marks_price = [0]
            current_marks = 0
            reached_marks = 0
            if order.order.game_name != "rocketLeague":
                with open(f'static/{order.order.game_name}/data/marks_data.json', 'r') as file:
                    marks_data = json.load(file)
                    marks_price = [item for sublist in marks_data for item in sublist]
                    marks_price.insert(0,0)

                current_marks = order.current_marks
                reached_marks = order.reached_marks

            current_rank = order.current_rank.id
            current_division = order.current_division
            
            reached_rank = order.reached_rank.id
            reached_division = order.reached_division

            print("Divide Number: ", divide_number)
            start_division = ((current_rank-1) * divide_number[0]) + current_division
            now_division = ((reached_rank-1) * divide_number[0]) + reached_division
            sublist_div = division_price[start_division:now_division]

            start_marks = (((current_rank-1) * divide_number[1]) + current_marks + 1) + 1
            now_marks = (((reached_rank-1) * divide_number[1]) + reached_marks + 1) + 1
            sublist_marks = marks_price[start_marks:now_marks]

            done_sum_div = sum(sublist_div)
            print("Divide Sum: ", done_sum_div)
            done_sum_marks = sum(sublist_marks)
            print("Marks Sum: ", done_sum_marks)

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
        'pubg_ranks': pubg_ranks,
        'lol_ranks': lol_ranks,
        'tft_ranks': tft_ranks,
        'hearthstone_ranks': hearthstone_ranks,
        'rocketLeague_ranks': rocketLeague_ranks
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
        print('game_id: ', game_id)
        order = None

        if order_id:
            if int(game_id) == 1:
                order = get_object_or_404(WildRiftDivisionOrder, order__id=order_id)
            elif int(game_id) == 2:
                order = get_object_or_404(ValorantDivisionOrder, order__id=order_id)
            elif int(game_id) == 3:
                order = get_object_or_404(PubgDivisionOrder, order__id=order_id)
            elif int(game_id) == 4:
                order = get_object_or_404(LeagueOfLegendsDivisionOrder, order__id=order_id)
            elif int(game_id) == 5:
                order = get_object_or_404(TFTDivisionOrder, order__id=order_id)
                print('Order: ', order)
            elif int(game_id) == 7:
                order = get_object_or_404(HearthstoneDivisionOrder, order__id=order_id)
                print('Order: ', order)
            elif int(game_id) == 9:
                order = get_object_or_404(RocketLeagueRankedOrder, order__id=order_id)
                print('Order: ', order)
            # try:
            order.order.is_drop = True
            order.order.is_done = True

            invoice = order.order.invoice.split('-')
            print('Old Invoice: ', invoice)
            invoice[3]= str(order.reached_rank.id) 
            invoice[4]= str(order.reached_division)
            if int(game_id) != 9:
                invoice[5]= str(order.reached_marks)
            else:
                invoice[5] = '0'
            new_invoice = '-'.join(invoice)
            print('New Invoice: ', new_invoice)
            payer_id = order.order.payer_id
            customer = order.order.customer
            
            new_order = create_order(new_invoice, payer_id, customer, 'Continue', order.order.name)
            new_order.order.actual_price = order.order.actual_price-order.order.money_owed
            new_order.order.customer_gamename = order.order.customer_gamename
            new_order.order.customer_password = order.order.customer_password
            new_order.order.customer_server = order.order.customer_server
            new_order.order.save()
            order.order.save()
            order.save()
            return redirect(reverse_lazy('booster.orders'))
            # except:
            #     return JsonResponse({'Drop Success': False})
    return JsonResponse({'success': False})

def update_rating(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        game_id  = request.POST.get('order_game_id')
        # Order Model & Rank Model
        OrderModel = None
        RankModel = None
        if int(game_id) == 1:
            OrderModel = WildRiftDivisionOrder
            RankModel = WildRiftRank
        elif int(game_id) == 2:
            OrderModel = ValorantDivisionOrder
            RankModel = ValorantRank
        elif int(game_id) == 3:
            OrderModel = PubgDivisionOrder
            RankModel = PubgRank
        elif int(game_id) == 4:
            OrderModel = LeagueOfLegendsDivisionOrder
            RankModel = LeagueOfLegendsRank
        elif int(game_id) == 5:
            OrderModel = TFTDivisionOrder
            RankModel = TFTRank
        elif int(game_id) == 7:
            OrderModel = HearthstoneDivisionOrder
            RankModel = HearthstoneRank
        elif int(game_id) == 9:
            OrderModel = RocketLeagueRankedOrder
            RankModel = RocketLeagueRank

        try:
            reached_rank_id = request.POST.get('reached_rank')
            reached_division = request.POST.get('reached_division')
            if int(game_id) != 9:
                reached_marks = request.POST.get('reached_marks')
            if reached_rank_id and order_id and reached_division and (int(game_id) == 9 or reached_marks):
                order = get_object_or_404(OrderModel, order__id=order_id)
                print("Order: ", order)
                reached_rank = get_object_or_404(RankModel, pk=reached_rank_id)
                order.reached_rank = reached_rank
                order.reached_division = reached_division 
                if int(game_id) != 9:
                    order.reached_marks = reached_marks 
                order.save()
                return redirect(reverse_lazy('booster.orders'))
        except:
            return JsonResponse({'update success': False})
    return JsonResponse({'success': False})