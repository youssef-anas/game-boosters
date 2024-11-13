class DivisionGameOrderInfo:
    game_order = {}
    
    def __init__(self, data: dict) -> None:
        self.data = data
    
    def get_game_info(self):
        game_info_params = ['current_rank', 'current_division', 'desired_rank', 'desired_division', 'marks']  
        # create a variable for each parameter
        for param in game_info_params:
            self.__setattr__(param, self.data[param])

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
        self.current_rank = _extend_game.desired_rank.id
        self.current_division = _extend_game.desired_division
        self.marks = 0

        # desired for price
        self.desired_rank = self.data['desired_rank']
        self.desired_division = self.data['desired_division']


        # current for order
        self.game_order.update({'current_rank_id': _extend_game.current_rank.id })
        self.game_order.update({'current_division': _extend_game.current_division})
        self.game_order.update({'current_marks': _extend_game.current_marks})    

        # desired for order
        self.game_order.update({'desired_rank_id': self.desired_rank})
        self.game_order.update({'desired_division': self.desired_division})

        # reached for order
        self.game_order.update({'reached_rank_id': _extend_game.reached_rank.id})
        self.game_order.update({'reached_division': _extend_game.reached_division})
        self.game_order.update({'reached_marks': _extend_game.reached_marks})


    def get_price(self):
        start_division = ((self.current_rank - 1) * self.division_number) + self.current_division
        end_division = ((self.desired_rank - 1) * self.division_number) + self.desired_division
        marks_price = self.marks_data[self.current_rank][self.marks]
        sublist = self.division_prices[start_division:end_division ]
        total_sum = sum(sublist)
        price = total_sum - marks_price
        price = self.apply_extra_price(price)
        price_for_payment = round(price, 2)
        self.base_order.update({'price': price + self.extend_order_price})
        self.base_order.update({'real_order_price': self.extend_real_order_price+ self.real_order_price})
        self.extra_order.update({'price': price_for_payment})
        return price
    
    
    def get_order_info(self):
        if hasattr(self, 'get_extend_order_info'):
            self.get_extend_order_info()
        if hasattr(self, 'get_champion_info'):
            self.get_champion_info()   

        if self.extend_order_price > 0 :
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