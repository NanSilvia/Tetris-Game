from settings import *
import math
import pygame.freetype as ft

# it s an app instance
from tetromino import Tetromino

class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W*0.61, WIN_H*0.02), text='TETRIS', fgcolor = 'white', size=TILE_SIZE*1.65, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W*0.65, WIN_H*0.25), text='NEXT', fgcolor='white', size=TILE_SIZE*1.4, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W*0.65, WIN_H*0.65), text='SCORE', fgcolor='white', size=TILE_SIZE*1.4, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W*0.64, WIN_H*0.8), text=f'{self.app.tetris.score}', fgcolor='white', size=TILE_SIZE*1.8)


class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()  # this will contain all the blocks of all the tetrominos that we have on the playing board
        self.field_array = self.get_field_array() # this gets a matris with 0 for the possitions that are unoccupied on the board and we will fill it with 1's each time we do an update
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)

        self.speed_up = False

        self.score =0
        self.full_lines=0
        self.points_per_lines = {0:0, 1:100, 2:400, 3:700, 4:1000}


    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines=0

    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(300)
            return True


    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block
    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]

    def check_tetromino_landing(self):
        """"checks if we finished with a tetromino and makes a new tet to move around"""
        if self.tetromino.landing:
            if self.is_game_over():
                self.__init__(self.app)
            else:
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)


    def control(self, pressed_key):
        """"gets info about pressed key and moves the tetromino in that direction"""
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction='right')
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True

    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'black', (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()


    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)

    def check_full_lines(self):
        row = FIELD_H-1
        for j in range(FIELD_H-1, -1, -1):
            for i in range(FIELD_W):
                self.field_array[row][i] = self.field_array[j][i]

                if self.field_array[j][i]:
                    self.field_array[row][i].pos = vec(i, j)
            if sum(map(bool, self.field_array[j])) < FIELD_W:
                row -=1
            else:
                for i in range(FIELD_W):
                    self.field_array[row][i].alive = False
                    self.field_array[row][i] = 0
                self.full_lines += 1

