from WorldOfWarcraft.models import WorldOfWarcraftBoss, WorldOfWarcraftBundle
from WorldOfWarcraft.utils import get_keyston_price 

class RaidSimpleGameOrderInfo:
    game_order = {}
    extend_order = 0
    
    def __init__(self, data: dict) -> None:
        self.data = data

    def get_bosses_price(self):
        total_bosses_price = 0
        for boss in self.bosses:
            try:
                boss = WorldOfWarcraftBoss.objects.get(id=boss, map=self.map)
                total_bosses_price += boss.price
            except WorldOfWarcraftBoss.DoesNotExist:
                pass
        return total_bosses_price    
    
    def get_game_info(self):
        game_info_params = ['bosses', 'boost_method', 'loot_priority', 'map']
        # create a variable for each parameter
        for param in game_info_params:
            self.__setattr__(param, self.data[param])
            self.game_order.update({param: self.data[param]}) 

        self.difficulty = self.data['difficulty_chosen']
        self.game_order.update({'difficulty': self.data['difficulty_chosen']})      

    def get_price(self):
        total_percent = 0
        total_percent += (self.difficulty * 100)
        if self.data['boost_method'] == 'remote-control':
            total_percent += 30
        if self.loot_priority == True:
            total_percent += 50
        self.total_percent += total_percent

        price = self.get_bosses_price()
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

class RaidBundleGameOrderInfo:
    game_order = {}
    extend_order = 0
    
    def __init__(self, data: dict) -> None:
        self.data = data

    
    def get_game_info(self):
        game_info_params = ['bundle_id', 'boost_method', 'loot_priority']
        # create a variable for each parameter
        for param in game_info_params:
            self.__setattr__(param, self.data[param])
            self.game_order.update({param: self.data[param]}) 

    def get_price(self):
        total_percent = 0
        if self.data['boost_method'] == 'remote-control':
            total_percent += 30
        if self.loot_priority == True:
            total_percent += 50
        self.total_percent += total_percent

        price = WorldOfWarcraftBundle.objects.get(id=self.bundle_id).price
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
    

class DungeonSimpleGameOrderInfo:
    game_order = {}
    extend_order = 0
    
    def __init__(self, data: dict) -> None:
        self.data = data

    def set_maps(self):
        maps = {}
        map_list = ['algathar_academy', 'azure_vault', 'brackenhide_hollow', 'halls_of_infusion', 'neltharus', 'nokhud_offensive', 'ruby_life_pools', 'uldaman_legacy_of_tyr']
        for map in map_list:
            maps.update({map: self.data[map]})
        self.game_order.update({'maps': maps})


    def get_game_info(self):
        game_info_params = ['keystone', 'keys', 'boost_method', 'timed', 'traders', 'traders_armor_type', 'map_preferred']
        self.set_maps()
        # create a variable for each parameter
        for param in game_info_params:
            self.__setattr__(param, self.data[param])
            self.game_order.update({param: self.data[param]}) 

    def get_price(self):
        total_percent = 0
        if self.data['boost_method'] == 'remote-control':
            total_percent += 30
        if self.timed == True:
            total_percent += 20
        if self.map_preferred == 'Specific':
            total_percent += 5

        if self.traders == 'Personal Loot':
            total_percent += 0
        elif self.traders == '1 trader':
            total_percent += 15
        elif self.traders == '2 trader':
            total_percent += 30
        elif self.traders == '3 trader':
            total_percent += 40
        elif self.traders == 'full-Priority':
            total_percent += 50
        print(self.traders)    
    
        self.total_percent += total_percent

        price = get_keyston_price()[self.keystone] * self.keys

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