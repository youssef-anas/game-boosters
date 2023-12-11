from django.shortcuts import render, redirect , HttpResponse, get_object_or_404
from django.urls import reverse, reverse_lazy
from .forms import Registeration_Booster
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from wildRift.models import WildRiftDivisionOrder, WildRiftRank
from django.http import JsonResponse

# Create your views here.

@csrf_exempt
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
