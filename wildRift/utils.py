from .models import WildRiftTier, WildRiftMark

def get_wildrift_divisions_data():
    divisions = WildRiftTier.objects.all().order_by('id')
    divisions_data = [
        [division.from_IV_to_III] if division.rank.rank_name == 'master' else
        [division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_IV_next]
        for division in divisions
    ]
    return divisions_data

def get_wildrift_marks_data():
    marks = WildRiftMark.objects.all().order_by('id')
    marks_data = [
        [0, mark.mark_1, mark.mark_2, mark.mark_3, mark.mark_4, mark.mark_5, mark.mark_6]
        for mark in marks
    ]
    return marks_data