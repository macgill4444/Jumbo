import pygame, os, sys, characters, pyganim
from pygame.locals import *

class Spiderweb(pygame.sprite.Sprite):
    def load_image(self, image_name):
        try:
            image = pygame.image.load(image_name)
        except pygame.error, message:
            print"Cannot load image " + image_name
            raise SystemExit, message
        return image.convert_alpha()


    def __init__(self, x, y):
        self.image = self.load_image('assets/web.jpeg')
        self.rect = self.image.get_rect().move(x, y)
        
    def update(self, hero, platform):
        if self.rect.colliderect(hero.rect):
            caughtHero(hero)

    def draw(self, screen, world):
        draw_pos = self.rect
        screen.blit(self.image, draw_pos.move(world))

    def caughtHero(self, hero):
        #still need to work on this, hero should not be able to move if caught
        #in web
        hero.moveVector[1] = 2
    

if __name__ == "__main__":

        #Constants
        FPS = 50
        SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

        #init pygame
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        pygame.display.set_caption('toxic drop demo')
        clock = pygame.time.Clock()

        web = Spiderweb(100, 200)
        hero = characters.Hero()
        #Game loop
        while True:
            time_passed = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            screen.fill((255,255,255))

            web.update(hero, None)
            web.draw(screen, (0,0))
            pygame.display.update()
