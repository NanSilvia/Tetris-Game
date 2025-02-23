from settings import *
import random


# we use sprite => block needs to inherit from it
# pygame.sprite.Sprite = Simple base class for visible game objects
class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):  # will also keep the position of the tetromino on the board as a tuple of form (x, y)
        self.tetromino = tetromino
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.next_pos = vec(pos) + NEXT_POS_OFFSET
        self.alive = True

        super().__init__(tetromino.tetris.sprite_group)
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pg.Surface([TILE_SIZE, TILE_SIZE])
        # self.image.fill('blue')
        pg.draw.rect(self.image, 'blue', (1, 1, TILE_SIZE - 2, TILE_SIZE - 2), border_radius=3)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y if necessary
        self.rect = self.image.get_rect()


    def is_alive(self):
        if not self.alive:
            self.kill()

    def rotate(self, pivot_pos):
        """"rotation of a block by 90 degrees"""
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos

    def set_rect_pos(self):
        pos = [self.next_pos, self.pos][self.tetromino.current]
        self.rect.topleft = pos * TILE_SIZE

    def update(self):
        self.is_alive()
        self.set_rect_pos()

    def is_collide(self, pos):
        """"if no collision = > will return false
        if the block is above the play field it.s not taken into account"""
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < FIELD_W and y < FIELD_H and (
                y < 0 or not self.tetromino.tetris.field_array[y][x]):
            return False
        return True


class Tetromino:
    def __init__(self, tetris, current=True):
        self.tetris = tetris
        self.shape = random.choice(list(TETROMINOES.keys()))
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]]
        self.landing = False  # this announces if the tetromino is in it's final position so it cpould.t be moved again(aka stanga dreapta)
        self.current = current

    def rotate(self):
        """"rotate each block of that specific shape and if it is ok=> we rotate it by assigning the new coordinates"""
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.is_collide(new_block_positions): # if no collisions=> we can assign a new position to each block
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]

    def is_collide(self, block_positions):
        return any(map(Block.is_collide, self.blocks, block_positions))
    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_positions)

        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == 'down':
            self.landing = True

    def update(self):
        self.move(direction='down')

        # pg.time.wait(200)
        # this is fine at first, but when we move the tetromonos on the board it will also have a delay
                # and it's not very nice => so we make a timintervalk fo animation

