from Game import *


class GameEvent:
    def __init__(self):
        pass

    def do_event(self, game):
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
            game.score.update_points_per_sec(new_auto_clicker.points_per_click / new_auto_clicker.delay)
            self.AutoClickerType.cost *= INCREASE_COST
        else:
            print('Not enough points')
        await asyncio.sleep(0)


class HandClick(GameEvent):
    def __init__(self):
        super().__init__()

    async def do_event(self, game):
        game.hand_clicker.click(game.score)
        await asyncio.sleep(0)
