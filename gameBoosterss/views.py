from django.shortcuts import render
from booster.models import OrderRating
import json

def index(request):
  # Read data from JSON file
  with open('static/homepage/data/games.json', 'r') as file:
    games = json.load(file)

  feedbacks = OrderRating.objects.all()

  context= {
    "games": games,
    "feedbacks": feedbacks,
  }

  return render(request, 'homepage/index.html', context=context)
