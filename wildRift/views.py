from django.shortcuts import render, HttpResponse

# Create your views here.

ranks = [
    {
        "id": 1,
        "name": "iron",
        "image": "iron.webp", 
        "division": 4,
        "marks": 3
    },
    {
        "id": 2,
        "name": "bronze",
        "image": "bronze.webp",
        "division": 4,
        "marks": 4 
    },
    {
        "id": 3,
        "name": "silver",
        "image": "silver.webp",
        "division": 4,
        "marks": 4 
    },
    {
        "id": 4,
        "name": "gold",
        "image": "gold.webp",
        "division": 4,
        "marks": 5 
    },
    {
        "id": 5,
        "name": "platinum",
        "image": "platinum.webp",
        "division": 4,
        "marks": 5
    },
    {
        "id": 6,
        "name": "emerald",
        "image": "emerald.webp",
        "division": 4,
        "marks": 6 
    },
    {
        "id": 7,
        "name": "diamond",
        "image": "diamond.webp",
        "division": 4,
        "marks": 0 
    },
    {
        "id": 8,
        "name": "master",
        "image": "master.webp",
        "division": 0,
        "marks": 0 
    }
]
def wildRiftGetBoosterByRank(request):

    if request.method == 'POST': 
        
        return HttpResponse("You choose from rank RANK_NAME to rank RANK_NAME with $.99")
    return render(request,'wildRift/GetBoosterByRank.html', context={"ranks": ranks})

