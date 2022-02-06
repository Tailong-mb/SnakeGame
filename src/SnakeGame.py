# import lib
import random
import sys

import pygame


class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_HEIGHT / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (146, 140, 141)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        current_position = self.get_head_position()
        x, y = self.direction
        new_position = (
            ((current_position[0] + (x * GRIDSIZE)) % SCREEN_WIDTH),
            (current_position[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)
        # condition of reset
        if len(self.positions) > 2 and new_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.positions.pop()

    def update_score(self):
        self.score += 1

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_HEIGHT / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            d = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, d)
            pygame.draw.rect(surface, (93, 216, 113), d, 1)

    def handle_key(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)

class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (236, 27, 68)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRIDSIZE, random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE)

    def draw(self, surface):
        food_draw = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, food_draw)
        pygame.draw.rect(surface, (93, 216, 113), food_draw, 1)

class Block(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (137, 41, 20)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRIDSIZE, random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE)

    def draw(self, surface):
        block_draw = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, block_draw)
        pygame.draw.rect(surface, (93, 216, 113), block_draw, 1)

def draw_grid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                type_square_one = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (93, 216, 113), type_square_one)
            else:
                type_square_two = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (93, 216, 113), type_square_two)


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRIDSIZE = 20
GRID_WIDTH = SCREEN_HEIGHT / GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH / GRIDSIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def main_normal():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)

    snake = Snake()
    food = Food()
    font_score = pygame.font.SysFont("monospace", 16)

    while True:
        clock.tick(10)
        snake.handle_key()
        draw_grid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.update_score()
            food.randomize_position()
            while food.position in snake.positions:
                food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        score_text = font_score.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(score_text, (5, 10))
        pygame.display.update()

def main_hard():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)

    snake = Snake()
    food = Food()
    font_score = pygame.font.SysFont("monospace", 16)
    block_list = []

    while True:
        clock.tick(10)
        snake.handle_key()
        draw_grid(surface)
        snake.move()
        if snake.score == 0:
            block_list.clear()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.update_score()
            food.randomize_position()
            food_position_ok = True
            block = Block()
            while block.position in food.position or block.position in snake.positions:
                block.randomize_position()
            block_list.append(block)
            while food_position_ok:
                food.randomize_position()
                food_position_ok = False
                for block_test in block_list:
                    if block_test == food.position:
                        food_position_ok = True
        for block_test in block_list:
            if snake.get_head_position() == block_test.position:
                snake.reset()
                block_list.clear()
        for block_test in block_list:
            block_test.draw(surface)
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        score_text = font_score.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(score_text, (5, 10))
        pygame.display.update()

main_hard()
