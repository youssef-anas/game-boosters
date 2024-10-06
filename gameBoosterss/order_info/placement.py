
class PlacementGameOrderInfo:
    game_order = {}
    placement_data = None
    def __init__(self, data: dict) -> None:
        self.data = data
        if not self.placement_data:
            raise Exception('placement data not seted')


    def get_game_info(self):
        game_info_params = ['last_rank', 'number_of_match',]  
        # create a variable for each parameter
        for param in game_info_params:
            self.__setattr__(param, self.data[param])

        self.game_order.update({'last_rank_id': self.last_rank + 1})
        self.game_order.update({'number_of_match': self.number_of_match})
        

    def get_price(self):
        price = self.placement_data[self.last_rank] * self.number_of_match
        price = self.apply_extra_price(price)
        self.base_order.update({'price': price})
        self.extra_order.update({'price': price})
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