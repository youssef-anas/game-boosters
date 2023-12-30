from wildRift.models import WildRiftDivisionOrder
from accounts.models import BaseUser, BaseOrder
from django.shortcuts import get_object_or_404


def create_order(invoice, payer_id, customer, status='New',name = None):
    # Split the invoice string by the hyphen ("-") delimiter
    invoice_values = invoice.split('-')

    # Extract specific values
    game_id = int(invoice_values[1])
    booster_id = int(invoice_values[11])
    extend_order_id = int(invoice_values[13])
    current_rank =  int(invoice_values[2])
    current_division = int(invoice_values[3])
    current_marks = int(invoice_values[4])
    desired_rank = int(invoice_values[5])
    desired_division = int(invoice_values[6])
    price = float(invoice_values[12])


    duo_boosting = bool(int(invoice_values[7]))
    select_booster = bool(int(invoice_values[8]))
    turbo_boost = bool(int(invoice_values[9]))
    streaming = bool(int(invoice_values[10]))

    if game_id == 1:
        Game = WildRiftDivisionOrder
    elif game_id == 2:
        Game = 'anoter model' # for future work
    else:
        pass

    try:
        booster = BaseUser.objects.get(id=booster_id)
    except BaseUser.DoesNotExist:
        booster = None

    try:
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




    if status == 'New' or status == 'Continue':
        baseOrder = BaseOrder.objects.create(invoice=invoice, booster=booster, payer_id=payer_id, customer=customer,status=status, price=price, duo_boosting=duo_boosting,select_booster=select_booster,turbo_boost=turbo_boost,streaming=streaming, name=name)

        order = Game.objects.create(order=baseOrder,current_rank_id=current_rank,current_division=current_division,
                                    current_marks=current_marks,desired_rank_id=desired_rank,
                                    desired_division=desired_division,reached_rank_id=current_rank,
                                    reached_division=current_division,reached_marks=current_marks)

    if status == 'Extend':
        print(f"order extended from:  {order_name}")
        baseOrder = BaseOrder.objects.create(invoice=invoice, booster=extend_order_booster,
                                             duo_boosting=duo_boosting,select_booster=select_booster,
                                             turbo_boost=turbo_boost,streaming=streaming,
                                             customer=extend_order_customer,payer_id=payer_id,
                                             customer_gamename=extend_order_customer_gamename,
                                             customer_password=extend_order_customer_password,
                                             customer_server=extend_order_server,
                                             name = order_name,
                                             money_owed =extend_order_money_owed,
                                             price = price + extend_order_price,
                                             data_correct = extend_order_data_correct,
                                             status = "Extend",
                                             )
        order = Game.objects.create(order=baseOrder,current_rank_id=current_rank,current_division=current_division,
                                    current_marks=current_marks,desired_rank_id=desired_rank,
                                    desired_division=desired_division,reached_rank=extend_order_game_reached_rank,
                                    reached_division=extend_order_game_reached_division,
                                    reached_marks=extend_order_game_reached_marks)

        

    order.save_with_processing()
    return order











    # extend_order_price = 0
    # extend_order_money_owed = 0
    # extend_order_game_reached_rank = 0
    # extend_order_game_reached_division = 0
    # extend_order_game_reached_marks = 0
    # try:
    #     extend_order = BaseOrder.objects.get(id=extend_order_id)
    #     extend_order.is_done = True
    #     extend_order.is_extended = True
    #     extend_order_money_owed = extend_order.money_owed
    #     extend_order_price = extend_order.price
    #     order_name = extend_order.name
    #     extend_order_booster = extend_order.booster
    #     extend_order_customer_gamename = extend_order.customer_gamename
    #     extend_order_customer_password = extend_order.customer_password
    #     extend_order_server = extend_order.customer_server
    #     extend_order_data_correct = extend_order.data_correct
    #     extend_order.money_owed = 0
    #     extend_order.save()
    #     extend_order_game = Game.objects.get(order = extend_order)
    #     extend_order_game_reached_rank = extend_order_game.reached_rank
    #     extend_order_game_reached_division = extend_order_game.reached_division
    #     extend_order_game_reached_marks = extend_order_game.reached_marks
    # except:
    #     order_name = None
    

    # if game_id == 1:
    #     Game = WildRiftDivisionOrder
    # elif game_id == 2:
    #     Game = 'anoter model' # for future work
    # else:
    #     pass

    # baseOrder = BaseOrder.objects.create(invoice=invoice, booster=booster, payer_id=payer_id, customer=customer,name=order_name,status=status)
    
    # order = Game.objects.create(order=baseOrder)
    # order.save_with_processing()
    # baseOrder.price = extend_order_price + baseOrder.price
    # baseOrder.money_owed = extend_order_money_owed + baseOrder.money_owed
    # if extend_order_game_reached_rank != 0 and extend_order_game_reached_division != 0 and extend_order_game_reached_marks != 0:
    #     order.reached_rank = extend_order_game_reached_rank
    #     order.reached_division = extend_order_game_reached_division
    #     order.reached_marks = extend_order_game_reached_marks
    #     baseOrder.booster = extend_order_booster
    #     baseOrder.customer_gamename = extend_order_customer_gamename
    #     baseOrder.customer_password = extend_order_customer_password
    #     baseOrder.customer_server = extend_order_server
    #     baseOrder.data_correct = extend_order_data_correct
    #     baseOrder.status = 'Extend'
    #     order.save()
    # baseOrder.save()
    # baseOrder.customer_wallet()
    # print(f'Order: {order}')
    # return order        
