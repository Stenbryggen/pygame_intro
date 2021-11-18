from os import spawnlpe
import pygame
from sys import breakpointhook, exit
from random import randint, choices

from pygame import display
from pygame.key import get_pressed

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == ['fly']:
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

def create_score(time):
    test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
    score_surface = test_font.render(time, False, TEXT_COLOR)
    score_rect = score_surface.get_rect(center = (SCREEN_WITDH/2, 50))
    screen.blit(score_surface, score_rect)

def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    create_score(f'Score: {current_time}')
    return current_time

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
game_music = pygame.mixer.Sound('audio/music.wav')

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

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
                if not game_active:
                    game_active = True
                    start_time = pygame.time.get_ticks()
            
            if event.key == pygame.K_q:
                pygame.quit()
                exit()
        
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choices(['fly', 'snail', 'snail', 'snail'])))

    if game_active:
        game_music.play(loops = -1)
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,GROUND_HEIGHT))

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

        display_score()
        score = display_score()
    else:
        game_music.stop()
        screen.fill((94, 129, 162))
        screen.blit(game_name, game_name_rect)
        screen.blit(player_stand,player_stand_rect)

        score_message = test_font.render(f'Your score: {score}', False, SPLASH_TEXT_COLOR)
        score_message_rect = score_message.get_rect(center = (400, 330))
        
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)