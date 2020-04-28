import pygame
from GameParameters import *
from GameEvent import *
from math import hypot


class Interface:
    def __init__(self, game_event_queue):
        pygame.init()
        self.main_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.main_surface.fill(COLOUR_OF_FIELD)
        self.score_text = pygame.font.Font(None, WINDOW_HEIGHT // 7)
        self.button_text = pygame.font.Font(None, WINDOW_HEIGHT // 10)
        self.info_text = pygame.font.Font(None, WINDOW_HEIGHT // 15)
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
                if self.hand_clicked(event):
                    await self.game_event_queue.put(HandClick())
                # buy simple clicker
                if self.pressed_BuySimpleClicker(event):
                    await self.game_event_queue.put(BuyAutoClicker(SimpleClicker))
                # buy upgraded clicker
                if self.pressed_BuyUpgradedClicker(event):
                    await self.game_event_queue.put(BuyAutoClicker(UpgradedClicker))
            self.main_surface.fill(COLOUR_OF_FIELD)
            self.render_score(score)
            self.render_points_per_sec(score)
            self.render_buttons()
            self.render_info()
            pygame.display.update()
            await asyncio.sleep(1 / FPS)

    def render_score(self, score):
        score_text_rendered = self.score_text.render('Score: ', 1, COLOUR_OF_TEXT, COLOUR_OF_FIELD)
        place_of_score = score_text_rendered.get_rect(center=(WINDOW_WIDTH // 8, WINDOW_HEIGHT // 12))
        self.main_surface.blit(score_text_rendered, place_of_score)
        points_text_rendered = self.score_text.render(str(score), 1, COLOUR_OF_TEXT, COLOUR_OF_FIELD)
        place_of_points = points_text_rendered.get_rect(
            center=(WINDOW_WIDTH // 4 + 9 * (len(str(score))) - 20, WINDOW_HEIGHT // 12)
        )
        self.main_surface.blit(points_text_rendered, place_of_points)

    def render_points_per_sec(self, score):
        points_per_sec_text_rendered = self.score_text.render('Point/sec: ', 1, COLOUR_OF_TEXT, COLOUR_OF_FIELD)
        place_of_points_per_sec = points_per_sec_text_rendered.get_rect(center=(WINDOW_WIDTH // 6, WINDOW_HEIGHT // 5))
        self.main_surface.blit(points_per_sec_text_rendered, place_of_points_per_sec)
        points_per_sec_text_rendered = self.score_text.render(
            str(round(score.point_per_sec, 2)), 1, COLOUR_OF_TEXT, COLOUR_OF_FIELD
        )
        place_of_points_per_sec = points_per_sec_text_rendered.get_rect(
            center=(WINDOW_WIDTH // 3 + 9 * (len(str(round(score.point_per_sec, 2)))) - 10, WINDOW_HEIGHT // 5)
        )
        self.main_surface.blit(points_per_sec_text_rendered, place_of_points_per_sec)

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

    def hand_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_pos = event.pos[0]
            y_pos = event.pos[1]
            center_x_pos = CENTER_OF_MAIN_BUTTON[0]
            center_y_pos = CENTER_OF_MAIN_BUTTON[1]
            return hypot(x_pos - center_x_pos, y_pos - center_y_pos) <= RADIUS_OF_MAIN_BUTTON

    def pressed_BuySimpleClicker(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            center = CENTER_OF_BUTTON_BUY_SIMPLE_CLICKER
            height = HEIGHT_OF_BUTTONS
            width = WIDTH_OF_BUTTONS
            button = pygame.Rect(center[0] - width // 2, center[1] - height // 2, width, height)
            return button.collidepoint(event.pos)

    def pressed_BuyUpgradedClicker(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            center = CENTER_OF_BUTTON_BUY_UPGRADED_CLICKER
            height = HEIGHT_OF_BUTTONS
            width = WIDTH_OF_BUTTONS
            button = pygame.Rect(center[0] - width // 2, center[1] - height // 2, width, height)
            return button.collidepoint(event.pos)

    def render_info(self):
        self.render_BuySimpleClicker_info()
        self.render_BuyUpgradedClicker_info()

    def render_BuySimpleClicker_info(self):
        center = list(CENTER_OF_BUTTON_BUY_SIMPLE_CLICKER)
        center[1] += 40
        center = tuple(center)
        height = HEIGHT_OF_BUTTONS // 2
        width = WIDTH_OF_BUTTONS
        pygame.draw.rect(self.main_surface, COLOUR_OF_BUTTONS,
                         (center[0] - width // 2, center[1] - height // 2, width, height))
        info_text_rendered = self.info_text.render(
            'Cost: {}, point/sec: {}'.format(round(SimpleClicker.cost, 2), round(SimpleClicker.init_points_per_sec, 2)),
            1,
            COLOUR_OF_TEXT, COLOUR_OF_BUTTONS
        )
        place_of_info = info_text_rendered.get_rect(center=center)
        self.main_surface.blit(info_text_rendered, place_of_info)

    def render_BuyUpgradedClicker_info(self):
        center = list(CENTER_OF_BUTTON_BUY_UPGRADED_CLICKER)
        center[1] += 40
        center = tuple(center)
        height = HEIGHT_OF_BUTTONS // 2
        width = WIDTH_OF_BUTTONS
        pygame.draw.rect(self.main_surface, COLOUR_OF_BUTTONS,
                         (center[0] - width // 2, center[1] - height // 2, width, height))
        info_text_rendered = self.info_text.render(
            'Cost: {}, point/sec: {}'.format(
                round(UpgradedClicker.cost, 2), round(UpgradedClicker.init_points_per_sec, 2)
            ),
            1, COLOUR_OF_TEXT, COLOUR_OF_BUTTONS
        )
        place_of_info = info_text_rendered.get_rect(center=center)
        self.main_surface.blit(info_text_rendered, place_of_info)
