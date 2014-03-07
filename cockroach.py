import pygame, characters

class Cockroach(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                
                try:
                        self.image = pygame.image.load('cockroach.png').convert_alpha()
			self.image
                except:
                        self.image = pygame.Surface((100, 63))
                self.rect = self.image.get_rect().move(x, y)
                self.moveVector = [0, 0]
                self.inAir = True
                self.grounded = False
                self.direction = 1


                #create huge rect to see if player is on same level
                self.rectPlayerCheck = pygame.Rect(x - 400, (y + self.image.get_size()[1]) - 1, (800 + self.image.get_size()[1]), 1) 

                #boolean to check it player is on same platform
                self.playerPlatform = False
                #self.currentXPlatform = None #does not start on a platform
                self.currentYPlatform = None

        def update(self, hero, platforms):
                #need to find a way to know if hero is on platform
                self.collide(platforms, hero) #make sure hero is passed here

                #if cockroach is grounded and player is on platform, move to him
                if (self.grounded == True and self.playerPlatform == True):
                    if (self.rect.x < hero.rect.x):
                        self.direction = 1
                        self.rect.x += 5
                    if (self.rect.x > hero.rect.x):
                        self.direction = -1
                        self.rect.x -= 5
                elif (self.grounded == True and self.currentYPlatform != None):
                #if roach is grounded and player is not on platform, walk around
                    if (self.rect.x < self.currentYPlatform.rect.x):
                        self.direction = 1
                    if ((self.rect.x + self.rect.w) > self.currentYPlatform.rect.x + self.currentYPlatform.rect.w):
                        self.direction = -1
                    self.rect.x += (5 * self.direction)
                        
                #this moves cockroach downward 
                if (self.inAir == True):
                        self.rect.y += 4 #make this increasing constant

                #update the other rectangle
                self.rectPlayerCheck = pygame.Rect(self.rect.x - 400, (self.rect.y + self.image.get_size()[1]) - 1, (800 + self.image.get_size()[1]), 1)
                
        def draw(self, screen, world):
                screen.blit(self.image, self.rect.move(world))

        def entityCollide(self, who):
                #if collision between mouse and cockroach, health decre by 5
                if (self.rect.colliderect(who.rect)):
                        who.health -= 5
                        self.rect.x = self.rect.x + 60
                        
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
                            if (self.rect.y < platform.rect.y):
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



