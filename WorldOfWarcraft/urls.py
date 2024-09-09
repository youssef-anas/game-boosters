from django.urls import path
from WorldOfWarcraft.views import WowPaymenApiView, wowGetBoosterByRank

urlpatterns = [
  path('', wowGetBoosterByRank, name='wow'),
  path('payment/', WowPaymenApiView.as_view(), name='wow-paypal-redirect'),
]