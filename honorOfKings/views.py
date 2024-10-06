from django.shortcuts import render, redirect
from django.http import JsonResponse

from honorOfKings.models import *
from honorOfKings.controller.serializers import DivisionSerializer
from honorOfKings.controller.order_information import *
from booster.models import OrderRating
from accounts.models import TokenForPay
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from accounts.models import BaseUser
from honorOfKings.utils import get_hok_divisions_data, get_hok_marks_data
from gameBoosterss.utils import NewMadBoostPayment


def get_hok_divisions_data_view(request):
    divisions_data = get_hok_divisions_data()
    return JsonResponse(divisions_data, safe=False)

def get_hok_marks_data_view(request):
    marks_data = get_hok_marks_data()
    return JsonResponse(marks_data, safe=False)


def honerOfKingeGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = HonorOfKingsDivisionOrder.objects.get(order_id=extend_order)
  except:
    order = None
  ranks = HonorOfKingsRank.objects.all().order_by('id')
  divisions  = HonorOfKingsTier.objects.all().order_by('id')
  divisions_list = list(divisions.values())

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 11)
  game_pk_condition = Case(
    When(booster_orders__game__pk=11, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
  )
    
  boosters = BaseUser.objects.filter(
      is_booster = True,
      booster__is_hok_player=True,
      booster__can_choose_me=True
      ).annotate(
      order_count=Sum(game_pk_condition)
      ).order_by('id')
  
  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "order":order,
    "feedbacks": feedbacks,
    "boosters": boosters,
  }
  return render(request,'honorOfKings/GetBoosterByRank.html', context)


class HOKPaymentAPiView(NewMadBoostPayment):
    serializer_mapping = {
        'D': DivisionSerializer,
    }