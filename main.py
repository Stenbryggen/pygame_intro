import pygame
from sys import exit

from pygame import display

def create_score(time):
    test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
    score_surface = test_font.render(time, False, TEXT_COLOR)
    score_rect = score_surface.get_rect(center = (SCREEN_WITDH/2, 50))
    screen.blit(score_surface, score_rect)

def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    create_score(f'Score: {current_time}')

SCREEN_WITDH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 300
TEXT_COLOR = (64,64,64)
BOX_COLOR = '#c0e8ec'
JUMP_HEIGHT = -20
GRAVITY = 1
SNAIL_SPEED = 5
SCREEN_COLOR = (94, 129, 162)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WITDH, SCREEN_HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
game_active = False
start_time = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_ract = snail_surface.get_rect(bottomleft = (SCREEN_WITDH, GROUND_HEIGHT))

player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_ract = player_surface.get_rect(midbottom = (80, GROUND_HEIGHT))
player_gravity = 0

player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_name = test_font.render('Pixel Runner',False, (111, 196,169))
game_name_rect = game_name.get_rect(center = (400, 80))

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
                    snail_ract.left = SCREEN_WITDH
                    start_time = pygame.time.get_ticks()
            
            if event.key == pygame.K_q:
                pygame.quit()
                exit()

    
 
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,GROUND_HEIGHT))

        snail_ract.x -= SNAIL_SPEED
        if snail_ract.right <= 0: snail_ract.left = SCREEN_WITDH
        screen.blit(snail_surface, snail_ract)

        player_gravity += GRAVITY
        player_ract.y += player_gravity
        if player_ract.bottom >= 300: player_ract.bottom = GROUND_HEIGHT

        screen.blit(player_surface, player_ract)

        if snail_ract.colliderect(player_ract):
            game_active = False

        display_score()
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(game_name, game_name_rect)

    pygame.display.update()
    clock.tick(60)