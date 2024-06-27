from .models import MobileLegendsTier, MobileLegendsMark, MobileLegendsPlacement

def get_mobile_legends_divisions_data():
    divisions = MobileLegendsTier.objects.all().order_by('id')
    return [
        [division.from_V_to_IV, division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_V_next]
        for division in divisions
    ]

def get_mobile_legends_marks_data():
    marks = MobileLegendsMark.objects.all().order_by('id')
    return [
        [mark.star_1, mark.star_2, mark.star_3, mark.star_4, mark.star_5]
        for mark in marks
    ]

def get_mobile_legends_placements_data():
    placements = MobileLegendsPlacement.objects.all().order_by('id')
    return [
        placement.price
        for placement in placements
    ]