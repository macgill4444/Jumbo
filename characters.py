import pygame, cockroach

#make separate cockroach class, decrement health for hero collision, make cockroach pace platform while hero no on platform

class Hero(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load('mouse.png').convert()
                self.swordImage = pygame.Surface((70, 10))
                self.swordRect = self.swordImage.get_rect()
                self.health = 5
# set the color key to blue
                blue    = (0,   0,   255)
                self.orientation = 1
                self.image.set_colorkey(blue)
                self.image = pygame.transform.scale(self.image, (150, 80))
                self.rect = self.image.get_rect()
                self.moveVector = [0, 0]
                self.inAir = True
                self.canJump = True
# sword indicates whether the mouse is in sword stance or not
# swordframe indicates the current position in the sword animation
                self.sword = False
                self.swordFrame = 0
                self.speed = 7
        def move(self, keys):
                if (keys[pygame.K_d]):
                        if not self.inAir:
                                self.moveVector[0] += 1
                                self.orientation  = 1
                        else:
                                self.moveVector[0] += 0.125
                elif (keys[pygame.K_a]):
                        if not self.inAir:
                                self.orientation = -1
                                self.moveVector[0] -= 1
                        else:
                                self.moveVector[0] -= 0.125
                        
                else:
                        if not self.inAir:
                                if (self.moveVector[0] < -0.5):
                                        self.moveVector[0] += 1
                                elif self.moveVector[0] > 0.5:
                                        self.moveVector[0] -= 1
                                else:
                                        self.moveVector[0] = 0
                if (keys[pygame.K_k]):
                        self.sword = not self.sword
                if (not self.sword):
                        if (keys[pygame.K_j] and not self.inAir):
                                if (self.canJump):
                                        self.moveVector[1] = -15
                                self.canJump = False
                        if not keys[pygame.K_j] and not self.inAir:
                                self.canJump = True
                else:
                        if (keys[pygame.K_j]) and self.swordFrame < 4:
                                self.swordFrame = 22

                self.moveVector[1] += 1
                if (self.moveVector[0] > self.speed):
                        self.moveVector[0] = self.speed
                if (self.moveVector[0] < -self.speed):
                        self.moveVector[0] = -self.speed

        def update(self):
                self.rect.x += self.moveVector[0]
                self.rect.y += self.moveVector[1]

                self.swordFrame -= 1
                if self.swordFrame < 0:
                        self.swordFrame = 0
                if self.sword:
                        self.swordRect.x = self.rect.x + (self.swordFrame * 2 + 30)
                        self.swordRect.y = self.rect.y + 30
                        self.speed = 4
                else:
                        self.swordRect.x = -100
                        self.speed = 7
                        
        def draw(self, screen,world):
                if (self.orientation == -1):
                        screen.blit(pygame.transform.flip(
                                self.image, True, False), 
                                        self.rect.move(world))
                else:
                        screen.blit(self.image, self.rect.move(world))
                if self.sword:
                        screen.blit(self.swordImage, self.swordRect.move(world))
# handle collision detection and position updates
# as new collidable objects are added, more arguments will be added to collide
        def collide(self, platforms, dynamics):
                self.platformCollide(platforms)
                self.dynamicCollide(dynamics)
        def dynamicCollide(self, dynamics):
                for dynamic in dynamics:
                        if (self.rect.colliderect(dynamic.rect)):
                                dynamic.entityCollide(self)
        def platformCollide(self, platforms):
                grounded = False
                for platform in platforms:
                        rect = self.rect.move((0, self.moveVector[1]))
                        col = platform.collides(rect) 
                        if col is not None:
                                if (self.rect.y > platform.rect.y):
                                        self.rect.y = rect.y + col.height
                                        self.moveVector[1] = 0

                                if (self.rect.y < platform.rect.y):
                                        self.inAir = False
                                        grounded = True
                                        self.rect.y = rect.y - col.height
                                        self.moveVector[1] = 0
                        rect = self.rect.move((self.moveVector[0], 0))
                        col = platform.collides(rect)
                        if col is not None:
                                if (self.rect.x < platform.rect.x):
                                        self.rect.x = rect.x - col.width
                                if (self.rect.x > platform.rect.x):
                                        self.rect.x = rect.x + col.width
                                self.moveVector[0] = 0

