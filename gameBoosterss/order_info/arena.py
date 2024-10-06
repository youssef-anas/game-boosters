import math


class ArenaGameOrderInfo:
    game_order = {}
    extend_order = 0
    floor = False

    # arena info
    points_value = 0

    def __init__(self, data: dict) -> None:
        self.data = data

    def get_arena_price_price(self):
        pass    

    def get_game_info(self):
        game_info_params = ['current_rank', 'desired_rank']  
        # create a variable for each parameter
        for param in game_info_params:
            self.__setattr__(param, self.data[param])

        # trnsform mmr to division
        self.current_division = self.data.get('current_RP', None) or self.data['current_division']
        self.desired_division = self.data.get('desired_RP', None) or self.data['desired_division']
        # current
        self.game_order.update({'current_rank_id': self.current_rank})
        self.game_order.update({'current_division': self.current_division})

        # desired
        self.game_order.update({'desired_rank_id': self.desired_rank})
        self.game_order.update({'desired_division': self.desired_division})

        # reached
        self.game_order.update({'reached_rank_id': self.current_rank})
        self.game_order.update({'reached_division': self.current_division})



    def get_game_info_extended(self):
        _extend_order = self.extend_order
        _extend_game = _extend_order.related_order
        self.extend_game = _extend_game

        # current for price
        self.current_rank = _extend_game.current_rank.id
        self.current_division = _extend_game.current_division

        # desired for price
        self.desired_rank = self.data['desired_rank']
        self.desired_division = self.data.get('desired_RP', None) or self.data['desired_rank']


        # current for order
        self.game_order.update({'current_rank_id': self.current_rank })
        self.game_order.update({'current_division': self.current_division})

        # desired for order
        self.game_order.update({'desired_rank_id': self.desired_rank})
        self.game_order.update({'desired_division': self.desired_division})

        # reached for order
        self.game_order.update({'reached_rank_id': _extend_game.reached_rank.id})
        self.game_order.update({'reached_division': _extend_game.reached_division})
    
    def get_price(self):
        _arena_price = self.get_arena_price_price()
        price = (self.desired_division - self.current_division ) * (_arena_price / self.points_value)
        
        price = self.apply_extra_price(price)    
        price_for_payment = round(price - self.extend_order_price, 2)
        
        self.base_order.update({'price': price})
        self.extra_order.update({'price': price_for_payment})
        return price
    
    def get_order_info(self):
        if self.extend_order > 0 :
            self.get_game_info_extended()
        else:
            self.get_game_info()
        self.get_base_order_info() 
        self.get_price()
        
        return {
            'base_order': self.base_order,
            'game_order': self.game_order,
            'extra_order': self.extra_order,
        }  
