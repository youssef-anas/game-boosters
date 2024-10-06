import json
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import PromoCode, BaseOrder
import math
from csgo2.utils import get_division_prices, get_premier_prices, get_faceit_prices

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

def get_division_order_result_by_rank(data):
    current_rank = data['current_rank']
    desired_rank = data['desired_rank']

    duo_boosting = data['duo_boosting']
    select_booster = data['select_booster']
    turbo_boost = data['turbo_boost']
    streaming = data['streaming']

    extend_order_id = data['extend_order']
    server = data['server']
    promo_code = data['promo_code']

    duo_boosting_value = 0
    select_booster_value = 0
    turbo_boost_value = 0
    streaming_value = 0

    promo_code_amount = 0
    promo_code_id = 0

    total_percent = 0

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
            promo_code_obj = PromoCode.objects.get(code=promo_code)
            promo_code_amount = promo_code_obj.discount_amount
            promo_code_id = promo_code_obj.id
        except PromoCode.DoesNotExist:
            promo_code_amount = 0
            promo_code_id = 0
    

    # Read data from utils file
    division_price = get_division_prices()
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
    invoice = f'CS-13-D-{current_rank}-{1}-{0}-{desired_rank}-{1}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-{0}-{promo_code_id}-0-0-0-0-{timezone.now()}'

    invoice_with_timestamp = str(invoice)

    boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
    name = f'Cs Go2, BOOSTING FROM {rank_names[current_rank]} TO {rank_names[desired_rank]} {boost_string}'

    return({'name':name,'price':price,'invoice':invoice_with_timestamp})

def get_premier_order_result_by_rank(data):
    print("Data: ", data)
    # Read data from utils file
    premier_prices = get_premier_prices()
    premier_prices.insert(0,0)

    price1 = round(premier_prices[1] * 10 , 2)
    price2 = round(premier_prices[2] * 6 , 2)
    price3 = round(premier_prices[3] * 8 , 2)
    price4 = round(premier_prices[4] * 14 , 2)
    price5 = round(premier_prices[5] * 4 , 2)
    price6 = round(premier_prices[6] * 8 , 2)
    price7 = round(premier_prices[7] * 10.002 , 2) 
    full_price_val = [price1, price2, price3, price4, price5, price6, price7]

    def get_range_current(amount):
        MAX_LISTS = [4999, 7999, 11999, 18999, 20999, 24999, 30000]
        for idx, max_val in enumerate(MAX_LISTS, start=1):
            if amount <= max_val:
                val = max_val - amount
                return round(val / 500, 2), idx
        print('out_of_range')
        return None, None
        
    def get_range_desired(amount):
        MAX_LISTS = [4999, 7999, 11999, 18999, 20999, 24999, 30000]
        for idx, max_val in enumerate(MAX_LISTS, start=1):
            if amount <= max_val:
                val = amount-MAX_LISTS[idx-2]
                return round(val / 500, 2), idx
        print('out_of_range')
        return None, None


    # Ranks
    current_rank = data['current_rank']
    desired_rank = data['desired_rank']

    # Division
    current_division = data['current_division']
    desired_division = data['desired_division']

    duo_boosting = data['duo_boosting']
    select_booster = data['select_booster']
    turbo_boost = data['turbo_boost']
    streaming = data['streaming']

    extend_order_id = data['extend_order']
    server = data['server']
    promo_code = data['promo_code']

    duo_boosting_value = 0
    select_booster_value = 0
    turbo_boost_value = 0
    streaming_value = 0

    promo_code_amount = 0
    promo_code_id = 0

    total_percent = 0

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
            promo_code_obj = PromoCode.objects.get(code=promo_code)
            promo_code_amount = promo_code_obj.discount_amount
            promo_code_id = promo_code_obj.id
        except PromoCode.DoesNotExist:
            promo_code_amount = 0
            promo_code_id = 0

     
    curent_mmr_in_c_range, current_range = get_range_current(current_division)
    desired_mmr_in_d_range, derired_range = get_range_desired(desired_division)
    sliced_prices = full_price_val[current_range : derired_range - 1]
    sum_current = curent_mmr_in_c_range * premier_prices[current_range]
    sum_desired = desired_mmr_in_d_range * premier_prices[derired_range]
    clear_res = sum(sliced_prices)

    if current_range == derired_range:
        range_value = math.floor((desired_division - current_division ) / 500)
        price = round(range_value * premier_prices[current_range], 2)
    else:
        price = round(sum_current + sum_desired + clear_res,2)

    print("Price1: ", price)
    price += (price * total_percent)

    price -= price * (promo_code_amount/100)

    price = round(price, 2)
    print("Price2: ", price)
    if extend_order_id > 0:
        try:
            # get extend order 
            extend_order = BaseOrder.objects.get(id=extend_order_id)
            extend_order_price = extend_order.price
            print("extend_order_price: ", extend_order_price)
            price = round(price - extend_order_price , 2)
        except: ####
            pass

    booster_id = data['choose_booster']
    if booster_id > 0 :
       get_object_or_404(User,id=booster_id,is_booster=True)
    else:
        booster_id = 0

    invoice = f'CS-13-A-{current_rank}-{current_division}-{0}-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-{0}-{promo_code_id}-0-0-0-0-{timezone.now()}'

    invoice_with_timestamp = str(invoice)

    boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
    name = f'Cs Go2, BOOSTING FROM {rank_names[current_rank]} TO {rank_names[desired_rank]} {boost_string}'

    return({'name':name,'price':price,'invoice':invoice_with_timestamp})

def get_faceit_order_result_by_rank(data):
    current_level = data['current_level']
    desired_level = data['desired_level']

    duo_boosting = data['duo_boosting']
    select_booster = data['select_booster']
    turbo_boost = data['turbo_boost']
    streaming = data['streaming']

    extend_order_id = 0
    server = data['server']
    promo_code = data['promo_code']

    duo_boosting_value = 0
    select_booster_value = 0
    turbo_boost_value = 0
    streaming_value = 0

    promo_code_amount = 0
    promo_code_id = 0

    total_percent = 0

    boost_options = []

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

    faceit_prices = get_faceit_prices()
    
    sublist = faceit_prices[current_level : desired_level]
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
            price = round(price - extend_order_price, 2)
        except: ####
            pass
        
    booster_id = data['choose_booster']
    if booster_id > 0 :
       get_object_or_404(User,id=booster_id,is_booster=True)
    else:
        booster_id = 0

    invoice = f'CS-13-F-{current_level}-{0}-{0}-{desired_level}-{0}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-{0}-{promo_code_id}-0-0-0-0-{timezone.now()}'

    invoice_with_timestamp = str(invoice)
    
    boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
    name = f'CS Go2, BOOSTING FROM {current_level} FACEIT Level TO {desired_level} FACEIT Level {boost_string}'

    return({'name':name,'price':price,'invoice':invoice_with_timestamp})


from gameBoosterss.order_info.orders import BaseOrderInfo, ExtendOrder
from gameBoosterss.order_info.division import DivisionGameOrderInfo
from gameBoosterss.order_info.arena_v2 import Arena_V2_GameOrderInfo 
from gameBoosterss.order_info.levelup import LevelupGameOrderInfo


class Csgo2_DOI(BaseOrderInfo, DivisionGameOrderInfo, ExtendOrder):
    division_prices_data = get_division_prices()
    division_prices = [item for sublist in division_prices_data for item in sublist]
    division_prices.insert(0, 0)
    marks_data = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    division_number = 1

    
class Csgo2_AOI(BaseOrderInfo, Arena_V2_GameOrderInfo, ExtendOrder):
    arena_prices = get_premier_prices()
    # arena_prices.insert(0,0)

    price1 = round(arena_prices[0] * 10 , 2)
    price2 = round(arena_prices[1] * 6 , 2)
    price3 = round(arena_prices[2] * 8 , 2)
    price4 = round(arena_prices[3] * 14 , 2)
    price5 = round(arena_prices[4] * 4 , 2)
    price6 = round(arena_prices[5] * 8 , 2)
    price7 = round(arena_prices[6] * 10.002 , 2) 
    full_price_val = [price1, price2, price3, price4, price5, price6, price7]

    points_value = 500
    points_range = [4999, 7999, 11999, 18999, 20999, 24999, 30000]

class Csgo2_FOI(BaseOrderInfo, LevelupGameOrderInfo):
    faceit_prices = get_faceit_prices()