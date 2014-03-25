import pygame, characters, pyganim, cockroach

class Jumpingroach(cockroach.Cockroach):
    '''a cockroach that jumps if the player is above it'''
    def __init__(self, x, y):
        cockroach.Cockroach.__init__(self, x, y)

        self.jumpingRect = pygame.Rect(x, y + 300, 1, 300)

        self.playerAbove = False
        self.jumped = False
        self.jump = 0

    def update(self, hero, platforms):
        cockroach.Cockroach.update(self, hero, platforms)

        #check to see if hero is above cockroach
        if (self.jumped == False):
            if self.jumpingRect.colliderect(hero.rect):
                #need to jump
                self.jump = 30
                self.jumped = True

        self.rect.y += self.jump

        if self.jump > 0:
            self.jump - 2

        #keep jumping rectangle moving with the roach
        self.jumpingRect.x = self.rect.x
        self.jumpingRect.y = self.rect.y + 300
        