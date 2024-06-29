from leagueOfLegends.models import LeagueOfLegendsTier, LeagueOfLegendsMark, LeagueOfLegendsPlacement

def get_lol_divisions_data():
    divisions = LeagueOfLegendsTier.objects.all().order_by('id')
    divisions_data = [
        [division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_IV_next]
        for division in divisions
    ]
    return divisions_data

def get_lol_marks_data():
    marks = LeagueOfLegendsMark.objects.all().order_by('id')
    marks_data = [
        [mark.marks_0_20, mark.marks_21_40, mark.marks_41_60, mark.marks_61_80, mark.marks_81_99, mark.marks_series]
        for mark in marks
    ]
    return marks_data

def get_lol_placements_data():
    placements = LeagueOfLegendsPlacement.objects.all().order_by('id')
    placements_data = [placement.price for placement in placements]
    return placements_data