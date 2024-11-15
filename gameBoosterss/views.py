from django.shortcuts import render
from booster.models import OrderRating
from games.models import Game
from accounts.models import BaseOrder
from django.views.generic import TemplateView, View
from django.contrib.admin.models import LogEntry

def index(request):
  games = Game.objects.all().order_by('id')

  last_orders_query = BaseOrder.objects.filter(is_done=True, is_drop=False).order_by('id')

  last_orders = []
  for order in last_orders_query:
    content_type = order.content_type
    if content_type:
      last_order = content_type.model_class().objects.get(order = order)

      last_orders.append(last_order)

  feedbacks = OrderRating.objects.all().order_by('id')

  context= {
    "games": games,
    "feedbacks": feedbacks,
    "last_orders": last_orders,
  }

  return render(request, 'gameboosterss/index.html', context=context)

def last_orders(request):
  last_orders_query = BaseOrder.objects.filter(is_done=True, is_drop=False).order_by('id')

  last_orders = []
  for order in last_orders_query:
    content_type = order.content_type
    if content_type:
      last_order = content_type.model_class().objects.get(order = order)

      last_orders.append(last_order)

  context = {
    "last_orders": last_orders
  }

  return render(request, 'gameboosterss/last-orders.html', context=context)

def privacy_policy(request):
  return render(request, 'gameboosterss/privacy-policy.html')

def terms_service(request):
  return render(request, 'gameboosterss/terms-service.html')

def custom_handler400(request, exception):
  return render(request, 'erorr_handler/400.html', status=400)

def custom_handler403(request, exception):
  return render(request, 'erorr_handler/403.html', status=403)

def custom_handler404(request, exception):
  return render(request, 'erorr_handler/404.html', status=404)

def custom_handler500(request):
  return render(request, 'erorr_handler/500.html', status=500)

import os
import zipfile
from django.http import HttpResponse
from django.conf import settings

def download_media_zip(request):
    # Path to the media directory
    media_path = os.path.join(settings.MEDIA_ROOT)

    # Create a temporary zip file
    zip_filename = os.path.join(settings.MEDIA_ROOT, 'media.zip')
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk(media_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, media_path))

    # Read the zip file
    with open(zip_filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=media.zip'
        return response
    


def social_auth_exception_handler(request):
  # Handle authentication exceptions here
  # You can access exception information from request.social_auth_exception attribute
  
  # For example, you can log the exception or display an error message to the user
  
  return HttpResponse('An authentication exception occurred. Please try again later.')


def facebook_data_deletion_handler(request):
    if request.method == 'POST':
        # Process the data deletion request from Facebook
        # Parse the request parameters and perform necessary actions
        user_id = request.POST.get('user_id')
        # Delete user data associated with the user_id
        
        # Return a success response
        return HttpResponse('Data deletion request processed successfully')
    else:
        # Handle invalid requests (e.g., GET requests)
        return HttpResponse('Method not allowed', status=405)


class StoreView(TemplateView):
    template_name = 'store.html'

class HowWeWorkView(TemplateView):
    template_name = 'gameboosterss/how-we-work.html'   