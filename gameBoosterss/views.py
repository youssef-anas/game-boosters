from django.shortcuts import render
from django.http import HttpResponse

def index(request):
  games = ["League of Legends", "Valorant", "TFT", "League of Legends Wild Rift","Dota 2" ,"Hearthstone","World of Warcraft", "Mobile Legends", "Pubg Mobile","Rocket League"]
  return render(request, 'homepage/index.html')