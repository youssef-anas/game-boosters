from pubg.models import PubgMark, PubgTier

def get_divisions_data():
    divisions = PubgTier.objects.all().order_by('id')
    divisions_data = [
        [division.from_V_to_VI, division.from_VI_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_V_next]
        for division in divisions
    ]
    return divisions_data

def get_marks_data():
    marks = PubgMark.objects.all().order_by('id')
    marks_data = [
        [mark.marks_0_20, mark.marks_21_40, mark.marks_41_60, mark.marks_61_80, mark.marks_81_100]
        for mark in marks
    ]
    return marks_data