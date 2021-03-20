import pygame, sys, random
import os
import numpy
import pandas as pd

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,450))
    screen.blit(floor_surface,(floor_x_pos + 288,450))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (350,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (350,random_pipe_pos-100))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        return False

    return True

pygame.init()
screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True

asset_url1 = resource_path('assets/background-day.png')
bg_surface = pygame.image.load(asset_url1).convert()
# bg_surface = pygame.transform.scale2x(bg_surface)
# if you want to 2x the size of surface

asset_url2 = resource_path('assets/base.png')
floor_surface = pygame.image.load(asset_url2).convert()
floor_x_pos = 0

asset_url3 = resource_path('assets/bluebird-midflap.png')
bird_surface = pygame.image.load(asset_url3).convert()
bird_rect = bird_surface.get_rect(center = (50,256)) # puts rectangle around bg_surface

asset_url4 = resource_path('assets/pipe-green.png')
pipe_surface = pygame.image.load(asset_url4)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT    # event triggered by timer
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [375,350,300,270]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50,256)
                bird_movement = 0


        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface,(0,0))

    if game_active:
        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface,bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0


    pygame.display.update()
    clock.tick(100)
