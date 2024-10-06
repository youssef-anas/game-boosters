from accounts.models import BaseUser, BaseOrder
from django.contrib.contenttypes.models import ContentType
from gameBoosterss.utils import get_game
from accounts.models import PromoCode
from customer.models import Champion
import random
import ast

def create_order(invoice, payer_id, customer, status='New', name = None, extra = 1):
    # try :
        invoice_values = invoice.split('-')
        game_id = int(invoice_values[1])
        game_type = str(invoice_values[2])


        # wow id 6 and game type = R
        if game_id == 6 and game_type == 'R':
            map = int(invoice_values[3])
            bosses_idss = str(invoice_values[4])
            bosses_ids = ast.literal_eval(bosses_idss)
            loot_priority = bool(int(invoice_values[22]))
            boost_method = str(invoice_values[23])
            difficulty_chosen = float(invoice_values[5])
        if game_id == 6 and game_type == 'RB':
            bundle = int(invoice_values[3])
            loot_priority = bool(int(invoice_values[4]))
            boost_method = str(invoice_values[22])
        if game_id == 6 and game_type == 'DS':   
            keystone = int(invoice_values[3]) 
            keys = int(invoice_values[4])

            map_preferred = str(invoice_values[5])
            traders = str(invoice_values[6])
            traders_armor_type = str(invoice_values[7])
            maps = invoice_values[20]

            timed = bool(int(invoice_values[22]))
            boost_method = str(invoice_values[23])
            

        booster_id = int(invoice_values[12])
        extend_order_id = int(invoice_values[13])
        price = float(invoice_values[15])
        server = str(invoice_values[14])
        if game_type == 'D' or game_type == 'A':
            current_rank =  int(invoice_values[3])
            current_division = int(invoice_values[4])
            current_marks = int(invoice_values[5])
            desired_rank = int(invoice_values[6])
            desired_division = int(invoice_values[7])
        elif game_type == 'P' and game_id == 10:
            last_rank = int(invoice_values[3])
            last_division = int(invoice_values[5])
            number_of_match = int(invoice_values[4])
        elif game_type == 'P':
            last_rank = int(invoice_values[3])
            number_of_match = int(invoice_values[4])
        elif game_type == 'S':
            current_rank = int(invoice_values[3])
            number_of_wins = int(invoice_values[4])
        elif game_type == 'T':
            current_league = int(invoice_values[3])
        elif game_type == 'F':
            current_level =  int(invoice_values[3])
            desired_level = int(invoice_values[6])

        duo_boosting = bool(int(invoice_values[8]))
        select_booster = bool(int(invoice_values[9]))
        turbo_boost = bool(int(invoice_values[10]))
        streaming = bool(int(invoice_values[11]))
        
        select_champion = bool(int(invoice_values[16]))

        promo_code = int(invoice_values[17])
        role = int(invoice_values[18])
        ranked_type = int(invoice_values[19]) 
        if game_id == 6 and game_type == 'A':  
            is_arena_2vs2 = bool(int(invoice_values[20]))
            rank1_player = bool(int(invoice_values[22]))
            tournament_player = bool(int(invoice_values[23]))
            boost_method = str(invoice_values[24])
            

        champions_selected = str(invoice_values[21])

        champions_list = []
        
        if champions_selected and select_champion and champions_selected != 'null':
            try:
                champions_list = [int(num) for num in champions_selected.split("ch") if num]
            except ValueError:
                champions_list = []
            if len(champions_list) > 3:
                champions_list = []
            for id in champions_list:
                try:
                    Champion.objects.get(id=id, game__id = game_id)
                except Champion.DoesNotExist:
                    champions_list = []
        
        if promo_code == 0:
            promo_code = None
        
        try:
            booster = BaseUser.objects.get(id=booster_id, is_booster =True)
        except BaseUser.DoesNotExist:
            booster = None

        Game = get_game(game_id, game_type)        
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
                extend_order_customer_username = extend_order.customer_username
                extend_order_data_correct = extend_order.data_correct
                extend_order_promo_code = extend_order.promo_code
                extend_order_game_id = extend_order.game.id

                extend_order_game = Game.objects.get(order = extend_order)
                
                extend_current_rank = extend_order_game.current_rank
                extend_current_division = extend_order_game.current_division
                extend_current_marks = extend_order_game.current_marks
                
                extend_order_game_reached_rank = extend_order_game.reached_rank
                extend_order_game_reached_division = extend_order_game.reached_division
                extend_order_game_reached_marks = extend_order_game.reached_marks  


                # set new extend_order_actual_price with old order percent 
                actual_price = extend_order.actual_price
                main_price = extend_order.price
                percent = round(actual_price / (main_price/100))

                new_order_price = price + extend_order_price
                extend_order_actual_price = new_order_price * (percent/100)
                
                if game_id == 12 or game_id == 10 :
                    extend_order_role = extend_order_game.role
                     

        except BaseOrder.DoesNotExist:
            extend_order = None

        if status == 'New' or status == 'Continue':
            actual_price = 0
            if status == 'Continue':
                actual_price = round(price * (extra / 100),2)
            baseOrder = BaseOrder.objects.create(game_id=game_id,invoice=invoice, booster=booster, payer_id=payer_id, customer=customer,status=status, price=price, duo_boosting=duo_boosting,select_booster=select_booster,turbo_boost=turbo_boost,streaming=streaming, name=name, customer_server=server,promo_code_id= promo_code, actual_price=actual_price, game_type=game_type)
            # Here I Make This Condition Because it Make Error in Placement
            if game_type == 'D' or game_type == 'A':
                default_fields = {
                    'order': baseOrder,
                    'current_rank_id': current_rank,
                    'current_division': current_division,
                    'current_marks': current_marks,
                    'desired_rank_id': desired_rank,
                    'desired_division': desired_division,
                    'reached_rank_id': current_rank,
                    'reached_division': current_division,
                    'reached_marks': current_marks,
                }
            # Wildrift Without Placement 
            if game_id == 1:
                order = Game.objects.create(**default_fields, select_champion=select_champion)
            # Valorant - Division
            elif game_id == 2 and game_type == 'D':
                order = Game.objects.create(**default_fields, select_champion=select_champion)
            # Valorant - Placement
            elif game_id == 2 and game_type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,select_champion=select_champion)
            # Pubg Without Placement 
            elif game_id == 3 and game_type == 'D':
                order = Game.objects.create(**default_fields, select_champion=select_champion)
            # LOL - Division
            elif game_id == 4 and game_type == 'D':
                order = Game.objects.create(**default_fields, select_champion=select_champion)
            # LOL - Placement
            elif game_id == 4 and game_type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,select_champion=select_champion)
            # TFT - Division
            elif game_id == 5 and game_type == 'D':
                order = Game.objects.create(**default_fields)
            # TFT - Placement
            elif game_id == 5 and game_type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match)
            # WoW - Arena
            elif game_id == 6 and game_type == 'A':
                order = Game.objects.create(**default_fields, is_arena_2vs2=is_arena_2vs2, rank1_player=rank1_player, tournament_player=tournament_player, boost_method=boost_method )
            # WoW - Raid
            elif game_id == 6 and game_type == 'R':
                order = Game.objects.create(order=baseOrder, map=map, difficulty=difficulty_chosen, boost_method=boost_method, loot_priority=loot_priority)
                # add meny to meny bosses ids from bosses_ids
                if bosses_ids :
                    for boss_id in bosses_ids:
                        order.bosses.add(boss_id)
                        
            elif game_id == 6 and game_type == 'RB':   
                order = Game.objects.create(order=baseOrder, bundle_id=bundle, boost_method=boost_method, loot_priority=loot_priority)     

            elif game_id == 6 and game_type == 'DS':
                order = Game.objects.create(order=baseOrder, keystone=keystone, keys=keys, traders=traders, traders_armor_type=traders_armor_type, map_preferred=map_preferred, maps=maps, boost_method=boost_method, timed=timed)    
            
            # WoW - Level Up
            elif game_id == 6 and game_type == 'F':
                order = Game.objects.create(order=baseOrder, current_level=current_level, desired_level=desired_level)

            # HEARTHSTONE - Division
            elif game_id == 7 and game_type == 'D':
                order = Game.objects.create(**default_fields)
            # HEARTHSTONE - Battle
            elif game_id == 7 and game_type == 'A':
                order = Game.objects.create(**default_fields)
            # Mobile Legends - Division
            elif game_id == 8 and game_type == 'D':
                order = Game.objects.create(**default_fields, select_champion=select_champion)
            # Mobile Legends - Placement
            elif game_id == 8 and game_type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,select_champion=select_champion)
            # Rocket League - Division
            elif game_id == 9 and game_type == 'D':
                order = Game.objects.create(**default_fields, ranked_type=ranked_type)
            # Rocket League - Placement
            elif game_id == 9 and game_type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=last_rank,number_of_match=number_of_match)
            # Rocket League - Seasonal
            elif game_id == 9 and game_type == 'S':
                order = Game.objects.create(order=baseOrder,current_rank_id=current_rank,number_of_wins=number_of_wins)
            # Rocket League - Tournament
            elif game_id == 9 and game_type == 'T':
                order = Game.objects.create(order=baseOrder,current_league_id=current_league)
            # TODO sara kamal Dota2          #########
            if game_id == 10 and game_type == 'A':
                order = Game.objects.create(**default_fields, role=role)
            elif game_id == 10 and game_type == 'P':
                order = Game.objects.create(order=baseOrder, last_rank_id=last_rank,last_division=last_division, number_of_match=number_of_match, role=role)
            #TODO sarah mohamed Honer Of King #########
            if game_id == 11:
                order = Game.objects.create(**default_fields)
            # Overwatch Division 
            elif game_id == 12 and game_type == 'D':
                order = Game.objects.create(**default_fields, role=role)
            # Overwatch Placement 
            elif game_id == 12 and game_type == 'P':
                order = Game.objects.create(order=baseOrder, number_of_match=number_of_match, last_rank_id=last_rank, role=role)
            # csgo2
            elif game_id == 13 and game_type == 'D':
                order = Game.objects.create(**default_fields)
            elif game_id == 13 and game_type == 'A':
                order = Game.objects.create(**default_fields)
            elif game_id == 13 and game_type == 'F':
                order = Game.objects.create(order=baseOrder, current_level=current_level, desired_level=desired_level)
            else:
                print(f'error in game id idk why ? game id:{game_id} game type:{game_type}')    

        elif status == 'Extend':
            baseOrder = BaseOrder.objects.create(invoice=invoice, booster=extend_order_booster,duo_boosting=duo_boosting, select_booster=select_booster, turbo_boost=turbo_boost,streaming=streaming, customer=extend_order_customer,payer_id=payer_id, customer_gamename=extend_order_customer_gamename, customer_username=extend_order_customer_username ,customer_password=extend_order_customer_password, customer_server=extend_order_server,name = order_name, money_owed =extend_order_money_owed, price = new_order_price, data_correct = extend_order_data_correct,promo_code=extend_order_promo_code, status = "Extend",game_id =extend_order_game_id, actual_price=extend_order_actual_price, game_type= game_type,)
            extend_fields = {
                'order': baseOrder,
                'current_rank': extend_current_rank,
                'current_division': extend_current_division,
                'current_marks': extend_current_marks,
                'desired_rank_id': desired_rank,
                'desired_division': desired_division,
                'reached_rank': extend_order_game_reached_rank,
                'reached_division': extend_order_game_reached_division,
                'reached_marks': extend_order_game_reached_marks,
            }

            # Wildrift Without Placement 
            if game_id == 1:
                order = Game.objects.create(**extend_fields, select_champion=select_champion)
            # Valorant - Division
            elif game_id == 2 and game_type == 'D':
                order = Game.objects.create(**extend_fields, select_champion=select_champion)
            # Valorant - Placement
            elif game_id == 2 and game_type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,select_champion=select_champion)       
            # Pubg Without Placement 
            elif game_id == 3:
                order = Game.objects.create(**extend_fields, select_champion=select_champion)
            # LOL - Division
            elif game_id == 4 and game_type == 'D':
                order = Game.objects.create(**extend_fields, select_champion=select_champion)
            # LOL - Placement
            elif game_id == 4 and game_type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,select_champion=select_champion)
            # TFT - Division
            elif game_id == 5 and game_type == 'D':
                order = Game.objects.create(**extend_fields)
            # TFT - Placement
            elif game_id == 5 and game_type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match)
            # WoW
            elif game_id == 6 and game_type == 'A':
                # TODO not completed yet
                order = Game.objects.create(**extend_fields, is_arena_2vs2=is_arena_2vs2, rank1_player=rank1_player, tournament_player=tournament_player, boost_method=boost_method )
            # HEARTHSTONE - Division
            elif game_id == 7 and game_type == 'D':
                order = Game.objects.create(**extend_fields)
            # HEARTHSTONE - Battle
            elif game_id == 7 and game_type == 'A':
                order = Game.objects.create(**extend_fields)   
            # Mobile Legends
            elif game_id == 8 and game_type == 'D': 
                order = Game.objects.create(**extend_fields, select_champion=select_champion)

            elif game_id == 8 and game_type == 'P': 
                order = Game.objects.create(order=baseOrder,last_rank_id=(last_rank + 1),number_of_match=number_of_match,select_champion=select_champion)

            # Rocket League - Division
            elif game_id == 9 and game_type == 'D':
                order = Game.objects.create(**extend_fields, ranked_type=ranked_type)
            # Rocket League - Placement
            elif game_id == 9 and game_type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=last_rank,number_of_match=number_of_match)
            # Rocket League - Seasonal
            elif game_id == 9 and game_type == 'S':
                order = Game.objects.create(order=baseOrder,current_rank_id=current_rank,number_of_wins=number_of_wins)
            # Rocket League - Tournament
            elif game_id == 9 and game_type == 'T':
                order = Game.objects.create(order=baseOrder,current_league_id=current_league)
            # TODO sara kamal Doat2      TODO       ########
            if game_id == 10 and game_type == 'A':
                order = Game.objects.create(**extend_fields, role=extend_order_role)
            elif game_id == 10 and game_type == 'P':
                order = Game.objects.create(order=baseOrder,last_rank_id=last_rank,last_division=last_division, number_of_match=number_of_match, role=extend_order_role)
            #TODO sarah mohamed Honer Of King      TODO      #########
            if game_id == 11:
                order = Game.objects.create(**extend_fields)
            # Overwatch Division 
            elif game_id == 12 and game_type == 'D':
                order = Game.objects.create(**extend_fields, role= extend_order_role)
            # Overwatch Placement 
            elif game_id == 12 and game_type == 'P':
                # order = Game.objects.create(order=baseOrder,)
                pass
            # csgo2
            elif game_id == 13 and game_type == 'D':
                order = Game.objects.create(**extend_fields)
            elif game_id == 13 and game_type == 'A':
                order = Game.objects.create(**extend_fields)
            elif game_id == 13 and game_type == 'F':
                order = Game.objects.create(order=baseOrder, current_level=current_level, desired_level=desired_level)
            else:
                print('error in game id')  
        content_type = ContentType.objects.get_for_model(order)
        baseOrder.content_type = content_type
        baseOrder.object_id = order.pk
        baseOrder.captcha_id =  random.randint(1, 2000)

        if champions_list :
            order.champions.add(*champions_list)

        order.save_with_processing()
        baseOrder.customer_wallet()
        print(baseOrder.game_type)
        print(type)
        return order
    
    # except Exception as e:
    #     print(f"Error creating order: {e}")
    #     return None