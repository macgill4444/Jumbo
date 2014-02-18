import pygame

#platform is a static box that inhibits movement in the environment
                        
class Platform(pygame.sprite.Sprite):
# x, y are the top left corner, w, h are the width and height
        def __init__(self, x, y, w, h):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.surface.Surface((w, h))
                self.image.fill(16777215)
                self.rect = pygame.rect.Rect(x, y, w, h)
        def update(self):
                pass
# returns the rectangle that is the intersection between rect and the platform,
# none if the rectangles do not collide
        def collides(self, rect):
                if (rect.colliderect(self.rect)):
                        return rect.clip(self.rect)
                return None
#parameter world is a vector containing the offset from 0, 0 that the world has 
               # scrolled
        def draw(self, screen, world):
                global worldX, worldY
                screen.blit(self.image, self.rect.move(world))
