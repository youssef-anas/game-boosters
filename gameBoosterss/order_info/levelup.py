class LevelupGameOrderInfo:
    game_order = {}
    extend_order = 0
    faceit_prices = []
    
    def __init__(self, data: dict) -> None:
        self.data = data
        if not self.faceit_prices:
            raise Exception('faceit price not seted')
    
    def get_game_info(self):
        game_info_params = ['current_level', 'desired_level']  
        # create a variable for each parameter
        for param in game_info_params:
            self.__setattr__(param, self.data[param])
            self.game_order.update({param: self.data[param]})        

    def get_price(self):
        sublist = self.faceit_prices[self.current_level : self.desired_level]
        price = sum(sublist)
        price = self.apply_extra_price(price)
        price_for_payment = round(price - self.extend_order_price, 2)
        self.base_order.update({'price': price})
        self.extra_order.update({'price': price_for_payment})
        return price
    
    
    def get_order_info(self):
        self.get_game_info()
        self.get_base_order_info() 
        self.get_price()
        return {
            'base_order': self.base_order,
            'game_order': self.game_order,
            'extra_order': self.extra_order,
        }  