import pygame, cockroach
import pyganim

#make separate cockroach class, decrement health for hero collision, make cockroach pace platform while hero no on platform

class Hero(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                # set animation states
                self.__setAnims__()

             

                # sword/health
                self.swordImage = pygame.Surface((70, 10))
                self.swordRect = self.swordImage.get_rect()
                self.health = 5

                self.orientation = 1
                self.rect = self.right_standing.get_rect()
                self.moveVector = [0, 0]
                self.inAir = True
                self.canJump = True

                # sword indicates whether the mouse is in sword stance or not
                # swordframe indicates the current position in the sword animation
                self.sword = False
                self.swordFrame = 0
                self.speed = 9

        def __setAnims__(self):
                '''initializes animation/static sprites'''

                # static sprites
                self.right_standing = pygame.image.load('sprites/stand.png')
                self.right_standing = pygame.transform.scale(self.right_standing, (300, 150))
                self.left_standing = pygame.transform.flip(self.right_standing, True, False)
                self.right_jump = pygame.image.load('sprites/run_2.png')
                self.right_jump = pygame.transform.scale(self.right_jump, (300, 150))
                self.left_jump = pygame.transform.flip(self.right_jump, True, False)

                # animation objects
                self.animObjs = {}
                self.animObjs['right-walk'] = pyganim.PygAnimation(
                        [('sprites/run_0.png', 0.08),
                         ('sprites/run_1.png', 0.09),
                         ('sprites/run_2.png', 0.08),
                         ('sprites/run_3.png', 0.08),
                         ('sprites/run_4.png', 0.07),
                         ('sprites/run_5.png', 0.05),
                         ('sprites/run_6.png', 0.05),
                         ('sprites/run_7.png', 0.05)
                        ])
                self.animObjs['right-walk'].scale((300, 150))

                # flip for left-walk
                self.animObjs['left-walk'] = self.animObjs['right-walk'].getCopy()
                self.animObjs['left-walk'].flip(True, False) # (boolx, booly)
                self.animObjs['left-walk'].makeTransformsPermanent()

                # animation 'conductor'
                self.conductor = pyganim.PygConductor(self.animObjs)


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
                        
        def draw(self, screen, world):
                # right orientation
                if self.orientation == 1:
                        if self.moveVector[0] == 0 and not self.inAir:    # standing still
                                self.conductor.stop()
                                screen.blit(self.right_standing, self.rect.move(world))
                        elif self.inAir:   # in air
                                self.conductor.stop()
                                screen.blit(self.right_jump, self.rect.move(world))
                        else:   # x axis motion
                                self.conductor.play()
                                self.animObjs['right-walk'].blit(screen, self.rect.move(world))

                # left orientation
                elif (self.orientation == -1):
                        if self.moveVector[0] == 0 and not self.inAir:    # standing still
                                self.conductor.stop()
                                screen.blit(self.left_standing, self.rect.move(world))
                        elif self.inAir:   # in air
                                self.conductor.stop()
                                screen.blit(self.left_jump, self.rect.move(world))
                        else:   # x axis motion
                                self.conductor.play()
                                self.animObjs['left-walk'].blit(screen, self.rect.move(world))

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
                if not grounded:
                        self.inAir = True
