from Clickers import  *
from Game import *


class GameEvent:
    def __init__(self):
        pass


class BuyAutoClicker(GameEvent):
    def __init__(self, AutoClickerType):
        self.AutoClickerType = AutoClickerType
        super().__init__()

    async def do_event(self, game):
        if game.score.points >= self.AutoClickerType.cost:
            new_auto_clicker = self.AutoClickerType()
            await game.clickers.put(new_auto_clicker)
            game.score.increase(-self.AutoClickerType.cost)
            game.total_points_per_second += new_auto_clicker.cookies_per_second
            print(game.total_points_per_second)

        else:
            print('Not enough score')
        await asyncio.sleep(0)
