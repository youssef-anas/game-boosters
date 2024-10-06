from django.shortcuts import render, redirect
from django.http import JsonResponse
from overwatch2.models import Overwatch2DivisionOrder, Overwatch2Rank, Overwatch2Tier, Overwatch2Placement
from overwatch2.controller.serializers import DivisionSerializer, PlacementSerializer
from overwatch2.controller.order_information import *
from accounts.models import BaseOrder
from booster.models import OrderRating
from django.db.models import Avg, Sum, Case, When, Value, IntegerField
from accounts.models import BaseUser
from .utils import get_overwatch2_divisions_data, get_overwatch2_marks_data, get_overwatch2_placements_data
from gameBoosterss.utils import NewMadBoostPayment



def get_overwatch2_divisions(request):
    divisions_data = get_overwatch2_divisions_data()
    return JsonResponse(divisions_data, safe=False)

def get_overwatch2_marks(request):
    marks_data = get_overwatch2_marks_data()
    return JsonResponse(marks_data, safe=False)

def get_overwatch2_placements(request):
    placements_data = get_overwatch2_placements_data()
    return JsonResponse(placements_data, safe=False)



def overwatch2GetBoosterByRank(request):
  order_get_rank_value = None
  extend_order = request.GET.get('extend')
  if extend_order:
    try:
      BaseOrder.objects.get(id = extend_order, customer= request.user)
      order_get_rank_value = Overwatch2DivisionOrder.objects.get(order_id=extend_order).get_rank_value()
    except Exception as e:
      print(e)
      return redirect('homepage.index')
  ranks = Overwatch2Rank.objects.all().order_by('id')
  divisions  = Overwatch2Tier.objects.all().order_by('id')
  placements = Overwatch2Placement.objects.all().order_by('id')
  divisions_list = list(divisions.values())

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 12)

  game_pk_condition = Case(
    When(booster_orders__game__pk=12, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
    default=0,
    output_field=IntegerField()
  )
    
  boosters = BaseUser.objects.filter(
      is_booster = True,
      booster__is_overwatch2_player=True,
      booster__can_choose_me=True
      ).annotate(
      order_count=Sum(game_pk_condition)
      ).order_by('id')


  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "placements": placements,
    "order_get_rank_value":order_get_rank_value,
    "feedbacks": feedbacks,
    "boosters": boosters,
  }
  return render(request,'overwatch2/GetBoosterByRank.html', context)


class Overwatch2PaymentAPiView(NewMadBoostPayment):
    serializer_mapping = {
        'D': DivisionSerializer,
        'P': PlacementSerializer,
    }