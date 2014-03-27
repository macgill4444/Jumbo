import pygame, characters, pyganim, random

class Spider(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.__setAnims__() 

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
                self.rect = self.image.get_rect().move(x,y)
                self.speed = 18
                self.sound = pygame.mixer.Sound("sound/skitter.wav")
                self.drop = pygame.mixer.Sound("sound/spider_drop.wav")
                self.state = 0
                self.counter = 1000
        def __setAnims__(self):
                self.animObjs = {}
                self.animObjs['climb'] = pyganim.PygAnimation(
                        [('sprites/climb_0.png', 0.08),
                         ('sprites/climb_1.png', 0.09),
                         ('sprites/climb_0.png', 0.08),
                         ('sprites/climb_-1.png', 0.08),
                        ])
                self.animObjs['left'] = pyganim.PygAnimation(
                        [('sprites/spider_0.png', 0.08),
                         ('sprites/spider_1.png', 0.09),
                         ('sprites/spider_0.png', 0.08),
                         ('sprites/spider_-1.png', 0.08),
                        ])
                self.animObjs['right'] = self.animObjs['left'].getCopy()
                self.animObjs['right'].flip(True, False) # (boolx, booly)
                self.animObjs['right'].makeTransformsPermanent()

                self.conductor = pyganim.PygConductor(self.animObjs)
        def cutsceneupdate(self, hero, platforms):
                self.counter -= 1
                if self.counter < 0:
                        self.state= 1
                        self.climbing = False
        def update(self, hero, platforms):
                if self.state == 1:
                        self.normalupdate(hero, platforms)
                if self.state == 0:
                        self.cutsceneupdate(hero, platforms)
        def normalupdate(self, hero, platforms):
                if (self.climbing):
                        if (hero.rect.x > self.rect.x):
                                self.rect.move_ip(self.speed, 0)
                        else:
                                self.rect.move_ip(-self.speed, 0)
                        ray = pygame.rect.Rect(self.rect.center, (1, 200)).move(0, -200)
                        if (len(filter((lambda x: ray.colliderect(x.rect)), platforms)) > 0 and self.rect.y < hero.rect.y):
                                self.climbing = False
                                if random.random() * 5 > 2:
                                        self.drop.play()
                                self.image = self.groundimage
                                self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)
                        else:
                                self.rect.move_ip(0, -4)
                else:
                        ray = pygame.rect.Rect(self.rect.center, (1, 55))
                        if (ray.colliderect(hero.rect)):
                                hero.hit(101, self)
                        if (len(filter((lambda x: ray.colliderect(x.rect)), platforms)) > 0):
                                self.climbing = True
                                #self.image = self.wallimage
                                self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)
                                self.rect.move_ip(0, -200)
                        else:
                                self.rect.move_ip(0, 10)
                
        def draw(self, screen, world):
                
                if self.climbing:
                        self.conductor.play()
                        self.animObjs['climb'].blit(screen, self.rect.move(world))
                else:
                        self.conductor.play()
                        self.animObjs['left'].blit(screen, self.rect.move(world))
                        #screen.blit(self.groundimage, self.rect.move(world).inflate(-5, -5))

        def entityCollide(self, someshit):
                pass

