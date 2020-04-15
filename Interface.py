import pygame
from GameParameters import *
from concurrent.futures import CancelledError
import asyncio
from GameEvent import *


class Interface:
    def __init__(self, game_event_queue):
        pygame.init()
        self.main_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.main_surface.fill(COLOUR_OF_FIELD)
        self.score_text = pygame.font.Font(None, WINDOW_HEIGHT // 5)
        self.game_event_queue = game_event_queue
        pygame.display.update()

    async def start_print_score(self, score):
        while True:
            for event in pygame.event.get():
                # exit from game
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    exit()
                # buy new clicker
                if event.type == pygame.MOUSEBUTTONDOWN:
                    await self.game_event_queue.put(BuyAutoClicker(SimpleClicker))
            self.main_surface.fill(COLOUR_OF_FIELD)
            score_text_rendered = self.score_text.render(str(score), 1, (50, 100, 100), (0, 240, 200))
            place_of_score = score_text_rendered.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.main_surface.blit(score_text_rendered, place_of_score)
            pygame.display.update()
            await asyncio.sleep(1 / FPS)
        raise CancelledError
