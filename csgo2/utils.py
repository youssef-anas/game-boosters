from .models import Csgo2Tier, Csgo2PremierPrice, CsgoFaceitPrice

def get_division_prices():
    divisions = Csgo2Tier.objects.all().order_by('id')
    divisions_data = [
        [division.from_I_to_I_next]
        for division in divisions
    ]
    return divisions_data

def get_premier_prices():
    premier_row = Csgo2PremierPrice.objects.all().first()
    premier_prices = [
        premier_row.price_0_4999, premier_row.price_5000_7999, premier_row.price_8000_11999, 
        premier_row.price_12000_18999, premier_row.price_19000_20999, premier_row.price_21000_24999, 
        premier_row.price_25000_30000
    ]
    return premier_prices

def get_faceit_prices():
    faceit_prices = CsgoFaceitPrice.objects.all().first()
    faceit_data = [
        0, faceit_prices.from_1_to_2, faceit_prices.from_2_to_3, faceit_prices.from_3_to_4, 
        faceit_prices.from_4_to_5, faceit_prices.from_5_to_6, faceit_prices.from_6_to_7, 
        faceit_prices.from_7_to_8, faceit_prices.from_8_to_9, faceit_prices.from_9_to_10
    ]
    return faceit_data
