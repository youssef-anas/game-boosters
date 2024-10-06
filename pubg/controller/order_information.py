from pubg.utils import get_divisions_data, get_marks_data
from gameBoosterss.order_info.orders import BaseOrderInfo, ExtendOrder
from gameBoosterss.order_info.division import DivisionGameOrderInfo

class PubgDOI(BaseOrderInfo, ExtendOrder, DivisionGameOrderInfo):
    division_prices_data = get_divisions_data()
    division_prices = [item for sublist in division_prices_data for item in sublist]
    division_prices.insert(0, 0)
    marks_data = get_marks_data()
    marks_data.insert(0, [0, 0, 0, 0, 0, 0])
    division_number = 5