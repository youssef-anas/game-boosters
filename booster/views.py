from django.shortcuts import render, HttpResponse, get_object_or_404
from .forms import Registeration_Booster
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


def register_booster_view(request):
    form = Registeration_Booster()
    if request.method == 'POST':
        form = Registeration_Booster(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            print(user.email_verified_at)
            user.is_active = False  # Mark the user as inactive until they activate their account
            user.save()
            # Send activation email
            return HttpResponse(f'account created with username {user.username}')
        return render(request, 'booster/registeration_booster.html', {'form': form}) # return error 
    return render(request, 'booster/registeration_booster.html', {'form': form})


@login_required
def profile_booster_view(request):
    return render(request, 'booster/booster_profile.html')


@login_required
def get_rate(request, order_id):
    order_obj = get_object_or_404(WildRiftDivisionOrder, id=order_id)
    customer =order_obj.customer
    booster =order_obj.booster
    if not (customer and booster):
        print(order_obj.customer)
        print(order_obj.booster)
        return HttpResponse(f'cant set rate to order {order_id}, with customer {customer} and booster {booster}')
    if order_obj.is_done:
        if request.method == 'POST':
            serializer = RatingSerializer(data=request.POST)
            if serializer.is_valid():
                existing_rating = Rating.objects.filter(order=order_obj).first()
                if existing_rating:
                    return HttpResponse('Rate Already Added', status=status.HTTP_400_BAD_REQUEST)
                serializer.save(order=order_obj,customer=customer, booster=booster)
                return HttpResponse('Thank You, Wanna to create New order ?')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('Method Not Allowed', status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse('Order Not Done', status=status.HTTP_400_BAD_REQUEST)

        
# this for only test and will remove it        
def form_test(request):
    order = WildRiftDivisionOrder.objects.get(id=6)
    return render(request,'booster/rating_page.html', context={'order':order})
def booster_orders(request):
    orders = WildRiftDivisionOrder.objects.filter(booster=request.user).order_by('id')
    ranks = WildRiftRank.objects.all()
    context = {
        'orders': orders,
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
