import json
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import PromoCode, BaseOrder

User = get_user_model()

rank_names = [
    "Silver I",
    "Silver II",
    "Silver III",
    "Silver IV",
    "Silver Elite",
    "SE Master",
    "Gold NV I",
    "Gold NV II",
    "Gold NV III",
    "Gold NV Master",
    "Master Grd I",
    "Master Grd II",
    "Master Grd Elite",
    "D Master Grd",
    "Leg Eagle",
    "Leg Eagle Master",
    "Supre Master FC",
    "Global Elite"
]

def get_division_order_result_by_rank(data, extend_order_id):
    current_rank = data['current_rank']
    desired_rank = data['desired_rank']
    duo_boosting = data['duo_boosting']
    select_booster = data['select_booster']
    turbo_boost = data['turbo_boost']
    streaming = data['streaming']
    server = data['server']
    promo_code = data['promo_code']

    duo_boosting_value = 0
    select_booster_value = 0
    turbo_boost_value = 0
    streaming_value = 0
    # booster_champions_value = 0
    promo_code_amount = 0
    total_percent = 0
    promo_code_id = 0

    boost_options = []

    if duo_boosting:
        total_percent += 0.65
        boost_options.append('DUO BOOSTING')
        duo_boosting_value = 1

    if select_booster:
        total_percent += 0.10
        boost_options.append('SELECT BOOSTING')
        select_booster_value = 1

    if turbo_boost:
        total_percent += 0.20
        boost_options.append('TURBO BOOSTING')
        turbo_boost_value = 1

    if streaming:
        total_percent += 0.15
        boost_options.append('STREAMING')
        streaming_value = 1


    if promo_code != 'null':   
        try:
            promo_code_obj = PromoCode.objects.get(code=promo_code.lower())
            promo_code_amount = promo_code_obj.discount_amount
            promo_code_id = promo_code_obj.id
        except PromoCode.DoesNotExist:
            promo_code_amount = 0
            promo_code_id = 0
    

    # Read data from JSON file
    with open('static/csgo2/data/divisions_data.json', 'r') as file:
        division_price = json.load(file)
        flattened_data = [item for sublist in division_price for item in sublist]
        flattened_data.insert(0,0)
    ##
    start_division = ((current_rank-1)*1) + 1
    end_division = ((desired_rank-1)*1)+ 1
    sublist = flattened_data[start_division:end_division ]
    total_sum = sum(sublist)
    price = total_sum 
    price += (price * total_percent)
    price -= price * (promo_code_amount/100)
    price = round(price, 2)
    if extend_order_id > 0:
        try:
            # get extend order 
            extend_order = BaseOrder.objects.get(id=extend_order_id)
            extend_order_price = extend_order.price
            price = round((price / (1 + total_percent)) - (extend_order_price / (1 + total_percent)), 2)
        except: ####
            pass
    booster_id = data['choose_booster']
    if booster_id > 0 :
       get_object_or_404(User,id=booster_id,is_booster=True)
    else:
        booster_id = 0
    #####################################
    invoice = f'CS-13-D-{current_rank}-{1}-{0}-{desired_rank}-{1}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-{0}-{promo_code_id}-0-0-0-{timezone.now()}'
    invoice_with_timestamp = str(invoice)
    boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
    name = f'Cs Go2, BOOSTING FROM {rank_names[current_rank]} TO {rank_names[desired_rank]} {boost_string}'

    return({'name':name,'price':price,'invoice':invoice_with_timestamp})