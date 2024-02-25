from django.shortcuts import render
from django.http import HttpResponse

def index(request):
  games = [
    {
      "id" : 1,
      "name": "League of Legends",
      "image": "League of legends.jpeg",
      "link": "lol"
    },
    {
      "id": 2,
      "name": "Valorant",
      "image": "Valorant.jpg",
      "link": "valorant"
    },
    {
      "id": 3,
      "name": "TFT",
      "image": "tft.jpg",
      "link": "tft"
    },
    {
      "id": 4,
      "name": "Wild Rift",
      "image": "League of legends wild rift.jpg",
      "link": "wildRift"
    },
    {
      "id": 5,
      "name": "Dota 2",
      "image": "Dota 2.jpg",
      "link": "dota2"
    },
    {
      "id": 6,
      "name": "Hearthstone",
      "image": "Hearthstone.jpg",
      "link": "hearthstone"
    },
    {
      "id": 7,
      "name": "World of Warcraft",
      "image": "World of Warcraft.jpg",
      "link": "wow"
    },
    {
      "id": 8,
      "name": "Mobile Legends",
      "image": "Mobile Legends.webp",
      "link": "mobileLegends"
    },
    {
      "id": 9,
      "name": "Pubg Mobile",
      "image": "Pubg Mobile.avif",
      "link": "pubg"
    },
    {
      "id": 10,
      "name": "Rocket League",
      "image": "Rocket League.webp",
      "link": "rocketLeague"
    },
    {
      "id": 11,
      "name": "Dota 2",
      "image": "Dota2.webp",
      "link": "dota2"
    },
  ]

  return render(request, 'homepage/index.html', context={"games": games})
