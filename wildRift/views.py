from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from wildRift.models import *
import json
from wildRift.controller.serializers import RankSerializer
from customer.models import Champion
from wildRift.controller.order_information import *
from booster.models import OrderRating
from accounts.models import TokenForPay
from django.db.models import Count, Sum, Case, When, FloatField, F, Q, Avg, IntegerField
from django.db.models.functions import Coalesce
from accounts.models import BaseUser
from .utils import get_wildrift_divisions_data, get_wildrift_marks_data
from gameBoosterss.utils import NewMadBoostPayment
from .controller.order_information import get_order_result_by_rank


def get_wildrift_divisions_data_view(request):
    divisions_data = get_wildrift_divisions_data()
    return JsonResponse(divisions_data, safe=False)

def get_wildrift_marks_data_view(request):
    marks_data = get_wildrift_marks_data()
    return JsonResponse(marks_data, safe=False)



def wildRiftGetBoosterByRank(request):
    extend_order = request.GET.get('extend')
    try:
        order = WildRiftDivisionOrder.objects.get(order_id=extend_order)
    except:
        order = None
    ranks = WildRiftRank.objects.all().order_by('id')
    divisions  = WildRiftTier.objects.all().order_by('id')
    champions = Champion.objects.filter(game__id =1).order_by('id')

    game_pk_condition = Case(
        When(booster_orders__game__pk=1, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
        default=0,
        output_field=IntegerField()
    )

    boosters = BaseUser.objects.filter(
        is_booster=True,
        booster__is_wr_player=True,
        booster__can_choose_me=True
    ).annotate(
        order_count=Sum(game_pk_condition)
    ).order_by('id')

    divisions_list = list(divisions.values())

    # Feedbacks
    feedbacks = OrderRating.objects.filter(order__game_id = 1)
    context = {
        "ranks": ranks,
        "divisions": divisions_list,
        "order": order,
        "feedbacks": feedbacks,
        'champions' : champions,
        'boosters': boosters,
    }
    return render(request,'wildRift/GetBoosterByRank.html', context)

class WRPaymentAPiView(NewMadBoostPayment):
    serializer_mapping = {
        'D': RankSerializer,
    }