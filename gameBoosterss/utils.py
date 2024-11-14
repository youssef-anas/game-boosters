from booster.models import Booster
from wildRift.models import WildRiftDivisionOrder
from valorant.models import ValorantDivisionOrder, ValorantPlacementOrder
from pubg.models import PubgDivisionOrder
from leagueOfLegends.models import LeagueOfLegendsDivisionOrder, LeagueOfLegendsPlacementOrder
from tft.models import TFTDivisionOrder, TFTPlacementOrder
from hearthstone.models import HearthstoneDivisionOrder, HearthStoneBattleOrder
from rocketLeague.models import RocketLeagueDivisionOrder, RocketLeaguePlacementOrder, RocketLeagueSeasonalOrder, RocketLeagueTournamentOrder
from mobileLegends.models import MobileLegendsDivisionOrder, MobileLegendsPlacementOrder
from WorldOfWarcraft.models import WorldOfWarcraftArenaBoostOrder, WorldOfWarcraftRaidSimpleOrder, WorldOfWarcraftRaidBundleOrder, WorldOfWarcraftDungeonSimpleOrder, WowLevelUpOrder
from overwatch2.models import Overwatch2DivisionOrder, Overwatch2PlacementOrder
from honorOfKings.models import HonorOfKingsDivisionOrder
from dota2.models import Dota2RankBoostOrder, Dota2PlacementOrder
from csgo2.models import Csgo2DivisionOrder, Csgo2PremierOrder, CsgoFaceitOrder
from accounts.models import BaseOrder, TokenForPay
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
from django.conf import settings
from rest_framework.throttling import UserRateThrottle

# paypalrestsdk
import paypalrestsdk
from cryptomus import Client

from gameBoosterss.permissions import IsNotBooster
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


def cryptomus_payment(order_info, request, token):
    data = {
        'amount': str(order_info['extra_order']['price']),
        'currency': 'USDT',
        'to_currency': 'USDT',
        'network': 'TRON',
        'order_id': str(token.id),
        'url_return': request.build_absolute_uri(f"/customer/payment-canceled/{token.token}/"),
        'url_success': request.build_absolute_uri(f"/customer/payment-success/{token.token}/"),
        # 'url_callback': 'http://127.0.0.1:8000/customer/payment-notify/',
    }
    
    try:
        payment = Client.payment(settings.PAYMENT_KEY, settings.MERCHANT_UUID)
        result = payment.create(data)
        
        if 'url' in result:
            return result['url']
        else:
            raise KeyError("The 'url' key is missing in the response.")
    
    except Exception as e:
        print(f"Error in cryptomus_payment: {str(e)}")
        raise 


def paypal_payment(order_info, request, token):
    data =  paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(f"/customer/payment-success/{token.token}/"),
            "cancel_url": request.build_absolute_uri(f"/customer/payment-canceled/{token.token}/")
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": 'Boosting Order',
                    "sku": "item",
                    "price": order_info['extra_order']['price'],
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": order_info['extra_order']['price'],
                "currency": "USD"
            },
            "description": "Payment for Boosting order."
        }]
    })
    if data.create():
        for link in data.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                return approval_url

def tipPayment(tip, request, token):
    return paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(f"/customer/tip-booster/success/{token}/"),
            "cancel_url": request.build_absolute_uri(f"/customer/tip-booster/cancel/{token}/")
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Tip For Booster",
                    "sku": "item",
                    "price": tip,
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": tip,
                "currency": "USD"
                    },
            "description": "Payment for Boosting order."
            }]
    })




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
        'R': WorldOfWarcraftRaidSimpleOrder,
        'RB': WorldOfWarcraftRaidBundleOrder,
        'DS': WorldOfWarcraftDungeonSimpleOrder,
        'F' : WowLevelUpOrder, 
    }
    Game = WOW_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid World of Warcraft game type: {type}")
    return Game

def check_hearthstone_type(type) -> Model:
    HEARTHSTONE_MODELS = {
        'D': HearthstoneDivisionOrder,
        'A': HearthStoneBattleOrder,
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
    1: {'can_choose_me': True, 'is_wr_player': True},
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
    orders = (BaseOrder.objects
        .filter(booster__isnull=True)  # Using __isnull=True for better readability
        .exclude(game_id=6)  # Exclude orders with game_id=6
        .order_by('-id')  # Order by 'id' in descending order
    )
    all_orders_dict = []
    for order in orders:
        if order.captcha:
           captcha=order.captcha.image.name
        else:
            captcha=None
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

        order_dict = {
            'game_id': order.game.id,
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
            'captcha': captcha,
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

    html_content = render_to_string('mails/activate_email_form.html', {'secret_key': secret_key, 'user':user})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content,  settings.EMAIL_HOST_USER, users_list)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

    user.activation_code = secret_key
    user.activation_time = timezone.now()
    user.save()
    return secret_key

def reset_password(user) -> int:
    subject = 'Password Reset'
    users_list = [user.email]
    secret_key = generate_random_5_digit_number()

    html_content = render_to_string('mails/reset_password_form.html', {'secret_key': secret_key, 'user': user})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content,  settings.EMAIL_HOST_USER, users_list)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    user.rest_password_code = secret_key
    user.reset_password_time = timezone.now()
    user.save()
    return secret_key

def booster_added_message(email, password,username):
    subject = 'Your application for madboost.gg has been approved'
    users_list = [email]
    html_content = render_to_string('mails/approved_form.html', {'password': password,'username':username})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, users_list)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    return True


def send_change_data_msg(message):

    event_data = {
        'type': 'change_data',
        'message': message.content,
        "username": message.user.username,
        "room_name": message.room.order_name,
        "msg_type": message.msg_type
    }
    async_to_sync(channel_layer.group_send)(f'chat_roomFor-{message.user.username}-{message.room.order_name}', event_data)

def send_refresh_msg(booster, customer, order_name):

    event_data = {
        'type': 'change_data',
        'message': 'refresh',
        "username": booster,
        "room_name": order_name,
        "msg_type": 5,
    }
    async_to_sync(channel_layer.group_send)(f'chat_roomFor-{customer}-{order_name}', event_data)



from firebase_admin import storage
import uuid
from django.core.files.uploadedfile import InMemoryUploadedFile
import io

def get_half_img_url(full_url):
    url_parts = full_url.split(".appspot.com/")
    img_url_part = url_parts[1]
    return img_url_part

def upload_image_to_firebase(image_data, image_name):
    if image_data is None:
        return None

    # Read the contents of the image file as bytes
    image_file = image_data.file.read()

    # Reset the file pointer to the beginning of the file data
    image_data.file.seek(0)

    # Generate a unique ID for the image filename
    unique_id = str(uuid.uuid4())

    # Upload image to Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(image_name)

    blob.upload_from_string(image_file, content_type=image_data.content_type)

    # Make the uploaded image publicly accessible
    blob.make_public()

    # Return the URL of the uploaded image
    print(blob.public_url)
    url = get_half_img_url(blob.public_url, )
    return url



def get_booster_game_ids(user):
    booster = Booster.objects.get(booster = user)   
    ids = []
    if booster.is_wr_player:
        ids.append(1)
    if booster.is_valo_player:
        ids.append(2)
    if booster.is_pubg_player:
        ids.append(3)
    if booster.is_lol_player:
        ids.append(4)
    if booster.is_tft_player:
        ids.append(5)
    if booster.is_wow_player:
        ids.append(6)
    if booster.is_hearthstone_player:
        ids.append(7)
    if booster.is_mobleg_player:
        ids.append(8)
    if booster.is_rl_player:
        ids.append(9)
    if booster.is_dota2_player:
        ids.append(10)
    if booster.is_hok_player:
        ids.append(11)
    if booster.is_overwatch2_player:
        ids.append(12)
    if booster.is_csgo2_player:
        ids.append(13)
    return ids       


def send_available_to_play_mail(user, order, client_url):
    if user.is_booster:
        email = order.customer.email
        madboost_user = order.customer
    else:
        if order.booster:
            email = order.booster.email
            madboost_user = order.booster
        else:
            return None
    subject = 'Are you Available to Play ?'
    users_list = [email]
    html_content = render_to_string('mails/available_mail_form.html', {'madboost_user': madboost_user,'order': order, 'requested_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'), 'client_url': client_url})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, users_list)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    return True

def send_message_mail(user, order, message):
    if user.is_booster:
        email = order.customer.email
        madboost_user = order.customer
    else:
        if order.booster:
            email = order.booster.email
            madboost_user = order.booster
        else:
            return None
    subject = 'New Message Arraive'
    users_list = [email]
    html_content = render_to_string('mails/message_mail_form.html', {'madboost_user': madboost_user,'order': order,'message': message})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, users_list)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    return True

def send_mail_bootser_choose(order_name, booster):
    subject = 'You Have new Order'
    users_list = [booster.email]
    html_content = render_to_string('mails/bootser_choose_mail_form.html', {'order_name': order_name,'booster': booster, 'requested_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S')})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, users_list)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    return True



class NewMadBoostPayment(APIView):
    permission_classes = [IsNotBooster]
    serializer_mapping = None
    throttle_classes = [UserRateThrottle] 

    def __init__(self, **kwargs):
      super().__init__(**kwargs)
      if not self.serializer_mapping:
          raise ValueError("serializer_mapping must not be None")

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class(request.data.get('game_type'))

        if not serializer_class:
            return Response({"message": "Invalid game type."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = serializer_class(data=request.data)
        if not serializer.is_valid():
            field, error_message = next(iter(serializer.errors.items()))
            return Response({'message': f"{field}: {error_message[0]}"}, status=status.HTTP_400_BAD_REQUEST)

        order_info = self.extract_order_info(serializer_class, serializer.validated_data)
        if isinstance(order_info, Response):
            return order_info

        amount_error = self.check_amount(order_info['extra_order']['price'])
        if amount_error:
            return amount_error

        return self.perform_payment(order_info, request, serializer_class)

    def extract_order_info(self, serializer_class, data):
        order_getter = serializer_class.game_order_info
        order_info_class = order_getter(data)
        order_info = order_info_class.get_order_info()
        if not order_info:
            return Response({"message": "Order information could not be retrieved."}, status=status.HTTP_400_BAD_REQUEST)
        return order_info

    def check_amount(self, price):
        if price < 10:
            return Response({"message": "Minimum order amount is $10.00."}, status=status.HTTP_400_BAD_REQUEST)
        return None

    def get_serializer_class(self, game_type):
        return self.serializer_mapping.get(game_type)
    
    def perform_payment(self, order_info, request, serializer_class):
        model = serializer_class.order_model
        token = TokenForPay.create_token_for_pay(request.user, order_info, model)
        payment_url = self.create_payment(order_info, request, token)
        if payment_url:
            return Response({'url': payment_url})
        else:
            return Response({"message": "There was an issue connecting to the payment provider."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_payment(self, order_info, request, token):
        if request.data.get('cryptomus') != 'false':

            return cryptomus_payment(order_info, request, token)
        else:
            return paypal_payment(order_info, request, token)        