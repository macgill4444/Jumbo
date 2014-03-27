import pygame, characters, pyganim, random

class Hawk(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)

                try:
                        self.image = pygame.image.load('sprites/hawk.png').convert_alpha()
                except:
                        pass
                self.climbing = False
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
                        hero.rect.x = self.rect.x + 300
                        hero.rect.y = self.rect.y + 300
        def draw(self, screen, world):
                screen.blit(self.image, self.rect)
        def entityCollide(self, something):
                pass
