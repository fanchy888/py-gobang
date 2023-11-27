# -*- coding: utf-8 -*-
import pygame
import sys

from client import game_client
from gobang.board import Board

pygame.init()

RULE = 19
ROW_COUNT = RULE - 1
COLUMN_COUNT = RULE - 1
SQUARE_SIZE = 40

width = (COLUMN_COUNT + 2) * SQUARE_SIZE
height = (ROW_COUNT + 2) * SQUARE_SIZE
size = (width, height)

start_point = (SQUARE_SIZE, SQUARE_SIZE)
board_size = (COLUMN_COUNT * SQUARE_SIZE, ROW_COUNT * SQUARE_SIZE)
length = COLUMN_COUNT * SQUARE_SIZE
piece_size = 18

BLACK = (20, 20, 20)
WHITE = (230, 230, 230)
CIRCLE = (220, 20, 20)
BACKGROUND = (230, 206, 172)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('五子棋')
        self.game = game_client
        self.player = None

    def quit(self):
        pygame.quit()

    def draw(self):
        self.draw_board()
        self.draw_piece()
        self.draw_mouse()
        pygame.display.update()

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

    def play(self):
        if self.game.is_my_turn:
            x, y = self.get_mouse_pos()
            if ROW_COUNT >= x >= 0 and COLUMN_COUNT >= y >= 0:
                self.game.play(x, y)


if __name__ == '__main__':

    game = Game()
    # 游戏主循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                game.play()
        game.draw()
    game.quit()
