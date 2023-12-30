from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from valorant.models import *

# Create your views here.
@csrf_exempt
def valorantGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
      order = ValorantDivisionOrder.objects.get(order_id=extend_order)
  except:
      order = None
  ranks = ValorantRank.objects.all().order_by('id')
  divisions  = ValorantTier.objects.all().order_by('id')
  marks = ValorantMark.objects.all().order_by('id')
  placements = ValorantPlacement.objects.all().order_by('id')

  divisions_data = [
    [division.from_I_to_II, division.from_II_to_III, division.from_III_to_I_next]
    for division in divisions
  ]

  marks_data = [
    [0,mark.marks_0_20, mark.marks_21_40, mark.marks_41_60, mark.marks_61_80, mark.marks_81_100]
    for mark in marks
  ]

  with open('static/valorant/data/divisions_data.json', 'w') as json_file:
      json.dump(divisions_data, json_file)

  with open('static/valorant/data/marks_data.json', 'w') as json_file:
      json.dump(marks_data, json_file)

  divisions_list = list(divisions.values())
  context = {
      "ranks": ranks,
      "divisions": divisions_list,
      "placements": placements,
      "order":order,
  }
  return render(request,'valorant/GetBoosterByRank.html', context)