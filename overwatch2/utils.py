from .models import Overwatch2Tier, Overwatch2Mark, Overwatch2Placement

def get_overwatch2_divisions_data():
    divisions = Overwatch2Tier.objects.all().order_by('id')
    divisions_data = [
        [division.from_V_to_IV, division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_V_next]
        for division in divisions
    ]
    return divisions_data

def get_overwatch2_marks_data():
    marks = Overwatch2Mark.objects.all().order_by('id')
    marks_data = [
        [mark.mark_1, mark.mark_2, mark.mark_3, mark.mark_4, mark.mark_5]
        for mark in marks
    ]
    return marks_data

def get_overwatch2_placements_data():
    placements = Overwatch2Placement.objects.all().order_by('id')
    placements_data = [
        placement.price
        for placement in placements
    ]
    return placements_data