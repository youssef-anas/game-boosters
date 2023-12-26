from wildRift.models import WildRiftDivisionOrder
from accounts.models import BaseUser, BaseOrder
from django.shortcuts import get_object_or_404


def create_order(invoice, payer_id, customer, status='None'):
    # Split the invoice string by the hyphen ("-") delimiter
    invoice_values = invoice.split('-')

    # Extract specific values
    game_id = int(invoice_values[1])
    booster_id = int(invoice_values[11])
    extend_order_id = int(invoice_values[13])
    print (f'game id: {game_id}, booster_id: {booster_id}')

    booster = BaseUser.objects.filter(id=booster_id, is_booster=True).first()
    print(booster)
    try:
        extend_order = BaseOrder.objects.get(id=extend_order_id)
        extend_order.is_done = True
        extend_order.is_extended = True
        extend_order.save()
        order_name = extend_order.name
    except:
        order_name = None
    

    if game_id == 1:
        Game = WildRiftDivisionOrder
    elif game_id == 2:
        Game = 'anoter model' # for future work
    else:
        pass

    baseOrder = BaseOrder.objects.create(invoice=invoice, booster=booster, payer_id=payer_id, customer=customer,name=order_name,status=status)
    
    order = Game.objects.create(order=baseOrder)
    order.save_with_processing()
    baseOrder.customer_wallet()
    print(f'Order: {order}')
    return order        
