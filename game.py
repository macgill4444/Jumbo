import sys, pygame, env, characters, cockroach, spider

pygame.init()
fpsClock = pygame.time.Clock()
size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
global worldX, worldY
worldX = 0
worldY = 0
global end
global curlevel
end = (0, 0, "")
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
        #render health bar:
        pygame.draw.rect(screen, 0, pygame.rect.Rect(40, 40, 40, 100))
        pygame.draw.rect(screen, (0, 255, 0), pygame.rect.Rect(45, 140 - hero.health, 30, hero.health))
        # render the game world to the screen
        pygame.display.flip()
def getInput():
        for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
        keys = pygame.key.get_pressed()
        hero.move(keys)
        
def update():
        global end
        endx, endy, endname = end

        if (hero.rect.collidepoint(endx, endy)):
                loadWorld(endname.strip())
        if (hero.health < 0):
                global curlevel
                hero.health = 100
                loadWorld(curlevel)
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
        global curlevel
        curlevel = file
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
                                if (l[0].lower() == 'spawn'):
                                        hero.rect.x = int(l[1])
                                        hero.rect.y = int(l[2])
                                if (l[0].lower() == 'end'):
                                        global end
                                        end = (int(l[1]), int (l[2]), l[3])
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
        global worldX, worldY
        worldX = hero.rect.x - 500
        worldY = hero.rect.y - 400

loadWorld('spiderlevel.lvl')
while 1:
        getInput()
        update()
        paint()
        fpsClock.tick(60) 
        



