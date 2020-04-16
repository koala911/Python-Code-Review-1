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
        self.points_per_click = 1

    def click(self, score):
        score.increase(self.points_per_click)


class AutoClicker(Clicker):
    def __init__(self):
        super().__init__()

    async def start_clicking(self, score):
        while True:
            await asyncio.sleep(self.delay)
            score.increase(self.points_per_click)


class SimpleClicker(AutoClicker):
    cost = 10

    def __init__(self):
        super().__init__()
        self.delay = 3
        self.points_per_click = 1


class UpgradedClicker(AutoClicker):
    cost = 20

    def __init__(self):
        super().__init__()
        self.delay = 1
        self.points_per_click = 1
