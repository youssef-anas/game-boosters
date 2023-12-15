from django.shortcuts import render, HttpResponse, get_object_or_404
from .forms import Registeration_Booster, ProfileEditForm, ProfileEditForm, PasswordEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from booster.models import Rating
from django.contrib.auth import get_user_model
from wildRift.models import WildRiftDivisionOrder
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from booster.serializers import RatingSerializer
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
    completed_orders = WildRiftDivisionOrder.objects.filter(is_done = True, booster=booster)
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
    order_obj = get_object_or_404(WildRiftDivisionOrder, id=order_id)
    customer =order_obj.customer
    booster =order_obj.booster
    if not (customer and booster):
        return HttpResponse(f'cant set rate to order {order_id}, with customer {customer} and booster {booster}')
    if order_obj.is_done:
        if request.method == 'POST':
            serializer = RatingSerializer(data=request.POST)
            if serializer.is_valid():
                existing_rating = Rating.objects.filter(order=order_obj).first()
                if existing_rating:
                    return HttpResponse('Rate Already Added', status=status.HTTP_400_BAD_REQUEST)
                serializer.save(order=order_obj)
                return redirect('wildrift')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('Method Not Allowed', status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse('Order Not Done', status=status.HTTP_400_BAD_REQUEST)
        
# this for only test and will remove it        
def form_test(request):
    order = WildRiftDivisionOrder.objects.get(id=1)
    return render(request,'booster/rating_page.html', context={'order':order})

def booster_orders(request):
    # if not request.user.is_booster:
    #     return HttpResponse('you are not booster')
    orders = WildRiftDivisionOrder.objects.filter(booster=request.user,is_done=False).order_by('id')
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

        percentege = round((done_sum / order.price) * 100 , 2)

        now_price = round(order.actual_price * (percentege / 100) , 2)

        order_data = {
            'order': order,
            'percentege': percentege,
            'now_price': now_price
        }
        orders_with_percentege.append(order_data)

    context = {
        'orders': orders_with_percentege,
        'ranks': ranks
    }
    return render(request, 'booster/booster-order.html', context=context)

def update_rating(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        reached_rank_id = request.POST.get('reached_rank')
        reached_division = request.POST.get('reached_division')
        reached_marks = request.POST.get('reached_marks')
        if reached_rank_id and order_id and reached_division and reached_marks:
            order = get_object_or_404(WildRiftDivisionOrder, pk=order_id)
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
            order = get_object_or_404(WildRiftDivisionOrder, pk=order_id)
            finish_image = request.FILES.get('finish_image')
            if finish_image:
                order.finish_image = finish_image
                order.save()
                return redirect(reverse_lazy('booster.orders'))
    return JsonResponse({'success': False})

def drop_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            order = get_object_or_404(WildRiftDivisionOrder, pk=order_id)
            order.booster = None
            order.is_drop = True
            order.save()
            return redirect(reverse_lazy('booster.orders'))
    return JsonResponse({'success': False})

def confirm_details(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            order = get_object_or_404(WildRiftDivisionOrder, pk=order_id)
            order.message = None
            order.data_correct = True
            order.save()
            return redirect(reverse_lazy('booster.orders'))
    return JsonResponse({'success': False})

def ask_customer(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            order = get_object_or_404(WildRiftDivisionOrder, pk=order_id)
            order.message = 'Pleace Specify Your Details'
            order.data_correct = False
            order.save()
            return redirect(reverse_lazy('booster.orders'))
    return JsonResponse({'success': False})