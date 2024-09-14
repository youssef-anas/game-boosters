from accounts.models import PromoCode, BaseOrder, BaseUser


class ChampionOrder:
    def get_champion_info(self):
        self.game_order.update({'champions': self.data['champion_data'], 'select_champion': self.data['select_champion']})


class ExtendOrder:
    extend_order_price = 0

    def get_extend_order_info(self):
        # if self.data['extend_order'] > 0:
            try :
                _extended_order = BaseOrder.objects.get(id=self.data['extend_order'])
                self.extend_order_price = _extended_order.price
            except BaseOrder.DoesNotExist:
                _extended_order = None
            self.extra_order.update({'extend_order': self.data['extend_order']})    
            
class BaseOrderInfo:
    base_order = {}
    extra_order = {}

    def get_percent_price(self):
        return {
            'duo_boosting': 65,
            'select_booster': 10,
            'turbo_boost': 20,
            'streaming': 15,
        }
    
    def get_promo_code_info(self):
        try:
            promo_code_obj = PromoCode.objects.get(code=self.data['promo_code'])
            self.promo_code_amount = promo_code_obj.discount_amount
            self.base_order.update({'promo_code_id': promo_code_obj.pk})
        except PromoCode.DoesNotExist:
            self.promo_code_amount = 0
    
    def get_base_order_info(self):

        self.base_order.update({'customer_server': self.data['server']})
        self.base_order.update({'game_id': self.data['game_id']})
        self.base_order.update({'game_type': self.data['game_type']})


        self.get_totla_percent_price()
        self.get_promo_code_info()
        self.get_booster()
        if hasattr(self, 'get_extend_order_info'):
            self.get_extend_order_info()
        if hasattr(self, 'get_champion_info'):
            self.get_champion_info()    


    def get_totla_percent_price(self):
        _percent_price = self.get_percent_price()
        _total_percent = 0
        _boost_options = []
        for key, value in _percent_price.items():
            if self.data[key]:
                _total_percent += value
                _boost_options.append(key)
            self.base_order[key] = self.data[key]
                
        self.total_percent = _total_percent
        self.boost_options = _boost_options
    
    def get_booster(self):
        if self.data['choose_booster'] > 0:
            booster_id = self.data['choose_booster']
        else:
            booster_id = None
        self.base_order.update({'booster_id': booster_id})    
