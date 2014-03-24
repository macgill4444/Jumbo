import pygame, characters

class Spider(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)

                try:
                        self.groundimage = pygame.image.load('spiderwall.png').convert_alpha()
                        self.image = pygame.image.load('spider.png').convert_alpha()
                except:
                        self.groundimage = pygame.Surface((400, 100))
                        self.wallimage = pygame.Surface((400,400))
                        self.groundimage.fill(0)
                        self.wallimage.fill(0)
                self.image = self.groundimage
                self.rect = self.image.get_rect().move(x,y)
        def update(self, hero, platforms):
                ray = pygame.rect.Rect(self.rect.center, (1, 55))
                if (len(filter((lambda x: ray.colliderect(x.rect)), platforms)) > 0):
                        pass
                else:
                        self.rect.move_ip(0, 1)
        def draw(self, screen, world):
                screen.blit(self.image, self.rect.move(world).inflate(-5, -5))
        def entityCollide(self, someshit):
                pass

