import sys,pygame, env

pygame.init()
fpsClock = pygame.time.Clock()
size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
hero = env.Hero()
platforms = pygame.sprite.Group()
platforms.add(env.Platform(0, 400, 400, 50))
platforms.add(env.Platform(300, 350, 400, 50))
def paint():
        screen.fill([0, 0, 0])
        hero.draw(screen)
        platforms.draw(screen)
        pygame.display.flip()
def getInput():
        for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
        keys = pygame.key.get_pressed()
        hero.move(keys)
def update():
        hero.collide(platforms)
        hero.update()

while 1:
        getInput()
        update()
        paint()
        fpsClock.tick(60) 
        



