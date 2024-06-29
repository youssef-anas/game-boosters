from .models import Dota2MmrPrice, Dota2Placement

def get_division_prices():
    division_row = Dota2MmrPrice.objects.all().first()
    division_prices = [
        division_row.price_0_2000,
        division_row.price_2000_3000,
        division_row.price_3000_4000,
        division_row.price_4000_5000,
        division_row.price_5000_5500,
        division_row.price_5500_6000,
        division_row.price_6000_extra
    ]
    return division_prices

def get_placement_prices():
    placement_rows = Dota2Placement.objects.all().order_by('id')
    placement_prices = [row.price for row in placement_rows]
    return placement_prices