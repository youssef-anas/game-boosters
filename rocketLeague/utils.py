from .models import RocketLeagueDivision, RocketLeaguePlacement, RocketLeagueSeasonal, RocketLeagueTournament

def get_rocket_league_divisions_data():
    divisions = RocketLeagueDivision.objects.all().order_by('id')
    divisions_data = [
        [division.from_I_to_II, division.from_II_to_III, division.from_III_to_I_next]
        for division in divisions
    ]
    return divisions_data

def get_rocket_league_placements_data():
    placements = RocketLeaguePlacement.objects.all().order_by('id')
    placements_data = [placement.price for placement in placements]
    return placements_data

def get_rocket_league_seasonals_data():
    seasonals = RocketLeagueSeasonal.objects.all().order_by('id')
    seasonals_data = [seasonal.price for seasonal in seasonals]
    return seasonals_data

def get_rocket_league_tournaments_data():
    tournaments = RocketLeagueTournament.objects.all().order_by('id')
    tournaments_data = [tournament.price for tournament in tournaments]
    return tournaments_data