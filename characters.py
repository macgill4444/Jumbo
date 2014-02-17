import pygame

class Hero(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load('mouse.png').convert()
                blue    = (   0,   0,   255)
                self.image.set_colorkey(blue)
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.rect = pygame.rect.Rect(100, 100, 50, 50)
                self.moveVector = [0, 0]
                self.inAir = True
                self.canJump = True
                self.speed = 7
        def move(self, keys):
                if (keys[pygame.K_d]):
                        if not self.inAir:
                                self.moveVector[0] += 1
                        else:
                                self.moveVector[0] += 0.125
                elif (keys[pygame.K_a]):
                        if not self.inAir:
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
                if (keys[pygame.K_j] and not self.inAir):
                        if (self.canJump):
                                self.moveVector[1] = -15
                        self.canJump = False
                if not keys[pygame.K_j] and not self.inAir:
                        self.canJump = True
                self.moveVector[1] += 1
                if (self.moveVector[0] > self.speed):
                        self.moveVector[0] = self.speed
                if (self.moveVector[0] < -self.speed):
                        self.moveVector[0] = -self.speed

        def update(self):
                self.rect.x += self.moveVector[0]
                self.rect.y += self.moveVector[1]
        def draw(self, screen,world):
                screen.blit(self.image, self.rect.move(world))
# handle collision detection and position updates
# as new collidable objects are added, more arguments will be added to collide
        def collide(self, platforms):
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
                if not grounded:
                        self.inAir = True

