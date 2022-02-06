# import lib
import random
import sys

import pygame
from pygame import mixer

#Snake class
class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_HEIGHT / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (255, 197, 15)
        self.score = 0
    #Return the head position of the snake
    def get_head_position(self):
        return self.positions[0]
    #Turn snake method
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    #Move snake method
    def move(self):
        current_position = self.get_head_position()
        x, y = self.direction
        new_position = (
            ((current_position[0] + (x * GRIDSIZE)) % SCREEN_WIDTH),
            (current_position[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)
        # Conditions of reset with himself
        if len(self.positions) > 2 and new_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.positions.pop()
    #Score update method
    def update_score(self):
        self.score += 1
    #Reset method
    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_HEIGHT / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
    #Draw snake method
    def draw(self, surface):
        for p in self.positions:
            d = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, d)
            pygame.draw.rect(surface, (93, 216, 113), d, 1)
    #Key to movement method
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
#Food class
class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (236, 27, 68)
        self.randomize_position()
    #Randomize the position of the food
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRIDSIZE, random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE)
    #draw the food object
    def draw(self, surface):
        food_draw = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, food_draw)
        pygame.draw.rect(surface, (93, 216, 113), food_draw, 1)
#Block class
class Block(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (137, 41, 20)
        self.randomize_position()
    #Randomize Block position
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRIDSIZE, random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE)
    #Draw the Block object
    def draw(self, surface):
        block_draw = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, block_draw)
        pygame.draw.rect(surface, (93, 216, 113), block_draw, 1)
#Draw the grid for the SnakeGame
def draw_grid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                type_square_one = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (93, 216, 113), type_square_one)
            else:
                type_square_two = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (97, 223, 119), type_square_two)

#Const values screen
SCREEN_WIDTH = 520
SCREEN_HEIGHT = 520
#Const values grid
GRIDSIZE = 20
GRID_WIDTH = SCREEN_HEIGHT / GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH / GRIDSIZE
#Const values movements
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

#Main for normal SnakeGame
def main_normal():
    #Initialisation
    pygame.init()
    #Background sound
    mixer.music.load('../music/SnakeGameNormalMusic.wav')
    mixer.music.set_volume(0.25)
    mixer.music.play(-1)
    #Clock and screen
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('SnakeGame normal')

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)

    snake = Snake()
    food = Food()
    font_score = pygame.font.SysFont("monospace", 16)
    #Game Start
    while True:
        clock.tick(10)
        snake.handle_key()
        draw_grid(surface)
        snake.move()
        #When the snake reach food position
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.update_score()
            food.randomize_position()
            #Check if the food is on the snake
            while food.position in snake.positions:
                food.randomize_position()
        #Draw after update
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        score_text = font_score.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(score_text, (5, 10))
        pygame.display.update()

#Hard mode for SnakeGame
def main_hard():
    #Initialisation
    pygame.init()
    #Background sound
    mixer.music.load('../music/SnakeGameHardMusic.wav')
    mixer.music.set_volume(0.25)
    mixer.music.play(-1)
    #Clock and screen
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('SnakeGame hard')

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)

    snake = Snake()
    food = Food()
    font_score = pygame.font.SysFont("monospace", 16)
    block_list = []
#Game start
    while True:
        clock.tick(10)
        snake.handle_key()
        draw_grid(surface)
        snake.move()
        #Reset block spawn if the snake reset (caused by himself)
        if snake.score == 0:
            block_list.clear()
        #When snake reach food position
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.update_score()
            food.randomize_position()
            food_position_ok = True
            block = Block()
            #Test if the block spawned on the snake (no matter if a block spawn on a block here)
            while block.position in food.position or block.position in snake.positions:
                block.randomize_position()
            block_list.append(block)
            #Check the spawn of the food (not on a block, not on the snake)
            while food_position_ok:
                food.randomize_position()
                food_position_ok = False
                #Check if the food is on a block
                for block_test in block_list:
                    if block_test == food.position:
                        food_position_ok = True
                #Check if the position is on the snake
                if food.position in snake.positions:
                    food_position_ok = True
        else:
            #When the snake reach a block
            for block_test in block_list:
                if snake.get_head_position() == block_test.position:
                    snake.reset()
                    block_list.clear()
        #Draw after update
        for block_test in block_list:
            block_test.draw(surface)
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        score_text = font_score.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(score_text, (5, 10))
        pygame.display.update()

