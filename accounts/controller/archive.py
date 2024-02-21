# Order Creater

# extend_order_price = 0
# extend_order_money_owed = 0
# extend_order_game_reached_rank = 0
# extend_order_game_reached_division = 0
# extend_order_game_reached_marks = 0
# try:
#     extend_order = BaseOrder.objects.get(id=extend_order_id)
#     extend_order.is_done = True
#     extend_order.is_extended = True
#     extend_order_money_owed = extend_order.money_owed
#     extend_order_price = extend_order.price
#     order_name = extend_order.name
#     extend_order_booster = extend_order.booster
#     extend_order_customer_gamename = extend_order.customer_gamename
#     extend_order_customer_password = extend_order.customer_password
#     extend_order_server = extend_order.customer_server
#     extend_order_data_correct = extend_order.data_correct
#     extend_order.money_owed = 0
#     extend_order.save()
#     extend_order_game = Game.objects.get(order = extend_order)
#     extend_order_game_reached_rank = extend_order_game.reached_rank
#     extend_order_game_reached_division = extend_order_game.reached_division
#     extend_order_game_reached_marks = extend_order_game.reached_marks
# except:
#     order_name = None


# if game_id == 1:
#     Game = WildRiftDivisionOrder
# elif game_id == 2:
#     Game = 'anoter model' # for future work
# else:
#     pass

# baseOrder = BaseOrder.objects.create(invoice=invoice, booster=booster, payer_id=payer_id, customer=customer,name=order_name,status=status)

# order = Game.objects.create(order=baseOrder)
# order.save_with_processing()
# baseOrder.price = extend_order_price + baseOrder.price
# baseOrder.money_owed = extend_order_money_owed + baseOrder.money_owed
# if extend_order_game_reached_rank != 0 and extend_order_game_reached_division != 0 and extend_order_game_reached_marks != 0:
#     order.reached_rank = extend_order_game_reached_rank
#     order.reached_division = extend_order_game_reached_division
#     order.reached_marks = extend_order_game_reached_marks
#     baseOrder.booster = extend_order_booster
#     baseOrder.customer_gamename = extend_order_customer_gamename
#     baseOrder.customer_password = extend_order_customer_password
#     baseOrder.customer_server = extend_order_server
#     baseOrder.data_correct = extend_order_data_correct
#     baseOrder.status = 'Extend'
#     order.save()
# baseOrder.save()
# baseOrder.customer_wallet()
# print(f'Order: {order}')
# return order 