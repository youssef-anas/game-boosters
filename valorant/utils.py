from .models import ValorantTier, ValorantMark, ValorantPlacement

def get_valorant_divisions_data():
    divisions = ValorantTier.objects.all().order_by('id')
    divisions_data = [
        [division.from_I_to_II, division.from_II_to_III, division.from_III_to_I_next]
        for division in divisions
    ]
    return divisions_data

def get_valorant_marks_data():
    marks = ValorantMark.objects.all().order_by('id')
    marks_data = [
        [mark.marks_0_20, mark.marks_21_40, mark.marks_41_60, mark.marks_61_80, mark.marks_81_100]
        for mark in marks
    ]
    return marks_data

def get_valorant_placements_data():
    placements = ValorantPlacement.objects.all().order_by('id')
    placements_data = [
        placement.price
        for placement in placements
    ]
    return placements_data
