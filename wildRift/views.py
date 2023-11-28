from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.http import JsonResponse
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

ranks = [
    {
        "id": 1,
        "name": "iron",
        "image": "iron.webp", 
        "division": 4,
        "marks": 3
    },
    {
        "id": 2,
        "name": "bronze",
        "image": "bronze.webp",
        "division": 4,
        "marks": 4 
    },
    {
        "id": 3,
        "name": "silver",
        "image": "silver.webp",
        "division": 4,
        "marks": 4 
    },
    {
        "id": 4,
        "name": "gold",
        "image": "gold.webp",
        "division": 4,
        "marks": 5 
    },
    {
        "id": 5,
        "name": "platinum",
        "image": "platinum.webp",
        "division": 4,
        "marks": 5
    },
    {
        "id": 6,
        "name": "emerald",
        "image": "emerald.webp",
        "division": 4,
        "marks": 6 
    },
    {
        "id": 7,
        "name": "diamond",
        "image": "diamond.webp",
        "division": 4,
        "marks": 0 
    },
    {
        "id": 8,
        "name": "master",
        "image": "master.webp",
        "division": 0,
        "marks": 0 
    }
]

@csrf_exempt
def wildRiftGetBoosterByRank(request):

    if request.method == 'POST': 
        
        return HttpResponse("hi")
    return render(request,'wildRift/GetBoosterByRank.html', context={"ranks": ranks})



@csrf_exempt
def view_that_asks_for_money(request):
    # What you want the button to do.
    paypal_dict = {
        "business":settings.PAYPAL_EMAIL ,
        "amount": "120.00",
        "item_name": "from Diamond to Master",
        "invoice": "1",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('accounts.profile')),
        "cancel_return": request.build_absolute_uri(reverse('accounts.register')),
        # "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "wildRift/paypal.html", context)