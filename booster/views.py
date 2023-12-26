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
from django.http import JsonResponse
from django.db.models import Sum
import json
from accounts.models import BaseOrder, Room, Message


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
    # if not request.user.is_booster:
    #     return HttpResponse('you are not booster')
    orders = WildRiftDivisionOrder.objects.filter(order__booster=request.user,order__is_done=False).order_by('order__id')
    ranks = WildRiftRank.objects.all()
    with open('static/wildRift/data/divisions_data.json', 'r') as file:
        division_data = json.load(file)
        division_price = [item for sublist in division_data for item in sublist]
        division_price.insert(0,0)
    
    with open('static/wildRift/data/marks_data.json', 'r') as file:
        marks_data = json.load(file)
        marks_price = [item for sublist in marks_data for item in sublist]
        marks_price.insert(0,0)

    orders_with_percentege = []
    rooms =[]
    messages=[]
    slugs=[]
    for order in orders:

        current_rank = order.current_rank.id
        current_division = order.current_division
        current_marks = order.current_marks

        reached_rank = order.reached_rank.id
        reached_division = order.reached_division
        reached_marks = order.reached_marks

        start_division = ((current_rank-1)*4) + current_division
        now_division = ((reached_rank-1)*4)+ reached_division
        sublist_div = division_price[start_division:now_division]

        start_marks = (((current_rank-1)*4) + current_marks + 1) + 1
        now_marks = (((reached_rank-1)*4) + reached_marks + 1) + 1
        sublist_marks = marks_price[start_marks:now_marks]

        done_sum_div = sum(sublist_div)
        done_sum_marks = sum(sublist_marks)

        done_sum = done_sum_div + done_sum_marks

        percentege = round((done_sum / order.order.price) * 100 , 2)
        if percentege >= 100 :
            percentege = 100

        now_price = round(order.order.actual_price * (percentege / 100) , 2)

        order.order.money_owed = now_price
        order.order.save()
        
        current_room = Room.get_specific_room(order.order.customer, order.order.id)
        if current_room is not None:
            messages=Message.objects.filter(room=current_room) 
            slug = current_room.slug
            order_data = {
                'order': order,
                'percentege': percentege,
                'now_price': now_price,
                'user': request.user,
                'room': current_room,
                'messages': messages,
                'slug': slug,
            }
            orders_with_percentege.append(order_data)
        else:
            order_data = {
            'order': order,
            'percentege': percentege,
            'now_price': now_price,
            'user': request.user,
            'room': None,
            'messages': None,
            'slug': None,
            }
            orders_with_percentege.append(order_data)
            
 
    context = {
        'orders': orders_with_percentege,
        'ranks': ranks,
    }
    return render(request, 'booster/booster-order.html', context=context)

class CanChooseMe(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user 

        instance = user

        instance.user.can_choose_me = not instance.user.can_choose_me
        instance.user.save()

        serializer = CanChooseMeSerializer(instance)
        return JsonResponse(serializer.data)