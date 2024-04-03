from booster.models import Booster
from wildRift.models import WildRiftDivisionOrder
from valorant.models import ValorantDivisionOrder, ValorantPlacementOrder
from pubg.models import PubgDivisionOrder
from leagueOfLegends.models import LeagueOfLegendsDivisionOrder, LeagueOfLegendsPlacementOrder
from tft.models import TFTDivisionOrder, TFTPlacementOrder
from hearthstone.models import HearthstoneDivisionOrder
from rocketLeague.models import RocketLeagueDivisionOrder, RocketLeaguePlacementOrder, RocketLeagueSeasonalOrder, RocketLeagueTournamentOrder
from mobileLegends.models import MobileLegendsDivisionOrder, MobileLegendsPlacementOrder
from WorldOfWarcraft.models import WorldOfWarcraftArenaBoostOrder
from overwatch2.models import Overwatch2DivisionOrder, Overwatch2PlacementOrder
from honorOfKings.models import HonorOfKingsDivisionOrder
from dota2.models import Dota2RankBoostOrder, Dota2PlacementOrder
from csgo2.models import Csgo2DivisionOrder, Csgo2PremierOrder, CsgoFaceitOrder
from accounts.models import BaseOrder
from django.db.models import Model
from django.utils import timezone
from typing import List
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.serializers.json import DjangoJSONEncoder
import random
import json


def check_rl_type(type) -> Model:
    ROCKET_LEAGUE_MODELS = {
    'D': RocketLeagueDivisionOrder,
    'P': RocketLeaguePlacementOrder,
    'S': RocketLeagueSeasonalOrder,
    'T': RocketLeagueTournamentOrder
        }
    Game = ROCKET_LEAGUE_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid Rocket League game type: {type}")
    return Game

def check_wl_type(type) -> Model:
    WR_MODELS = {
        'D': WildRiftDivisionOrder,
    }
    Game = WR_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid WildRift game type: {type}")
    return Game

def check_valo_type(type) -> Model:
    VALORANT_MODELS = {
    'D': ValorantDivisionOrder,
    'P': ValorantPlacementOrder
        }
    Game = VALORANT_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid Valorant game type: {type}")
    return Game

def check_lol_type(type) -> Model:
    LOL_MODELS = {
        'D': LeagueOfLegendsDivisionOrder,
        'P': LeagueOfLegendsPlacementOrder
    }
    Game = LOL_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid League of Legends game type: {type}")
    return Game

def check_tft_type(type) -> Model:
    TFT_MODELS = {
        'D': TFTDivisionOrder,
        'P': TFTPlacementOrder
    }
    Game = TFT_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid TFT game type: {type}")
    return Game

def check_wow_type(type) -> Model:
    WOW_MODELS = {
        'A': WorldOfWarcraftArenaBoostOrder,
    }
    Game = WOW_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid World of Warcraft game type: {type}")
    return Game

def check_hearthstone_type(type) -> Model:
    HEARTHSTONE_MODELS = {
        'D': HearthstoneDivisionOrder,
    }
    Game = HEARTHSTONE_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid Hearthstone game type: {type}")
    return Game

def check_hok_type(type) -> Model:
    HOK_MODELS = {
        'D': HonorOfKingsDivisionOrder,
    }
    Game = HOK_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid Honor Of Kings game type: {type}")
    return Game

def check_dota2_type(type) -> Model:
    DOTA2_MODELS = {
        'A': Dota2RankBoostOrder,
        'P': Dota2PlacementOrder
    }
    Game = DOTA2_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid Dota2 game type: {type}")
    return Game

def check_mobleg_type(type) -> Model:
    MOBILE_LEGENDS_MODELS = {
        'D': MobileLegendsDivisionOrder,
        'P': MobileLegendsPlacementOrder
    }
    Game = MOBILE_LEGENDS_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid Mobile Legends game type: {type}")
    return Game

def check_overwatch2_type(type) -> Model:
    OVERWATCH2_MODELS = {
        'D': Overwatch2DivisionOrder,
        'P': Overwatch2PlacementOrder
    }
    Game = OVERWATCH2_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid Overwatch2 game type: {type}")
    return Game

def check_pubg_type(type) -> Model:
    PUBG_MODELS = {
        'D': PubgDivisionOrder,
    }
    Game = PUBG_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid Pubg game type: {type}")
    return Game

def check_csgo2_type(type) -> Model:
    CSGO2_MODELS = {
        'D': Csgo2DivisionOrder,
        'A': Csgo2PremierOrder,
        'F': CsgoFaceitOrder,
    }
    Game = CSGO2_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid Csgo2 game type: {type}")
    return Game



def get_game(id, type) -> Model:
    GAME_MODELS = {
        1: check_wl_type,
        2: check_valo_type,
        3: check_pubg_type,
        4: check_lol_type,
        5: check_tft_type,
        6: check_wow_type,
        7: check_hearthstone_type,
        8: check_mobleg_type,
        9: check_rl_type,
        10: check_dota2_type,
        11: check_hok_type,
        12: check_overwatch2_type,
        13: check_csgo2_type,
    }
    Game = GAME_MODELS.get(id, None)
    if callable(Game):  
        return Game(type)  
    elif not Game:
        raise ValueError(f"Invalid game ID: {id}")
    return Game


def get_boosters(id: int) -> List[Booster]:
    filter_conditions = {
    1: {'can_choose_me': True, 'is_wf_player': True},
    2: {'can_choose_me': True, 'is_valo_player': True},
    3: {'can_choose_me': True, 'is_pubg_player': True},
    4: {'can_choose_me': True, 'is_lol_player': True},
    5: {'can_choose_me': True, 'is_tft_player': True},
    6: {'can_choose_me': True, 'is_wow_player': True},
    7: {'can_choose_me': True, 'is_hearthstone_player': True},
    8: {'can_choose_me': True, 'is_mobleg_player': True},
    9: {'can_choose_me': True, 'is_rl_player': True},
    10: {'can_choose_me': True, 'is_dota2_player': True},
    11: {'can_choose_me': True, 'is_hok_player': True},
    12: {'can_choose_me': True, 'is_overwatch2_player': True},
    13: {'can_choose_me': True, 'is_csgo2_player': True},
    }
    filters = filter_conditions.get(id, {})
    boosters = Booster.objects.filter(**filters)
    return boosters


#--------------------------------------------------------------------------
def live_orders():
    orders = BaseOrder.objects.filter(booster=None).order_by('-created_at')
    all_orders_dict = []
    for order in orders:

        if order.game.pk == 1 or order.game.pk == 2 or order.game.pk == 4:
            champions_queryset = order.related_order.champions.all()
            champions = []
            for champion in champions_queryset:
                champion_dict = {
                    "id": champion.pk,
                    "name": champion.name,
                    "image": champion.get_image_url(),
                    "game_id": champion.game_id
                }
                champions.append(champion_dict)
            # champions_list = list(champions_queryset.values())
            # champions = json.dumps(champions_list, cls=DjangoJSONEncoder)
            
        else:
            champions = None

        print("ORDER: ",order)
        order_dict = {
            "id": order.pk,
            'name': order.name,
            'server': order.customer_server,
            'status': order.status,
            'price': order.price,
            'game_name':order.game.name,
            'details':order.details,
            'duo_boosting': order.duo_boosting,
            'turbo_boost': order.turbo_boost,
            'streaming': order.streaming,
            'select_champion': order.related_order.select_champion if hasattr(order, 'related_order') and hasattr(order.related_order, 'select_champion') else 0,

            'champions': champions,
            'url':f'{order.game.link}/{order.pk}/',
        }
        all_orders_dict.append(order_dict)
    return all_orders_dict 

def refresh_order_page():
    all_orders_dict = live_orders()
    async_to_sync(channel_layer.group_send)(
        'orders',
        {
            'type': 'order_list',
            'order': all_orders_dict,
        }
    )

# activate account and reset password
    
def generate_random_5_digit_number():
    return random.randint(10000, 99999)

def send_activation_code(user) -> int:
    subject = 'Activate Your Account'
    users_list = [user.email]
    secret_key = generate_random_5_digit_number()

    html_content = render_to_string('chat/activation_email.html', {'secret_key': secret_key, 'user':user})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, 'madboost.customer@gmail.com', users_list)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

    user.activation_code = secret_key
    user.activation_time = timezone.now()
    user.save()
    return secret_key

def send_change_data_msg(message):

    event_data = {
        'type': 'change_data',
        'message': message.content,
        "username": message.user.username,
        "room_name": message.room.order_name,
        "msg_type": message.msg_type
    }
    async_to_sync(channel_layer.group_send)(f'chat_roomFor-{message.user}-{message.room.order_name}', event_data)