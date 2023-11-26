from django.shortcuts import render, HttpResponse

# Create your views here.


def wildRiftGetBoosterByRank(request):
    if request.method == 'POST': 
        
        return HttpResponse("You choose from rank RANK_NAME to rank RANK_NAME with $.99")
    return render(request,'wildRift/GetBoosterByRank.html')

