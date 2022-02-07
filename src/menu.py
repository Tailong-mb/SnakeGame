import pygame
import button
import snakeGame

SCREEN_WIDTH = 520
SCREEN_HEIGHT = 520

def menu():

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Menu')

    #Load image
    hard_button_img = pygame.image.load('../image/hard_button.png').convert_alpha()
    normal_button_img = pygame.image.load('../image/normal_button.png').convert_alpha()
    #Set button
    hard_button = button.Button(140,300, normal_button_img)
    normal_button = button.Button(140,150, hard_button_img)
    #Set boolean for choice
    normal_game = False
    hard_game = False
    run = True
    while run:

        screen.fill((38, 154, 57))

        if hard_button.draw(screen):
            normal_game = True
            run = False
        if normal_button.draw(screen):
            hard_game = True
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    if normal_game:
        snakeGame.main_game(False)
    if hard_game:
        snakeGame.main_game(True)
    pygame.quit()
