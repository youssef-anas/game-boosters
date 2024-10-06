import math


class Arena_V2_GameOrderInfo:
    game_order = {}
    extend_order = 0
    floor = False

    # arena info
    points_value = 0
    points_range = []
    arena_prices = []
    full_price_val = []

    def __init__(self, data: dict) -> None:
        self.data = data

        # or no digit intger
        if self.points_value <= 0: 
            raise Exception('points value not seted')
        if len(self.points_range) <= 0:
            raise Exception('points range not seted')
        if len(self.arena_prices) <= 0:
            raise Exception('arena price not seted')
        if len(self.full_price_val) <= 0:
            raise Exception('full price not seted')
        
    def get_range_current(self, amount):
        for idx, max_val in enumerate(self.points_range, start=1):
            if amount <= max_val:
                val = max_val - amount
                if self.floor :
                    return math.floor(val/self.points_value), idx
                return round(val / self.points_value, 2), idx
        raise Exception('out_of_range')
    
    def get_range_desired(self, amount):
        for idx, max_val in enumerate(self.points_range, start=1):
            if amount <= max_val:
                val = amount-self.points_range[idx-2]
                if self.floor :
                    return math.floor(val/self.points_value), idx
                return round(val / self.points_value, 2), idx
        raise Exception('out_of_range')


    def get_game_info(self):
        game_info_params = ['current_rank', 'desired_rank', 'marks']  
        # create a variable for each parameter
        for param in game_info_params:
            self.__setattr__(param, self.data[param])

        # trnsform mmr to division
        self.current_division = self.data.get('current_mmr', None) or self.data['current_division']
        self.desired_division = self.data.get('desired_mmr', None) or self.data['desired_division']
        # current
        self.game_order.update({'current_rank_id': self.current_rank})
        self.game_order.update({'current_division': self.current_division})
        self.game_order.update({'current_marks': self.marks})

        # desired
        self.game_order.update({'desired_rank_id': self.desired_rank})
        self.game_order.update({'desired_division': self.desired_division})

        # reached
        self.game_order.update({'reached_rank_id': self.current_rank})
        self.game_order.update({'reached_division': self.current_division})
        self.game_order.update({'reached_marks': self.marks})


    def get_game_info_extended(self):
        _extend_order = self.extend_order
        _extend_game = _extend_order.related_order
        self.extend_game = _extend_game

        # current for price
        self.current_rank = _extend_game.current_rank.id
        self.current_division = _extend_game.current_division
        self.marks = _extend_game.current_marks

        # desired for price
        self.desired_rank = self.data['desired_rank']
        self.desired_division = self.data.get('desired_mmr', None) or self.data['desired_rank']


        # current for order
        self.game_order.update({'current_rank_id': self.current_rank })
        self.game_order.update({'current_division': self.current_division})
        self.game_order.update({'current_marks': self.marks})    

        # desired for order
        self.game_order.update({'desired_rank_id': self.desired_rank})
        self.game_order.update({'desired_division': self.desired_division})

        # reached for order
        self.game_order.update({'reached_rank_id': _extend_game.reached_rank.id})
        self.game_order.update({'reached_division': _extend_game.reached_division})
        self.game_order.update({'reached_marks': _extend_game.reached_marks})
    
    def get_price(self):
        curent_mmr_in_c_range, current_range = self.get_range_current(self.current_division)
        desired_mmr_in_d_range, derired_range = self.get_range_desired(self.desired_division)

        if current_range == derired_range:
            range_value = math.floor((self.desired_division - self.current_division ) / self.points_value)
            price = round(range_value * self.arena_prices[current_range-1], 2)
            print(current_range, derired_range, curent_mmr_in_c_range, desired_mmr_in_d_range)
        else:
            sliced_prices = self.full_price_val[current_range : derired_range-1]
            sum_current = curent_mmr_in_c_range * self.arena_prices[current_range-1]
            sum_desired = desired_mmr_in_d_range * self.arena_prices[derired_range-1]
            clear_res = sum(sliced_prices)
            price = round(sum_current + sum_desired + clear_res,2)
        
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
