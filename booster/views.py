from django.shortcuts import render, HttpResponse
from .forms import Registeration_Booster
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from wildRift.models import WildRiftDivisionOrder

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
    orders = WildRiftDivisionOrder.objects.filter(booster=request.user)
    context = {
        'orders': orders
    }
    return render('booster/booster-order.html', context=context)
