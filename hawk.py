import pygame, characters, pyganim, random

class Hawk(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)

                try:
                        self.groundimage = pygame.image.load('sprites/spider_0.png').convert_alpha()
                        self.image = pygame.image.load('sprites/spider_0.png').convert_alpha()
                except:
                        self.groundimage = pygame.Surface((400, 100))
                        self.wallimage = pygame.Surface((400,400))
                        self.groundimage.fill(0)
                        self.wallimage.fill(0)
                self.climbing = False
                self.image = self.groundimage
                self.rect = self.image.get_rect()
                self.speed = 10
                self.state = 0
                self.counter = 250
                self.dy = 15
                self.dx = 3
                pygame.mixer.Sound("sound/hawk.wav").play()
        def update(self, hero, wildcard):
                self.rect.x+=self.dx
                self.rect.y+=self.dy
                self.dy -= 0.5
                self.dx += 1
                if self.rect.x >= 400:
                        hero.rect.x = self.rect.x + 200
                        hero.rect.y = self.rect.y + 200
        def draw(self, screen, world):
                screen.blit(self.image, self.rect)
        def entityCollide(self, something):
                pass
