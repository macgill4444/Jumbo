import sys, pygame, env

pygame.init()
fpsClock = pygame.time.Clock()
size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
worldX = 0
worldY = 0
hero = env.Hero()
platforms = pygame.sprite.Group()
background = pygame.image.load('back.jpg').convert()

def paint():
        screen.fill(16777215)
        otherScreen = pygame.Surface((3000, 1000))
        otherScreen.set_clip( pygame.rect.Rect(worldX, worldY, 1024, 768))
        otherScreen.blit(background, pygame.rect.Rect(0, 0, 1024, 768))
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

        global worldX, worldY
        if (hero.rect.x - worldX > 600):
                worldX += hero.speed
        if (hero.rect.x - worldX < 300):
                worldX -= hero.speed
        if (hero.rect.y - worldY < 200):
                worldY -= 5
        if (hero.rect.y - worldY > 300):
                worldY += 5

def loadWorld(file):
        f = open (file)
        for line in f:
                if line[0] != '#':
                        l = line.split(",")
                        coords = []
                
                        for x in l:
                                coords.append(int(x))
                        try:
                                platforms.add(env.Platform(coords[0], coords[1],
                                        coords[2], coords[3]))
                        except:
                                pass

loadWorld('dewick.lvl')

while 1:
        getInput()
        update()
        paint()
        fpsClock.tick(60) 
        



