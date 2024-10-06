from ..utils import get_tft_divisions_data, get_tft_marks_data, get_tft_placements_data
from gameBoosterss.order_info.orders import BaseOrderInfo,ExtendOrder
from gameBoosterss.order_info.division import DivisionGameOrderInfo
from gameBoosterss.order_info.placement import PlacementGameOrderInfo


division_names = ['','IV','III','II','I']  
rank_names = ['UNRANK', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD', 'DIAMOND', 'MASTER']

class TFT_DOI(BaseOrderInfo, ExtendOrder, DivisionGameOrderInfo):
    division_prices_data = get_tft_divisions_data()
    division_prices = [item for sublist in division_prices_data for item in sublist]
    division_prices.insert(0, 0)
    marks_data = get_tft_marks_data()
    marks_data.insert(0, [0, 0, 0, 0, 0, 0])
    division_number = 4

class TFT_POI(BaseOrderInfo, PlacementGameOrderInfo):
  placement_data = get_tft_placements_data()
