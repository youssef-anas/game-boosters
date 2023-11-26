from django.shortcuts import render
from django.http import HttpResponse

def index(request):
  games = [
    {
      "id" : 1,
      "name": "League of Legends",
      "image": "League of legends.jpeg"
    },
    {
      "id": 2,
      "name": "Valorant",
      "image": "Valorant.jpg"
    },
    {
      "id": 3,
      "name": "TFT",
      "image": "tft.jpg"
    },
    {
      "id": 4,
      "name": "Wild Rift",
      "image": "League of legends wild rift.jpg"
    },
    {
      "id": 5,
      "name": "Dota 2",
      "image": "Dota 2.jpg"
    },
    {
      "id": 6,
      "name": "Hearthstone",
      "image": "Hearthstone.jpg"
    },
    {
      "id": 7,
      "name": "World of Warcraft",
      "image": "World of Warcraft.jpg"
    },
    {
      "id": 8,
      "name": "Mobile Legends",
      "image": "Mobile Legends.webp"
    },
    {
      "id": 9,
      "name": "Pubg Mobile",
      "image": "Pubg Mobile.avif"
    },
    {
      "id": 10,
      "name": "Rocket League",
      "image": "Rocket League.webp"
    },
  ]

  return render(request, 'homepage/index.html', context={"games": games})
