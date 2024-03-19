from django.test import TestCase
from customer.models import Champion

# Create your tests here.

class SetUp(TestCase):
    valorent = [
        Champion(game_id=2, name='Astra', image='valorant/champions/Astra.png'),
        Champion(game_id=2, name='Breach', image='valorant/champions/Breach.png'),
        Champion(game_id=2, name='Brimstone', image='valorant/champions/Brimstone.png'),
        Champion(game_id=2, name='Cypher', image='valorant/champions/Cypher.png'),
        Champion(game_id=2, name='Chamber', image='valorant/champions/Chamber.png'),
        Champion(game_id=2, name='Jett', image='valorant/champions/Jett.png'),
        Champion(game_id=2, name='Kayo', image='valorant/champions/Kayo.png'),
        Champion(game_id=2, name='Killjoy', image='valorant/champions/Killjoy.png'),
        Champion(game_id=2, name='Omen', image='valorant/champions/Omen.png'),
        Champion(game_id=2, name='Phoenix', image='valorant/champions/Phoenix.png'),
        Champion(game_id=2, name='Raze', image='valorant/champions/Raze.png'),
        Champion(game_id=2, name='Reyna', image='valorant/champions/Reyna.png'),
        Champion(game_id=2, name='Sage', image='valorant/champions/Sage.png'),
        Champion(game_id=2, name='Skye', image='valorant/champions/Skye.png'),
        Champion(game_id=2, name='Sova', image='valorant/champions/Sova.png'),
        Champion(game_id=2, name='Viper', image='valorant/champions/Viper.png'),
        Champion(game_id=2, name='Yoru', image='valorant/champions/Yoru.png'),
        Champion(game_id=2, name='Deadlock', image='valorant/champions/Deadlock.png'),
        Champion(game_id=2, name='Fade', image='valorant/champions/Fade.png'),
        Champion(game_id=2, name='Gekko', image='valorant/champions/Gekko.png'),
        Champion(game_id=2, name='Harbor', image='valorant/champions/Harbor.png'),
        Champion(game_id=2, name='Iso', image='valorant/champions/Iso.png'),
        Champion(game_id=2, name='Neon', image='valorant/champions/Neon.png'),
    ]
    
    Champion.objects.bulk_create(valorent)

