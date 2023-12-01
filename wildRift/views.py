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
from wildRift.models import WildRiftRank, WildRiftTier, WildRiftMark 
import json

# Create your views here.

@csrf_exempt
def wildRiftGetBoosterByRank(request):
    ranks = WildRiftRank.objects.all()
    divisions  = WildRiftTier.objects.all()
    marks = WildRiftMark.objects.all()

    divisions_data = [
        {'id': division.id, 'name': division.rank.rank_name, 'IV': division.from_IV_to_III, 'III': division.from_III_to_II,
         'II': division.from_II_to_II, 'I': division.from_I_to_IV_next}
        for division in divisions
    ]

    marks_data = [
        {'id': mark.id, 'rank': mark.rank.rank_name, 'mark_1': mark.mark_1, 'mark_2': mark.mark_2, 'mark_3': mark.mark_3, 'mark_4': mark.mark_4, 'mark_5': mark.mark_5}
        for mark in marks
    ]

    with open('static/wildRift/data/divisions_data.json', 'w') as json_file:
        json.dump(divisions_data, json_file)

    with open('static/wildRift/data/marks_data.json', 'w') as json_file:
        json.dump(marks_data, json_file)

    divisions_list = list(divisions.values())
    print(divisions_list)
    context = {
        "ranks": ranks,
        "divisions": divisions_list,
    }
    if request.method == 'POST': 
        return HttpResponse("hi")
    return render(request,'wildRift/GetBoosterByRank.html', context)



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