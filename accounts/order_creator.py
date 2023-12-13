from wildRift.models import WildRiftDivisionOrder
from accounts.models import BaseUser
from django.shortcuts import get_object_or_404


def create_order(invoice, payer_id):
    # Split the invoice string by the hyphen ("-") delimiter
    invoice_values = invoice.split('-')

    # Extract specific values
    game_id = int(invoice_values[1])
    booster_id = int(invoice_values[11])
    print (f'game id: {game_id}, booster_id: {booster_id}')

    booster = BaseUser.objects.filter(id=booster_id, is_booster=True).first()
    print(booster)
    
    

    if game_id == 1:
        Game = WildRiftDivisionOrder
    elif game_id == 2:
        Game = 'anoter model' # for future work
    else:
        pass

    if booster :
        order = Game.objects.create(invoice=invoice, booster=booster, payer_id=payer_id)
    else:
        order = Game.objects.create(invoice=invoice, payer_id=payer_id)

    order.save_with_processing()
    print(f'Order: {order}')
    return order        
