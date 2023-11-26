from django.shortcuts import render
from django.http import HttpResponse

def index(request):
  games = ["League of legends", "Valorant", "Tft", "League of legends wild rift","Dota 2" ,"Hearthstone","World of warcraft", "Mobile legends", "Pubg mobile","Rocket league"]
  return render(request, 'homepage/index.html', context={games: games})