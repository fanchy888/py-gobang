# -*- coding: utf-8 -*-
import pygame
import sys

from client.menu import Menu
from config import config

pygame.init()

RULE = config.rule
ROW_COUNT = RULE - 1
COLUMN_COUNT = RULE - 1
SQUARE_SIZE = 40

width = (COLUMN_COUNT + 2) * SQUARE_SIZE
height = (ROW_COUNT + 4) * SQUARE_SIZE
size = (width, height)

start_point = (SQUARE_SIZE, SQUARE_SIZE*2)
board_size = (COLUMN_COUNT * SQUARE_SIZE, ROW_COUNT * SQUARE_SIZE)
length = COLUMN_COUNT * SQUARE_SIZE
piece_size = 18

BLACK = (20, 20, 20)
WHITE = (230, 230, 230)
CIRCLE = (220, 20, 20)
BACKGROUND = (230, 206, 172)

FONT = pygame.font.SysFont('pingfang', 30)
FONT2 = pygame.font.SysFont('pingfang', 45)


class MainWindow:
    def __init__(self):
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('五子棋')
        self.menu = Menu(size, FONT)
        self.game = None

    def quit(self):
        self.game = None
        pygame.quit()

    def draw(self):
        self.draw_board()
        if self.game is None or self.menu.state < self.menu.READY:
            self.draw_menu()
        else:
            self.draw_game()
        pygame.display.update()

    def draw_menu(self):
        self.screen.blit(self.menu.surface, self.menu.pos)
        self.menu.draw()

    def draw_board(self):
        self.screen.fill(BACKGROUND)
        pygame.draw.rect(self.screen, BLACK, (start_point, board_size), 4, 4)
        for i in range(1, ROW_COUNT):
            x = start_point[0]
            y = start_point[1] + i * SQUARE_SIZE
            pygame.draw.line(self.screen, BLACK, (x, y), (x+length-1, y), 2)

        for i in range(1, COLUMN_COUNT):
            x = start_point[0] + i * SQUARE_SIZE
            y = start_point[1]
            pygame.draw.line(self.screen, BLACK, (x, y), (x, y+length-1), 2)

        center = COLUMN_COUNT // 2 * SQUARE_SIZE
        pygame.draw.circle(self.screen, BLACK, (start_point[0]+center, start_point[1]+center), 6)

    @classmethod
    def get_mouse_pos(cls):
        x, y = pygame.mouse.get_pos()
        x = round((x - start_point[0]) / SQUARE_SIZE)
        y = round((y - start_point[1]) / SQUARE_SIZE)
        return x, y

    def draw_game(self):
        self.draw_head()
        if self.game.started:
            self.draw_piece()
            self.draw_mouse()
        if self.game.state == self.game.END:
            self.draw_end()

    def draw_head(self):
        x, y = SQUARE_SIZE, SQUARE_SIZE

        user1 = FONT.render('You: ', True, (130, 130, 130))
        t_length, t_height = user1.get_size()
        self.screen.blit(user1, (x, y-t_height//2))
        if self.game.color:
            pygame.draw.circle(self.screen, BLACK if self.game.color == 1 else WHITE, (x+t_length+piece_size, y), piece_size)

        if self.game.started:
            user2 = FONT.render('Opp: ', True, (130, 130, 130))
            t_length, t_height = user2.get_size()
            x = size[0] - SQUARE_SIZE - piece_size * 2 - t_length
            self.screen.blit(user2, (x, y-t_height//2))
            pygame.draw.circle(self.screen, WHITE if self.game.color == 1 else BLACK, (x+t_length+piece_size, y), piece_size)
            pygame.draw.circle(self.screen, BLACK if self.game.is_black else WHITE, (size[0]//2, y), piece_size)

        else:
            user2 = FONT.render('Waiting...', True, (130, 130, 130))
            t_length, t_height = user2.get_size()
            x, y = (size[0] - SQUARE_SIZE - t_length, SQUARE_SIZE)
            self.screen.blit(user2, (x, y-t_height//2))

    def draw_mouse(self):
        x, y = self.get_mouse_pos()
        if ROW_COUNT >= x >= 0 and COLUMN_COUNT >= y >= 0 and not self.game.board.board[x][y]:
            point = (start_point[0]+x*SQUARE_SIZE, start_point[1]+y*SQUARE_SIZE)
            pygame.draw.circle(self.screen, CIRCLE, point, piece_size, 3)

    def draw_piece(self):
        for i, row in enumerate(self.game.board.board):
            for j, value in enumerate(row):
                if value:
                    x = i * SQUARE_SIZE + start_point[0]
                    y = j * SQUARE_SIZE + start_point[1]
                    pygame.draw.circle(self.screen, BLACK if value == 1 else WHITE, (x, y), piece_size)
        if self.game.board.last:
            pygame.draw.rect(self.screen, (137, 190, 178),
                             (self.game.board.last[0] * SQUARE_SIZE + start_point[0] - SQUARE_SIZE//2,
                              self.game.board.last[1] * SQUARE_SIZE + start_point[1] - SQUARE_SIZE//2,
                              SQUARE_SIZE, SQUARE_SIZE), 2)

    def draw_end(self):
        if self.game.winner:
            txt = 'You win!' if self.game.winner == self.game.color else 'You lose!'
            msg = FONT2.render(txt, True, (1, 77, 130))
            w, h = msg.get_size()
            self.screen.blit(msg, ((size[0]-w)//2, size[1]//2-h-50))

        msg = FONT.render('Click to continue', True, (20, 20, 20))
        w, h = msg.get_size()
        self.screen.blit(msg, ((size[0]-w)//2, size[1]//2+50))

    def click(self):
        if self.menu.state < self.menu.JOINED:
            self.game = self.menu.click_mode()
        elif self.menu.state == self.menu.JOINED:
            if self.menu.click_ready():
                self.game.ready()
        elif self.game:
            if self.game.started:
                self.play()
            elif self.game.state == self.game.END:
                x, y = self.get_mouse_pos()
                if ROW_COUNT >= x >= 0 and COLUMN_COUNT >= y >= 0:
                    self.menu.state = self.menu.JOINED
                    self.game.reset()

    def play(self):
        if self.game.is_my_turn:
            x, y = self.get_mouse_pos()
            if ROW_COUNT >= x >= 0 and COLUMN_COUNT >= y >= 0:
                self.game.play(x, y)


def run_game():
    game = MainWindow()
    # 游戏主循环
    running = True
    clicked = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                tick = pygame.time.get_ticks()
                if tick - clicked >= 100:  # 100ms delay
                    game.click()
                    clicked = tick
        game.draw()
    game.quit()


if __name__ == '__main__':
    run_game()

