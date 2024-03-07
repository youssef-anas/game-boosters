from django.shortcuts import render
from booster.models import OrderRating
from games.models import Game
from accounts.models import BaseOrder

import json

def index(request):

  games = Game.objects.all()

  base_orders_query = list(BaseOrder.objects.filter(is_done=True))

  divsion_orders = []

  placement_orders = []

  for order in base_orders_query:
    content_type = order.content_type
    if content_type:
      last_order = content_type.model_class().objects.get(order_id=order.object_id)

      if last_order.order.game_type == 'D':
        divsion_orders.append(last_order)

      elif last_order.order.game_type == 'P':
        placement_orders.append(last_order)


  last_orders = list(divsion_orders) + list(placement_orders)

  feedbacks = OrderRating.objects.all()

  context= {
    "games": games,
    "feedbacks": feedbacks,
    "last_orders": last_orders,
  }

  return render(request, 'homepage/index.html', context=context)


def custom_handler400(request, exception):
    return render(request, 'erorr_handler/400.html', status=400)

def custom_handler403(request, exception):
    return render(request, 'erorr_handler/403.html', status=403)

def custom_handler404(request, exception):
    return render(request, 'erorr_handler/404.html', status=404)

def custom_handler500(request):
    return render(request, 'erorr_handler/500.html', status=500)


