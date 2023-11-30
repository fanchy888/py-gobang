import pygame
from client.game import OnlineGameClient, SingleGameClient, online_game


class Menu:
    SINGLE = 1
    ONLINE = 2

    JOINED = 1
    READY = 2
    STARTED = 3

    def __init__(self, window_size, font):
        self.mode = 0
        self.window_size = window_size
        self.menu_size = window_size[0]//2, window_size[1]//2
        self.font = font
        self.surface = pygame.Surface(self.menu_size, pygame.SRCALPHA, 32).convert_alpha()
        self.buttons = []
        self.ready_button = None
        self.make_buttons()
        self.pos = (self.window_size[0] - self.menu_size[0])//2, (self.window_size[1] - self.menu_size[1])//2
        self.state = 0

    def make_buttons(self):
        buttons = [
            {'name': 'Single', 'value': self.SINGLE, 'enabled': False},
            {'name': 'Online', 'value': self.ONLINE, 'enabled': True},
        ]
        res = []
        btn_size = (200, 60)
        x = (self.menu_size[0] - btn_size[0]) // 2
        for i, b in enumerate(buttons):
            y = i * (btn_size[1] + 60) + self.menu_size[1] // 4
            button = Button(self.surface, self.font, b, (x, y), btn_size)
            res.append(button)
        self.buttons = res

        btn_size = (200, 80)
        y = (self.menu_size[1] - 80) // 2
        self.ready_button = Button(self.surface, self.font,
                                   {'name': 'Ready', 'value': True, 'enabled': True}, (x, y), btn_size)

    def generate_game(self, mode):
        if mode == self.ONLINE:
            online_game.make_init()
            return online_game

        elif mode == self.SINGLE:
            return SingleGameClient()

    def draw(self):
        self.surface.fill((0,0,0,0))
        x, y = pygame.mouse.get_pos()
        relative_mouse_pos = x - self.pos[0], y - self.pos[1]
        if self.state < self.JOINED:
            for btn in self.buttons:
                btn.draw(relative_mouse_pos)

        elif self.state == self.JOINED:
            self.ready_button.draw(relative_mouse_pos)

    def click_mode(self):
        x, y = pygame.mouse.get_pos()
        relative_mouse_pos = x - self.pos[0], y - self.pos[1]
        for btn in self.buttons:
            if btn.enabled and btn.check_hover(relative_mouse_pos):
                self.state = self.JOINED
                return self.generate_game(btn.value)
        return None

    def click_ready(self):
        x, y = pygame.mouse.get_pos()
        relative_mouse_pos = x - self.pos[0], y - self.pos[1]
        btn = self.ready_button
        if btn.enabled and btn.check_hover(relative_mouse_pos):
            self.state = self.READY
            return btn.value
        return False


class Button:
    def __init__(self, surface, font, info, relative_pos, size):
        self.size = size
        self.relative_pos = relative_pos
        self.surface = surface
        self.value = info['value']
        self.enabled = info['enabled']
        self.color = (130, 130, 130) if self.enabled else (200, 200, 200)

        self.font = font
        self.text_color = (249, 205, 173)
        self.text = self.font.render(info['name'], True, self.text_color)
        self.text_size = self.text.get_size()
        self.text_pos = (self.size[0] - self.text_size[0]) // 2 + self.relative_pos[0], \
            (self.size[1] - self.text_size[1]) // 2 + self.relative_pos[1]

    def draw(self, mouse_pos):
        if self.check_hover(mouse_pos) and self.enabled:
            pygame.draw.rect(self.surface, [i-50 for i in self.color], (self.relative_pos, self.size))
            self.surface.blit(self.text, self.text_pos)
        else:
            pygame.draw.rect(self.surface, self.color, (self.relative_pos, self.size))
            self.surface.blit(self.text, self.text_pos)

    def check_hover(self, mouse_pos):
        return self.relative_pos[0] <= mouse_pos[0] <= self.relative_pos[0] + self.size[0] and \
            self.relative_pos[1] <= mouse_pos[1] <= self.relative_pos[1] + self.size[1]




