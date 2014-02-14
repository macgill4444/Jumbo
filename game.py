import sys,pygame, env

pygame.init()
fpsClock = pygame.time.Clock()
size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
worldX = 0
hero = env.Hero()
platforms = pygame.sprite.Group()
platforms.add(env.Platform(0, 400, 400, 50))
platforms.add(env.Platform(300, 350, 400, 50))
platforms.add(env.Platform(600, 400, 400, 50))
platforms.add(env.Platform(1000, 300, 400, 50))
platforms.add(env.Platform(300, 230, 400, 50))
def paint():
        screen.fill(16777215)
        otherScreen = pygame.Surface((3000, 768))
        otherScreen.set_clip( pygame.rect.Rect(worldX, 0, 1024, 768))
        hero.draw(otherScreen)
        platforms.draw(otherScreen)
        screen.blit(otherScreen, pygame.rect.Rect(0, 0, 1024, 768), 
                otherScreen.get_clip())
        pygame.display.flip()
def getInput():
        for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
        keys = pygame.key.get_pressed()
        hero.move(keys)
        
def update():
        hero.collide(platforms)
        hero.update()

        global worldX
        if (hero.rect.x - worldX > 600):
                worldX += hero.speed
        if (hero.rect.x - worldX < 300):
                worldX -= hero.speed

while 1:
        getInput()
        update()
        paint()
        fpsClock.tick(60) 
        



