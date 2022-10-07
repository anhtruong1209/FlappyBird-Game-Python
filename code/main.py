import pygame
import sys
import time
from utils import quit_game
from settings import *
from sprites import BG, Ground, Plane, Obstacle
from debug import debug

class Game:

    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        
        # sống chết :)
        self.active = True 
        
        # sprite group
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale background
        bg_height = pygame.image.load(
            '../graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # scale setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # text font
        self.font = pygame.font.Font(
            '../graphics/font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0
        self.start_offset = 0
        
        # menu
        self.menu_surf = pygame.image.load('../graphics/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        
        # sound
        self.music_all = pygame.mixer.Sound('../sounds/jump.wav')
        self.music_all.play(loops=-1)

    def collisions(self):
        # chạm nhau thì ...
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask)\
                or self.plane.rect.top <= 0:  # đã có Ground rồi nên chỉ cần để plane <=0 thôi là đủ
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.plane.kill()

    def display_score(self):
        if self.active: # Sống
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000 
            y = WINDOW_HEIGHT / 10
        else: # Chết
            y = WINDOW_HEIGHT / 2 + self.menu_rect.height

        score_surf = self.font.render("TruongHuFPTU "+ str(self.score) , True, 'black')
        score_rect = score_surf.get_rect(
            midtop=(WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        last_time = time.time()
        while True:
            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active: # Sống
                        self.plane.jump()

                    else: # Chết
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()

                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites],
                             self.scale_factor * 1.1)

            # game logic
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()
            
            if self.active: 
                self.collisions()
            else: 
                self.display_surface.blit(self.menu_surf, self.menu_rect)
            pygame.display.update()
            self.clock.tick(FRAME_RATE)


if __name__ == '__main__':
    game = Game()
    game.run()
