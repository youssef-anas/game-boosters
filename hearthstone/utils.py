from .models import HearthstoneTier, HearthstoneMark, HearthstoneBattlePrice

def get_hearthstone_divisions_data():
    divisions = HearthstoneTier.objects.all().order_by('id')
    divisions_data = [
        [division.from_X_to_IX, division.from_IX_to_VIII, division.from_VIII_to_VII, division.from_VII_to_VI, division.from_VI_to_V, division.from_V_to_IV, division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_IV_next]
        for division in divisions
    ]
    return divisions_data

def get_hearthstone_marks_data():
    marks = HearthstoneMark.objects.all().order_by('id')
    marks_data = [
        [0, mark.marks_3, mark.marks_2, mark.marks_1]
        for mark in marks
    ]
    return marks_data

def get_hearthstone_battle_prices():
    price = HearthstoneBattlePrice.objects.all().first()
    battle_prices_data = [
        price.from_0_to_2000, 
        price.from_2000_to_4000,
        price.from_4000_to_6000,
        price.from_6000_to_8000,
        price.from_8000_to_10000
    ]
    return battle_prices_data