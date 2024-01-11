from wildRift.models import WildRiftDivisionOrder
from valorant.models import ValorantDivisionOrder, ValorantPlacementOrder
from pubg.models import PubgDivisionOrder
from leagueOfLegends.models import LeagueOfLegendsDivisionOrder, LeagueOfLegendsPlacementOrder
from accounts.models import BaseUser, BaseOrder
from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
channel_layer = get_channel_layer()


def create_order(invoice, payer_id, customer, status='New',name = None):
    # Split the invoice string by the hyphen ("-") delimiter
    invoice_values = invoice.split('-')

    # Extract specific values
    game_id = int(invoice_values[1])
    type = str(invoice_values[2])
    booster_id = int(invoice_values[12])
    extend_order_id = int(invoice_values[14])
    price = float(invoice_values[13])

    if type == 'D':
        current_rank =  int(invoice_values[3])
        current_division = int(invoice_values[4])
        current_marks = int(invoice_values[5])
        desired_rank = int(invoice_values[6])
        desired_division = int(invoice_values[7])
    elif type == 'P':
        last_rank = int(invoice_values[3])
        number_of_match = int(invoice_values[4])

    duo_boosting = bool(int(invoice_values[8]))
    select_booster = bool(int(invoice_values[9]))
    turbo_boost = bool(int(invoice_values[10]))
    streaming = bool(int(invoice_values[11]))

    # Wildrift
    if game_id == 1:
        Game = WildRiftDivisionOrder 
    # Volarent
    elif game_id == 2:
        # Extra Fields +
        print('Choose Agents: ', invoice_values[16])
        choose_agents = bool(int(invoice_values[16]))
        if type == 'D':
            Game = ValorantDivisionOrder
        elif type == 'P':
            Game = ValorantPlacementOrder
    # Pubg
    elif game_id == 3:
        choose_agents = bool(int(invoice_values[16]))
        Game = PubgDivisionOrder
    # LOL
    elif game_id == 4:
        # Extra Fields +
        print('Choose Champions: ', invoice_values[16])
        choose_champions = bool(int(invoice_values[16]))
        if type == 'D':
            Game = LeagueOfLegendsDivisionOrder
        elif type == 'P':
            Game = LeagueOfLegendsPlacementOrder
    elif game_id == 5:
        Game = 'anoter model' # for future work
    else:
        pass

    try:
        booster = BaseUser.objects.get(id=booster_id)
    except BaseUser.DoesNotExist:
        booster = None

    try:
        if status != 'Continue':
            extend_order = BaseOrder.objects.get(id=extend_order_id)
            extend_order.is_done = True
            extend_order.is_extended = True
            extend_order.money_owed = 0
            extend_order.status = 'Extend'
            extend_order.save()
            status = 'Extend'
            
            extend_order_money_owed = extend_order.money_owed
            extend_order_price = extend_order.price
            order_name = extend_order.name
            extend_order_booster = extend_order.booster
            extend_order_customer = extend_order.customer
            extend_order_customer_gamename = extend_order.customer_gamename
            extend_order_customer_password = extend_order.customer_password
            extend_order_server = extend_order.customer_server
            extend_order_data_correct = extend_order.data_correct

            extend_order_game = Game.objects.get(order = extend_order)
            extend_order_game_reached_rank = extend_order_game.reached_rank
            extend_order_game_reached_division = extend_order_game.reached_division
            extend_order_game_reached_marks = extend_order_game.reached_marks

    except BaseOrder.DoesNotExist:
        extend_order = None
    print("Check Condition: ",status == 'New' or status == 'Continue')
    if status == 'New' or status == 'Continue':
        print('Booster: ', booster)
        baseOrder = BaseOrder.objects.create(invoice=invoice, booster=booster, payer_id=payer_id, customer=customer,status=status, price=price, duo_boosting=duo_boosting,select_booster=select_booster,turbo_boost=turbo_boost,streaming=streaming, name=name)
        # Wildrift Without Placement 
        if game_id == 1:
            order = Game.objects.create(order=baseOrder,current_rank_id=current_rank,current_division=current_division, current_marks=current_marks,desired_rank_id=desired_rank, desired_division=desired_division,reached_rank_id=current_rank, reached_division=current_division,reached_marks=current_marks)
        # Valorant - Division
        elif game_id == 2 and type == 'D':
            order = Game.objects.create(order=baseOrder,current_rank_id=current_rank,current_division=current_division, current_marks=current_marks,desired_rank_id=desired_rank, desired_division=desired_division,reached_rank_id=current_rank, reached_division=current_division,reached_marks=current_marks, choose_agents=choose_agents)
        # Valorant - Placement
        elif game_id == 2 and type == 'P':
            order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,choose_agents=choose_agents)
        # Pubg Without Placement 
        elif game_id == 3:
            order = Game.objects.create(order=baseOrder,current_rank_id=current_rank,current_division=current_division, current_marks=current_marks, desired_rank_id=desired_rank, desired_division=desired_division,reached_rank_id=current_rank, reached_division=current_division, reached_marks=current_marks, choose_agents=choose_agents)
        # LOL - Division
        elif game_id == 4 and type == 'D':
            order = Game.objects.create(order=baseOrder,current_rank_id=current_rank,current_division=current_division, current_marks=current_marks,desired_rank_id=desired_rank, desired_division=desired_division,reached_rank_id=current_rank, reached_division=current_division,reached_marks=current_marks, choose_champions=choose_champions)
        # LOL - Placement
        elif game_id == 4 and type == 'P':
            order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,choose_champions=choose_champions)   


    elif status == 'Extend':
        print(f"order extended from:  {order_name}")
        baseOrder = BaseOrder.objects.create(invoice=invoice, booster=extend_order_booster,duo_boosting=duo_boosting, select_booster=select_booster, turbo_boost=turbo_boost,streaming=streaming, customer=extend_order_customer,payer_id=payer_id, customer_gamename=extend_order_customer_gamename, customer_password=extend_order_customer_password, customer_server=extend_order_server,name = order_name, money_owed =extend_order_money_owed, price = price + extend_order_price, data_correct = extend_order_data_correct, status = "Extend")

        # Wildrift Without Placement 
        if game_id == 1:
            order = Game.objects.create(order=baseOrder,current_rank_id=current_rank,current_division=current_division, current_marks=current_marks,desired_rank_id=desired_rank, desired_division=desired_division,reached_rank=extend_order_game_reached_rank, reached_division=extend_order_game_reached_division, reached_marks=extend_order_game_reached_marks)
        # Valorant - Division
        elif game_id == 2 and type == 'D':
            order = Game.objects.create(order=baseOrder,current_rank_id=current_rank,current_division=current_division, current_marks=current_marks,desired_rank_id=desired_rank, desired_division=desired_division,reached_rank=extend_order_game_reached_rank, reached_division=extend_order_game_reached_division, reached_marks=extend_order_game_reached_marks, choose_agents=choose_agents)
        # Valorant - Placement
        elif game_id == 2 and type == 'P':
            order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,choose_agents=choose_agents)       
        # Pubg Without Placement 
        elif game_id == 3:
            order = Game.objects.create(order=baseOrder,current_rank_id=current_rank,current_division=current_division, current_marks=current_marks,desired_rank_id=desired_rank, desired_division=desired_division,reached_rank=extend_order_game_reached_rank, reached_division=extend_order_game_reached_division, reached_marks=extend_order_game_reached_marks, choose_agents=choose_agents)
        # LOL - Division
        elif game_id == 4 and type == 'D':
            order = Game.objects.create(order=baseOrder,current_rank_id=current_rank,current_division=current_division, current_marks=current_marks,desired_rank_id=desired_rank, desired_division=desired_division,reached_rank=extend_order_game_reached_rank, reached_division=extend_order_game_reached_division, reached_marks=extend_order_game_reached_marks, choose_champions=choose_champions)
        # LOL - Placement
        elif game_id == 4 and type == 'P':
            order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,choose_champions=choose_champions) 

    order.save_with_processing()
    baseOrder.customer_wallet()
    return order

#--------------------------------------------------------------------------
def live_orders():
    orders = BaseOrder.objects.filter(booster=None).order_by('-created_at')
    all_orders_dict = []
    for order in orders:
        order_dict = {
            "id": order.pk,
            'name': order.game_name,
            'server': order.customer_server,
            'status': order.status,
            'price': order.price,
            'game_name':order.game_name,
            'details':order.details,
            'url':f'{order.game_name}/{order.pk}/',
        }
        all_orders_dict.append(order_dict)
    return all_orders_dict 

def refresh_order_page():
    all_orders_dict = live_orders()
    async_to_sync(channel_layer.group_send)(
        'orders',
        {
            'type': 'order_list',
            'order': all_orders_dict,
        }
    )