from wildRift.models import WildRiftRank
import json

def wildrift_reached_percent(orders):
  ranks = WildRiftRank.objects.all()
  with open('static/valorant/data/divisions_data.json', 'r') as file:
    division_data = json.load(file)
    division_price = [item for sublist in division_data for item in sublist]
    division_price.insert(0,0)
    
  with open('static/valorant/data/marks_data.json', 'r') as file:
    marks_data = json.load(file)
    marks_price = [item for sublist in marks_data for item in sublist]
    marks_price.insert(0,0)

  for order in orders:

    current_rank = order.current_rank.id
    current_division = order.current_division
    current_marks = order.current_marks

    reached_rank = order.reached_rank.id
    reached_division = order.reached_division
    reached_marks = order.reached_marks

    start_division = ((current_rank-1) * 4) + current_division
    now_division = ((reached_rank-1) * 4)+ reached_division
    sublist_div = division_price[start_division:now_division]

    start_marks = (((current_rank-1) * 4) + current_marks + 1) + 1
    now_marks = (((reached_rank-1) * 4) + reached_marks + 1) + 1
    sublist_marks = marks_price[start_marks:now_marks]

    done_sum_div = sum(sublist_div)
    done_sum_marks = sum(sublist_marks)

    done_sum = done_sum_div + done_sum_marks

    percentage = round((done_sum / order.order.price) * 100 , 2)
    if percentage >= 100 :
        percentage = 100

    now_price = round(order.order.actual_price * (percentage / 100) , 2)

    order.order.money_owed = now_price
    order.order.save()