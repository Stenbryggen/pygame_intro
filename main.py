import pygame
from sys import exit

from pygame import display

SCREEN_WITDH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 300
TEXT_COLOR = (64,64,64)
BOX_COLOR = '#c0e8ec'
JUMP_HEIGHT = -20
GRAVITY = 1
SNAIL_SPEED = 5

pygame.init()
screen = pygame.display.set_mode((SCREEN_WITDH, SCREEN_HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = True

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

text_surface = test_font.render('Runner', False, TEXT_COLOR)
text_rect = text_surface.get_rect(center = (SCREEN_WITDH/2,50))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_ract = snail_surface.get_rect(bottomleft = (SCREEN_WITDH, GROUND_HEIGHT))

player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_ract = player_surface.get_rect(midbottom = (80, GROUND_HEIGHT))
player_gravity = 0

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
    
 
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,GROUND_HEIGHT))
        pygame.draw.rect(screen, BOX_COLOR, text_rect)
        pygame.draw.rect(screen, BOX_COLOR, text_rect, 10)
        screen.blit(text_surface, text_rect)

        snail_ract.x -= SNAIL_SPEED
        if snail_ract.right <= 0: snail_ract.left = SCREEN_WITDH
        screen.blit(snail_surface, snail_ract)

        player_gravity += GRAVITY
        player_ract.y += player_gravity
        if player_ract.bottom >= 300: player_ract.bottom = GROUND_HEIGHT

        screen.blit(player_surface, player_ract)

        if snail_ract.colliderect(player_ract):
            game_active = False
    else:
        screen.fill('Yellow')


    pygame.display.update()
    clock.tick(60)