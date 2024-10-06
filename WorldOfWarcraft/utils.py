from WorldOfWarcraft.models import KeystonePrice, WowLevelUpPrice

def extract_bosses_ids(boss_string):
    if not boss_string:
        return []
    bosses = boss_string.split(',')
    ids = [int(boss[4:]) for boss in bosses]
    return ids


def extract_bundle_id(bundle_string):
    id = int(''.join(filter(str.isdigit, bundle_string)))
    return id


def get_keyston_price():
    prices = KeystonePrice.objects.all().order_by('id').values_list('price', flat=True)
    price_list = list(prices)
    return price_list


def get_level_up_price():
    price = WowLevelUpPrice.objects.all().order_by('-id').first().price
    return price


def get_rank_from_rp(rp):
    if rp >= 2100: 
      return 4
    
    if rp >= 1800 and rp < 2100:
      return 3
    
    if rp >= 1600 and rp < 1799:
      return 2

    if rp < 1600: 
      return 1
    
def get_map_id (map_name):
    if map_name == 'incarnates':
        map = 1

    if map_name == 'crucible':
        map = 2

    if map_name == 'amirdrassil':
        map = 3  

    return map    
