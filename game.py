import sys, pygame, env, characters, cockroach, spider

pygame.init()
fpsClock = pygame.time.Clock()
size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
global worldX, worldY
worldX = 0
worldY = 0
#env.Hero is the class for the player-controlled character
hero = characters.Hero()
#platforms is a sprite group that contains all platforms
platforms = pygame.sprite.Group()
#dynamics is the sprite group that contains all dynamic elements in the game world, including enemies, mobile objects, and collectibles
dynamics = pygame.sprite.Group()
#background is the current background image

def paint():
        screen.fill(16777215)
        #otherScreen = pygame.Surface((3000, 1000))
        global worldX, worldY
        #prevent the world from scrolling out of screen
        if worldX < 0:
                worldX = 0
        #set the rendering area for the rendering buffer to the area currently
        #visible on screen
        screen.blit(background, pygame.rect.Rect(-worldX, -worldY, width, height))
        #draw sprites
        hero.draw(screen, (-worldX, -worldY))
        for dynamic in dynamics:
                dynamic.draw(screen, (-worldX, -worldY))
        for platform in platforms:
                platform.draw(screen, (-worldX, -worldY))
        # render the game world to the screen
        pygame.display.flip()
def getInput():
        for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
        keys = pygame.key.get_pressed()
        hero.move(keys)
        
def update():
        hero.collide(platforms, dynamics)
        hero.update()
        dynamics.update(hero, platforms)
#camera mechanics:
        global worldX, worldY
        if (hero.rect.x - worldX > width - (width/3)):
                worldX += hero.speed
        if (hero.rect.x - worldX < width/3):
                worldX -= hero.speed
        if (hero.rect.y - worldY < (height/5)):
                worldY -= 5
        if (hero.rect.y - worldY > height - (height / 3)):
                worldY += 5

def loadWorld(file):
        f = open (file)
        global background
        background = pygame.image.load(f.readline().rstrip()).convert()
        dynamics.empty()
        platforms.empty()
        enemies = False
        for line in f:
                if (line[0] == 'E'):
                        enemies = True
                elif line[0] != '#':
                        
                        l = line.split(",")
                        if (enemies):
                                if (l[0].lower() ==  'cockroach'):
                                        dynamics.add(cockroach.Cockroach(int(l[1]), 
                                        int(l[2])))
                                if (l[0].lower() == 'spider'):
                                        dynamics.add(spider.Spider(int(l[1]), int (l[2])))
                        else:
                                coords = []
                        
                                for x in l:
                                        coords.append(int(x))
                                try:
                                        platforms.add(env.Platform(coords[0], 
                                                coords[1],
                                                coords[2], coords[3]))
                                except:
                                        pass


loadWorld('spiderlevel.lvl')

while 1:
        getInput()
        update()
        paint()
        fpsClock.tick(60) 
        



