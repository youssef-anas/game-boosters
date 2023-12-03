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
import uuid
from django.forms.models import model_to_dict

# Create your views here.

@csrf_exempt
def wildRiftGetBoosterByRank(request):
    ranks = WildRiftRank.objects.all()
    divisions  = WildRiftTier.objects.all().order_by('id')
    marks = WildRiftMark.objects.all().order_by('id')

    divisions_data = [
        [division.from_IV_to_III] if division.rank.rank_name == 'master' else
        [division.from_IV_to_III, division.from_III_to_II, division.from_II_to_II, division.from_I_to_IV_next]
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

    ranks = WildRiftRank.objects.all()
    ranks_map = {obj.id: model_to_dict(obj) for obj in ranks}

    divisions  = WildRiftTier.objects.all()
    divisions_map = {obj.id: model_to_dict(obj) for obj in divisions}

    marks = WildRiftMark.objects.all()
    marks_map = {obj.id: model_to_dict(obj) for obj in marks}

    dynamic_invoice = str(uuid.uuid4())


    print(ranks_map[1])
    print(divisions_map[1])
    print(marks_map[1])

    print(dynamic_invoice)

    
    paypal_dict = {
        "business": settings.PAYPAL_EMAIL,
        "amount": "120.00",
        "item_name": "FROM SILVER II MARKS 0 TO GOLD III",
        "invoice": dynamic_invoice,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('wildrift.payment.success')),
        "cancel_return": request.build_absolute_uri(reverse('wildrift.payment.canceled')),
    }
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "wildRift/paypal.html", context)

def payment_successed(request):
    return HttpResponse('payment success')

def payment_canceled(request):
    return HttpResponse('payment success')