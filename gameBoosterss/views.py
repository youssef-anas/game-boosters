from django.shortcuts import render
from booster.models import OrderRating
from games.models import Game
from accounts.models import BaseOrder
import json

def index(request):

  games = Game.objects.all()

  last_orders_query = BaseOrder.objects.filter(is_done=True, is_drop=False)

  last_orders = []
  for order in last_orders_query:
    content_type = order.content_type
    if content_type:
      last_order = content_type.model_class().objects.get(order_id=order.object_id)

      last_orders.append(last_order)

  feedbacks = OrderRating.objects.all()

  context= {
    "games": games,
    "feedbacks": feedbacks,
    "last_orders": last_orders,
  }

  return render(request, 'gameboosterss/index.html', context=context)

def last_orders(request):
  last_orders_query = BaseOrder.objects.filter(is_done=True, is_drop=False)

  last_orders = []
  for order in last_orders_query:
    content_type = order.content_type
    if content_type:
      last_order = content_type.model_class().objects.get(order_id=order.object_id)

      last_orders.append(last_order)

  context = {
    "last_orders": last_orders
  }

  return render(request, 'gameboosterss/last-orders.html', context=context)

def privacy_policy(request):
  return render(request, 'gameboosterss/privacy-policy.html')

def custom_handler400(request, exception):
  return render(request, 'erorr_handler/400.html', status=400)

def custom_handler403(request, exception):
  return render(request, 'erorr_handler/403.html', status=403)

def custom_handler404(request, exception):
  return render(request, 'erorr_handler/404.html', status=404)

def custom_handler500(request):
  return render(request, 'erorr_handler/500.html', status=500)