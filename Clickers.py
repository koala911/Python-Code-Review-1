import asyncio
import time
from Score import *


class Clicker:
    def __init__(self):
        pass


# Singleton
class HandClicker(Clicker):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HandClicker, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
        self.cookies_per_click = 1

    async def start_clicking(self, score):
        while True:
            # await asyncio.sleep(1)  #player_clicked()
            await asyncio.sleep(1)
            score.increase(self.cookies_per_click)


class AutoClicker(Clicker):
    def __init__(self):
        super().__init__()

    async def start_clicking(self, score):
        while True:
            await asyncio.sleep(1)
            score.increase(self.cookies_per_second)


class SimpleClicker(AutoClicker):
    cost = 10

    def __init__(self):
        super().__init__()
        self.cookies_per_second = 0.5
