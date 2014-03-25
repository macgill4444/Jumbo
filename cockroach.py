import pygame, characters, pyganim

X_SCALE = 180
Y_SCALE = 112

class Cockroach(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                
                # set animation states
                self.__setAnims__()               
 
                try:
                        self.image = pygame.transform.scale(pygame.image.load('sprites/roach_0.png').convert_alpha(), (X_SCALE, Y_SCALE))
                except:
                        self.image = pygame.Surface((X_SCALE, Y_SCALE))
                self.rect = self.image.get_rect().move(x, y)
                self.moveVector = [0, 0]
                self.inAir = True
                self.grounded = False
                self.direction = 1
                self.speed = 3

                self.jumped = False


                #create huge rect to see if player is on same level
                self.rectPlayerCheck = pygame.Rect(x - 400, (y + self.image.get_size()[1]) - 1, (800 + self.image.get_size()[1]), 1) 

                #boolean to check it player is on same platform
                self.playerPlatform = False
                #self.currentXPlatform = None #does not start on a platform
                self.currentYPlatform = None

        def __setAnims__(self): 
                # animation objects
                self.animObjs = {}
                self.animObjs['right-walk'] = pyganim.PygAnimation(
                        [('sprites/roach_0.png', 0.08),
                         ('sprites/roach_1.png', 0.09),
                         ('sprites/roach_2.png', 0.08),
                         ('sprites/roach_3.png', 0.08),
                        ])
                self.animObjs['right-walk'].scale((X_SCALE, Y_SCALE))

                # flip for left-walk
                self.animObjs['left-walk'] = self.animObjs['right-walk'].getCopy()
                self.animObjs['left-walk'].flip(True, False) # (boolx, booly)
                self.animObjs['left-walk'].makeTransformsPermanent()

                self.conductor = pyganim.PygConductor(self.animObjs)

        def update(self, hero, platforms):
                #need to find a way to know if hero is on platform
                self.collide(platforms, hero) #make sure hero is passed here

                #if cockroach is grounded and player is on platform, move to him
                if (self.grounded == True and self.playerPlatform == True):
                    if (self.rect.x < hero.rect.x):
                        self.direction = 1
                        self.rect.x += self.speed
                    if (self.rect.x > hero.rect.x):
                        self.direction = -1
                        self.rect.x -= self.speed
                elif (self.grounded == True and self.currentYPlatform != None):
                #if roach is grounded and player is not on platform, walk around
                    if (self.rect.x < self.currentYPlatform.rect.x):
                        self.direction = 1
                    if ((self.rect.x + self.rect.w) > self.currentYPlatform.rect.x + self.currentYPlatform.rect.w):
                        self.direction = -1
                    self.rect.x += (self.speed * self.direction)
                        
                #this moves cockroach downward 
                if (self.inAir == True):
                        self.rect.y += 4 #make this increasing constant

                #update the other rectangle
                self.rectPlayerCheck = pygame.Rect(self.rect.x - 400, (self.rect.y + self.image.get_size()[1]) - 1, (800 + self.image.get_size()[1]), 1)
                
        def draw(self, screen, world):
              #### not appearing....
                self.conductor.play()
                if self.direction == -1:
                    self.animObjs['right-walk'].blit(screen, self.rect.move(world))
                else:
                    self.animObjs['left-walk'].blit(screen, self.rect.move(world))

        def entityCollide(self, who):
                #if collision between mouse and cockroach, health decre by 5
                if (self.rect.colliderect(who.rect)):
                        who.hit(5, (self.rect.x, self.rect.y))
                        #self.rect.x = self.rect.x + 60
                        
        def collide(self, platforms, hero):
                self.platformCollide(platforms)
                self.HeroOnPlatform(hero)
                #check for player collision
                #swordFrame is greater than 5 than it is being swung

        def HeroOnPlatform(self, hero):
                #if the player collides with this
                if (self.rectPlayerCheck.colliderect(hero.rect)):
                        #the player is on the same platform is this is true
                        self.playerPlatform = True
                else:
                        self.playerPlatform = False
                
                        
        def platformCollide(self, platforms):
                #self.grounded = False
                for platform in platforms:
                        recty = self.rect.move((0, self.moveVector[1]))
                        col = platform.collides(recty)
                        if col is not None:
                            self.currentYPlatform = platform               
                            if (self.rect.y > platform.rect.y):
                                self.rect.y = recty.y + col.height
                                self.moveVector[1] = 0
                            if (self.rect.y < platform.rect.y and self.jumped == False):
                                self.inAir = False
                                self.grounded = True
                                self.rect.y = recty.y - col.height
                                self.moveVector[1] = 0
                        rect = self.rect.move((self.moveVector[0], 0))
                        col = platform.collides(rect)
                        if col is not None:
                                if (self.rect.x < platform.rect.x):
                                        self.rect.x = rect.x - col.width
                                if (self.rect.x > platform.rect.x):
                                        self.rect.x = rect.x + col.width
                                self.moveVector[0] = 0
                if not self.grounded:
                        self.inAir = True



