import sys,pygame, env

pygame.init()
fpsClock = pygame.time.Clock()
size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
worldX = 0
worldY = 0
#env.Hero is the class for the player-controlled character
hero = env.Hero()
#platforms is a sprite group that contains all static platforms
platforms = pygame.sprite.Group()
#background is the current background image
background = pygame.image.load('back.jpg').convert()

def paint():
        screen.fill(16777215)
        otherScreen = pygame.Surface((3000, 1000))
        global worldX
        #prevent the world from scrolling out of screen
        if worldX < 0:
                worldX = 0
        #set the rendering area for the rendering buffer to the area currently
        #visible on screen
        otherScreen.set_clip( pygame.rect.Rect(worldX, (worldY) , 1024, 768))
        otherScreen.blit(background, pygame.rect.Rect(0, 0, 1024, 768))
        #draw sprites
        hero.draw(otherScreen)
        platforms.draw(otherScreen)
        # render the game world to the screen
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
        if (hero.rect.y - worldY > 600):
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

loadWorld('miller.lvl')

while 1:
        getInput()
        update()
        paint()
        fpsClock.tick(60) 
        



