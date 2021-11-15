from os import spawnlpe
import pygame
from sys import exit
from random import randint

from pygame import display

def create_score(time):
    test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
    score_surface = test_font.render(time, False, TEXT_COLOR)
    score_rect = score_surface.get_rect(center = (SCREEN_WITDH/2, 50))
    screen.blit(score_surface, score_rect)

def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    create_score(f'Score: {current_time}')
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= SNAIL_SPEED

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in  obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

SCREEN_WITDH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 300
TEXT_COLOR = (64,64,64)
BOX_COLOR = '#c0e8ec'
JUMP_HEIGHT = -20
GRAVITY = 1
SNAIL_SPEED = 5
SCREEN_COLOR = (94, 129, 162)
SPLASH_TEXT_COLOR = (111, 196,169)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WITDH, SCREEN_HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Obstacles
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surface = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
obstacle_rect_list = []

player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_ract = player_surface.get_rect(midbottom = (80, GROUND_HEIGHT))
player_gravity = 0

player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_name = test_font.render('Pixel Runner',False, SPLASH_TEXT_COLOR)
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = test_font.render('Press space to run', False, SPLASH_TEXT_COLOR)
game_message_rect = game_message.get_rect(center = (400, 320))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    if player_gravity >= 0:
                        if player_ract.bottom >= GROUND_HEIGHT:
                            player_gravity = JUMP_HEIGHT                
                else:
                    game_active = True
                    start_time = pygame.time.get_ticks()
            
            if event.key == pygame.K_q:
                pygame.quit()
                exit()
        
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surface.get_rect(bottomleft = (randint(900, 1100), GROUND_HEIGHT)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(bottomleft = (randint(900, 1100), GROUND_HEIGHT -90)))
        
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,GROUND_HEIGHT))

        # snail_ract.x -= SNAIL_SPEED
        # if snail_ract.right <= 0: snail_ract.left = SCREEN_WITDH
        # screen.blit(snail_surface, snail_ract)

        player_gravity += GRAVITY
        player_ract.y += player_gravity
        if player_ract.bottom >= 300: player_ract.bottom = GROUND_HEIGHT

        screen.blit(player_surface, player_ract)

        # Obstacle movment
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active = collisions(player_ract, obstacle_rect_list)
        # if snail_ract.colliderect(player_ract):
        #     game_active = False

        display_score()
        score = display_score()
    else:
        screen.fill((94, 129, 162))
        screen.blit(game_name, game_name_rect)
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_ract.midbottom = (80,GROUND_HEIGHT)

        score_message = test_font.render(f'Your score: {score}', False, SPLASH_TEXT_COLOR)
        score_message_rect = score_message.get_rect(center = (400, 330))
        
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)