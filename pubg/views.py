from django.shortcuts import render
from django.http import JsonResponse
from pubg.models import PubgDivisionOrder, PubgRank, PubgTier
from pubg.controller.serializers import DivisionSerializer
from booster.models import OrderRating
from django.db.models import Sum, Case, When, IntegerField
from accounts.models import BaseUser
from pubg.utils import get_divisions_data, get_marks_data
from gameBoosterss.utils import NewMadBoostPayment


def get_divisions_data_view(request):
    return JsonResponse(get_divisions_data(), safe=False)

def get_marks_data_view(request):
    return JsonResponse(get_marks_data(), safe=False)



def pubgGetBoosterByRank(request):
    extend_order = request.GET.get('extend')
    try:
        order_get_rank_value = PubgDivisionOrder.objects.get(order_id=extend_order).get_rank_value()
    except PubgDivisionOrder.DoesNotExist:
        order_get_rank_value = None

    ranks = PubgRank.objects.all().order_by('id')
    divisions = PubgTier.objects.all().order_by('id')
    divisions_list = list(divisions.values())
    
    # Feedbacks
    feedbacks = OrderRating.objects.filter(order__game_id = 3)
    game_pk_condition = Case(
      When(booster_orders__game__pk=3, booster_orders__is_done=True, booster_orders__is_drop=False, then=1),
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
      "order_get_rank_value": order_get_rank_value,
      "feedbacks": feedbacks,
      "boosters": boosters,
    }
    return render(request,'pubg/GetBoosterByRank.html', context)


class PubgPaymentAPiView(NewMadBoostPayment):
    serializer_mapping = {
        'D': DivisionSerializer,
    }