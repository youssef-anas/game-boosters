from .models import HonorOfKingsTier, HonorOfKingsMark

def get_hok_divisions_data():
    divisions = HonorOfKingsTier.objects.all().order_by('id')
    divisions_data = [
        [division.from_V_to_IV, division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_IV_next]
        for division in divisions
    ]
    return divisions_data

def get_hok_marks_data():
    marks = HonorOfKingsMark.objects.all().order_by('id')
    marks_data = [
        [0, mark.star_1, mark.star_2, mark.star_3]
        for mark in marks
    ]
    return marks_data
