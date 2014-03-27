import pygame, characters, pyganim, cockroach

class Dieroach(cockroach.Cockroach):
    def __init__(self, x, y):
        cockroach.Cockroach.__init__(self,x, y)

        self.left_pix = 200
        self.right_pix = 900
        #make the player check rect really small
        self.rectPlayerCheck = pygame.Rect(0,0, 1, 1)

    def update(self, hero, platforms):
      

        if self.left_pix > 0:
            self.direction = -1
        else:
            self.direction = 1
        self.rectPlayerCheck = pygame.Rect(0,0, 1, 1)

        cockroach.Cockroach.update(self, hero, platforms)

        #set the player not to be on platform becuase we don't care about him
        self.playerPlatform = False

        if self.left_pix > 0 and self.inAir == False:
            self.left_pix -= self.speed
        elif self.inAir == False:
            self.right_pix -= self.speed

        #once the roach walks 900 pixels to the right, it dies
        if self.right_pix < 0:
            print "we going kill this"
            self.kill()
        
