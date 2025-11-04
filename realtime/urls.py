from django.urls import path
from . import views

app_name = 'realtime'

urlpatterns = [
    path('test/', views.realtime_test, name='realtime_test'),
]



