from accounts.models import PromoCode, BaseOrder, BaseUser


class ChampionOrder:
    def get_champion_info(self):
        self.game_order.update({'champions': self.data['champion_data'], 'select_champion': self.data['select_champion']})


class ExtendOrder:
    def get_extend_order_info(self):
        try :
            _extend_order = BaseOrder.objects.get(id=self.data['extend_order'])
            self.extend_order_price = _extend_order.price
            self.extend_real_order_price = _extend_order.real_order_price
            self.extend_order = _extend_order

            extend_fields = [
                'customer_gamename', 'customer_password', 'customer_username',
                'data_correct', 'money_owed', 'name'
            ] 
            extend_data = [
                'duo_boosting', 'select_booster', 'turbo_boost', 'streaming'
            ]

            # for new order when create
            for field in extend_fields:
                self.base_order.update({field: getattr(_extend_order, field)})
            self.base_order.update({'customer_id': _extend_order.customer.id})
            self.base_order.update({'status': 'Extend'})
    
            # for other part of classes use
            # and other part will pass the value
            for field in extend_data:
                self.data.update({field: getattr(_extend_order, field)})
            self.data.update({'promo_code': _extend_order.promo_code.code}) if _extend_order.promo_code else None
            self.data.update({'choose_booster': _extend_order.booster.id}) if _extend_order.booster else None
            self.data.update({'server': _extend_order.customer_server})

        except BaseOrder.DoesNotExist:
            self.extend_order_price = 0
            self.extend_real_order_price = 0
        self.extra_order.update({'extend_order': self.data['extend_order']})   

            
class BaseOrderInfo:
    extend_order_price = 0
    real_order_price = 0
    base_order = {}
    extra_order = {}

    def apply_extra_price(self, price):
        price += (price * self.total_percent/100)
        
        self.real_order_price = price

        if self.extend_order_price <= 0 :

            if self.promo_code_amount < 1 and self.promo_code_amount > 0:
                price -= price * (self.promo_code_amount)    
            elif self.promo_code_amount > 1:
                price -= self.promo_code_amount

        if self.data.get('cryptomus'):
            price -= price * (5/100)

        return round(price, 2)

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
            if promo_code_obj.is_active:
                if promo_code_obj.is_percent:
                    self.promo_code_amount = promo_code_obj.discount_amount / 100
                else:
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
        booster_id = None
        if 'choose_booster' in self.data:
            if self.data['choose_booster'] > 0:
                booster_id = self.data['choose_booster']
        self.base_order.update({'booster_id': booster_id})    
