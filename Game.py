from Clickers import *
from GameParameters import *
from concurrent.futures import CancelledError
from Interface import *
from collections import deque


class Game:
    def __init__(self):
        self.score = Score()
        self.hand_clicker = HandClicker()
        self.clickers = asyncio.Queue()
        self.game_event_queue = asyncio.Queue()
        self.interface = Interface(self.game_event_queue)
        self.event_loop = asyncio.get_event_loop()

    def start_game(self):
        tasks = [
            self.event_loop.create_task(self.run_clickers()),
            self.event_loop.create_task(self.run_interface()),
            self.event_loop.create_task(self.run_processing_game_events())
        ]
        wait_tasks = asyncio.wait(tasks)
        self.event_loop.run_until_complete(wait_tasks)

    async def run_clickers(self):
        while True:
            while not self.clickers.empty():
                clicker = await self.clickers.get()
                asyncio.run_coroutine_threadsafe(clicker.start_clicking(self.score), loop=self.event_loop)
            await asyncio.sleep(1 / FPS)

    async def run_interface(self):
        await self.interface.start(self.score)

    async def run_processing_game_events(self):
        while True:
            while not self.game_event_queue.empty():
                game_event = await self.game_event_queue.get()
                await game_event.do_event(self)
            await asyncio.sleep(1 / FPS)
