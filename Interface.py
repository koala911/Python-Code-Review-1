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
        self.score_text = pygame.font.Font(None, WINDOW_HEIGHT // 7)
        self.button_text = pygame.font.Font(None, WINDOW_HEIGHT // 10)
        self.game_event_queue = game_event_queue
        self.main_button_rendered = self.button_text.render('Click here!', 1, COLOUR_OF_TEXT, COLOUR_OF_BUTTONS)
        self.place_of_main_button = self.main_button_rendered.get_rect(center=CENTER_OF_MAIN_BUTTON)
        self.BuySimpleClicker_button_rendered = self.button_text.render(
            'Buy Simple Clicker', 1, COLOUR_OF_TEXT, COLOUR_OF_BUTTONS
        )
        self.place_of_BuySimpleClicker_button = self.BuySimpleClicker_button_rendered.get_rect(
            center=CENTER_OF_BUTTON_BUY_SIMPLE_CLICKER
        )
        self.BuyUpgradedClicker_button_rendered = self.button_text.render(
            'Buy Upgraded Clicker', 1, COLOUR_OF_TEXT, COLOUR_OF_BUTTONS
        )
        self.place_of_BuyUpgradedClicker_button = self.BuyUpgradedClicker_button_rendered.get_rect(
            center=CENTER_OF_BUTTON_BUY_UPGRADED_CLICKER
        )
        pygame.display.set_caption('Clicker')
        pygame.display.update()

    async def start(self, score):
        while True:
            for event in pygame.event.get():
                # exit from game
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    exit()
                # hand click
                if event.type == pygame.MOUSEBUTTONDOWN and self.place_of_main_button.collidepoint(event.pos):
                    await self.game_event_queue.put(HandClick())
                # buy simple clicker
                if event.type == pygame.MOUSEBUTTONUP and self.place_of_BuySimpleClicker_button.collidepoint(event.pos):
                    await self.game_event_queue.put(BuyAutoClicker(SimpleClicker))
                # buy upgraded clicker
                if event.type == pygame.MOUSEBUTTONUP and self.place_of_BuyUpgradedClicker_button.collidepoint(event.pos):
                    await self.game_event_queue.put(BuyAutoClicker(UpgradedClicker))
            self.main_surface.fill(COLOUR_OF_FIELD)
            self.render_score(score)
            self.render_buttons()
            pygame.display.update()
            await asyncio.sleep(1 / FPS)
        raise CancelledError

    def render_score(self, score):
        score_text_rendered = self.score_text.render('Score: ', 1, COLOUR_OF_TEXT, COLOUR_OF_FIELD)
        place_of_score = score_text_rendered.get_rect(center=(WINDOW_WIDTH // 8, WINDOW_HEIGHT // 12))
        self.main_surface.blit(score_text_rendered, place_of_score)
        points_text_rendered = self.score_text.render(str(score), 1, COLOUR_OF_TEXT, COLOUR_OF_FIELD)
        place_of_points = points_text_rendered.get_rect(
            center=(WINDOW_WIDTH // 4 + 9 * (len(str(score))) - 20, WINDOW_HEIGHT // 12)
        )
        self.main_surface.blit(points_text_rendered, place_of_points)

    def render_buttons(self):
        self.render_main_button()
        self.render_button_BuySimpleClicker()
        self.render_button_BuyUpgradedClicker()

    def render_main_button(self):
        center = CENTER_OF_MAIN_BUTTON
        radius = RADIUS_OF_MAIN_BUTTON
        pygame.draw.circle(self.main_surface, COLOUR_OF_BUTTONS, center, radius)
        self.main_surface.blit(self.main_button_rendered, self.place_of_main_button)

    def render_button_BuySimpleClicker(self):
        center = CENTER_OF_BUTTON_BUY_SIMPLE_CLICKER
        height = HEIGHT_OF_BUTTONS
        width = WIDTH_OF_BUTTONS
        pygame.draw.rect(self.main_surface, COLOUR_OF_BUTTONS,
                         (center[0] - width // 2, center[1] - height // 2, width, height))

        self.main_surface.blit(self.BuySimpleClicker_button_rendered, self.place_of_BuySimpleClicker_button)

    def render_button_BuyUpgradedClicker(self):
        center = CENTER_OF_BUTTON_BUY_UPGRADED_CLICKER
        height = HEIGHT_OF_BUTTONS
        width = WIDTH_OF_BUTTONS
        pygame.draw.rect(self.main_surface, COLOUR_OF_BUTTONS,
                         (center[0] - width // 2, center[1] - height // 2, width, height))

        self.main_surface.blit(self.BuyUpgradedClicker_button_rendered, self.place_of_BuyUpgradedClicker_button)
