import pygame, os, sys, characters, pyganim
from pygame.locals import *

class Toxicdrip(pygame.sprite.Sprite):

    def load_image(self, image_name):
        try:
            image = pygame.image.load(image_name)
        except pygame.error, message:
            print"Cannot load image " + image_name
            raise SystemExit, message
        return image.convert_alpha()
    
    def __init__(self, x, y, ground, dy):
        pygame.sprite.Sprite.__init__(self)

        #load image for now we will use a rectangle
        self.image = self.load_image('assets/drop.jpg')
        self.rect = self.image.get_rect().move(x, y)

        self.dy = dy
        #ground is the y coordinate that the dorp should splatter
        #at if it doesn't hit player before
        self.ground = ground

        self.orig_x = x
        self.orig_y = y


    def update(self, hero, platforms):
        #check to see if drop has either hit a platform or a the player
        if self.rect.colliderect(hero.rect):
            self.hitHero(hero)

        if self.rect.collidepoint(self.rect.x, self.ground):
            self.explode()

        self.rect.y = self.rect.y + self.dy
            
    def hitHero(self, hero):
        #if the drop hits the player it needs to hurt him
        hero.hit(10, 0)
	self.explode()

    def explode(self):
        #reset the x and y coordinates if the drop splatters
        self.rect.x = self.orig_x
        self.rect.y = self.orig_y

    def draw(self, screen, world):
        draw_pos = self.rect
        screen.blit(self.image, draw_pos.move(world))

    def entityCollide(self, someBULLshit):
        pass

if __name__ == "__main__":

    #Constants
    FPS = 50
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    BACKGROUND_COLOR = (255, 255, 255)

    #init pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('toxic drop demo')
    clock = pygame.time.Clock()

    drip = Toxicdrip(300, -40, 500, 10)

    herox = 0
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

        screen.fill(BACKGROUND_COLOR)
        herox += 2
        if herox > screen.get_size()[0]:
            herox = 0
        hero.update()
        hero.rect.x = herox 
        hero.draw(screen, (0, 0))


        drip.update(hero, None)
        drip.draw(screen, (0, 0))

        pygame.display.update()

        
