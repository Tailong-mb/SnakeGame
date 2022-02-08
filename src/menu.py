import pygame
import button
import snakeGame
from pygame import mixer

SCREEN_WIDTH = 520
SCREEN_HEIGHT = 520

def menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Menu')

    #Load image
    snakeGame_img = pygame.image.load('../image/snake_img.jpg').convert_alpha()
    hard_button_img = pygame.image.load('../image/hard_button.png').convert_alpha()
    normal_button_img = pygame.image.load('../image/normal_button.png').convert_alpha()
    #Set button
    snakeGame_button = button.Button(200, 20, snakeGame_img)
    hard_button = button.Button(140,300, normal_button_img)
    normal_button = button.Button(140,150, hard_button_img)
    #Set boolean for choice
    sound = True
    normal_game = False
    hard_game = False
    run = True
    Music = True
    #button music
    sound_button_img = pygame.image.load('../image/audio_button.png')
    mute_button_img = pygame.image.load('../image/mute_button.png')
    sound_button = button.Button(500, 5, sound_button_img)
    mute_button = button.Button(500, 5, mute_button_img)
    while run:
        #Music
        if Music:
            mixer.music.load('../music/SnakeGameMenuMusic.wav')
            mixer.music.set_volume(0.25)
            mixer.music.play(-1)
            Music = False
        #Color Background
        screen.fill((255, 255, 255))
        #snake icon
        if snakeGame_button.draw(screen):
            Music = False
        #Mute music choice
        if sound:
            if sound_button.draw(screen):
                sound = False
                mixer.music.set_volume(0)
        else:
            if mute_button.draw(screen):
                sound = True
                mixer.music.set_volume(0.25)
        #Conditions when one of the icons are pressed
        if hard_button.draw(screen):
            normal_game = True
        if normal_button.draw(screen):
            hard_game = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
        #launch game
        if normal_game:
            snakeGame.main_game(False)
            normal_game = False
            Music = True
        if hard_game:
            snakeGame.main_game(True)
            hard_game = False
            Music = True
    pygame.quit()
