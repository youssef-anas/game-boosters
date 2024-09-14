class DivisionGameOrderInfo:
    game_order = {}
    
    def __init__(self, data: dict) -> None:
        self.data = data
    
    def get_game_info(self):
        game_info_params = ['current_rank', 'current_division', 'desired_rank', 'desired_division', 'marks']  
        # create a variable for each parameter
        for param in game_info_params:
            self.__setattr__(param, self.data[param])
              
            
        self.marks = self.data.get('marks', 0)
        self.game_order.update({'current_marks': self.marks})

        self.game_order.update({'current_rank_id': self.current_rank})
        self.game_order.update({'desired_rank_id': self.desired_rank})
        self.game_order.update({'current_division': self.current_division})
        self.game_order.update({'desired_division': self.desired_division})
        

    def get_price(self):
        start_division = ((self.current_rank - 1) * self.division_number) + self.current_division
        end_division = ((self.desired_rank - 1) * self.division_number) + self.desired_division
        marks_price = self.marks_data[self.current_rank][self.marks]
        sublist = self.division_prices[start_division:end_division ]
        total_sum = sum(sublist)
        price = total_sum - marks_price
        price += (price * self.total_percent/100)
        price -= price * (self.promo_code_amount/100)
        price = round(price, 2)
        price = round(price - self.extend_order_price, 2)
        self.base_order.update({'price': price})
        return price
    
    
    def get_order_info(self):
        self.get_game_info()
        self.get_base_order_info() 
        self.get_price()


        return {
            'base_order': self.base_order,
            'extra_order': self.extra_order,
            'game_order': self.game_order,
        }  
            


