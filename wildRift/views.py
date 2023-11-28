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


@csrf_exempt
def wildRiftGetBoosterByRank(request):
    if request.method == 'POST': 
        return HttpResponse("hi")
    return render(request, 'wildRift/GetBoosterByRank.html')



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