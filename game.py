import sys, pygame, env, characters, cockroach, spider, toxicdrip, jumpingroach, web, dieroach, pyganim, hawk
from pygame.locals import *

pygame.init()
pygame.joystick.init()
pygame.mixer.init()
joystick = None
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
if (len(joysticks)>0):
        joysticks[0].init()
        joystick = joysticks[0]
        print "Joystick"
fpsClock = pygame.time.Clock()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
global worldX, worldY, camX, camY
worldX = 0
worldY = 0
camX = 0
camY = 0
offX = 0
offY = 0
global end
global curlevel
global cutscene
cutscene = -1
end = (1000000000, 1000000000000, "")
#env.Hero is the class for the player-controlled character
hero = characters.Hero()
#platforms is a sprite group that contains all platforms
platforms = pygame.sprite.Group()
#dynamics is the sprite group that contains all dynamic elements in the game world, including enemies, mobile objects, and collectibles
dynamics = pygame.sprite.Group()
#background is the current background image
chiptunes = {'spiderlevel.lvl':'chiptunes/boss.wav', 
            'softserve.lvl':'chiptunes/level2.wav',
            'dewicklvl.lvl':'chiptunes/level3.wav',  
            'tutorial.lvl': 'chiptunes/level.wav'}

def paint():
        screen.fill(16777215)
        #otherScreen = pygame.Surface((3000, 1000))
        global worldX, worldY, camX, camY
	ox = worldX
	oy = worldY
	worldX += camX
	worldY += camY
        #prevent the world from scrolling out of screen
        if worldX < 0:
                worldX = 0
        #set the rendering area for the rendering buffer to the area currently
        #visible on screen
        screen.blit(background, pygame.rect.Rect(-worldX, -worldY, width, height))
        #draw sprites
        for dynamic in dynamics:
                dynamic.draw(screen, (-worldX, -worldY))
        #render health bar:
        hero.draw(screen, (-worldX, -worldY))
        global endSprite, end
        (ex, ey, st ) = end
        screen.blit(endSprite, (ex-worldX, ey-worldY))
        pygame.draw.rect(screen, 0, pygame.rect.Rect(40, 40, 40, 100))
        pygame.draw.rect(screen, (0, 255, 0), pygame.rect.Rect(45, 140 - hero.health, 30, hero.health))
        # render the game world to the screen
        pygame.display.flip()
        worldX = ox
	worldY = oy

def getInput():
        for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
        keys = pygame.key.get_pressed()
        global cutscene
        if cutscene < 0:
                hero.move(keys, joystick)
        else:
                hero.moveVector=[0, 0]
	global camX, camY
	if (joystick):
		if (joystick.get_axis(1) > 0.5):
			camY +=10
		elif (joystick.get_axis(1) < -0.5):
			camY -= 10
		else:
			if camY > 103:
                                camY -= 15
                        if camY < 97:
                                camY += 15
        else:
                if (keys[pygame.K_w]):
                        camY -= 10
                elif(keys[pygame.K_s]):
                        camY += 10
                else:
                        if camY > 103:
                                camY -= 15
                        if camY < 97:
                                camY += 15
	if camY > 400:
		camY = 400
	if camY < -200:
		camY = -200
def update():
        global end
        endx, endy, endname = end
        global cutscene
        if cutscene >= 0:
                cutscene -= 1
        if (hero.rect.collidepoint(endx, endy)):
                loadWorld(endname.strip())
        if (hero.health < 0):
                global curlevel
                hero.health = 100
                loadWorld(curlevel)
        hero.collide(platforms, dynamics)
        hero.update(dynamics)
        dynamics.update(hero, platforms)
#camera mechanics:
        if cutscene < 0:
                global worldX, worldY
                if (hero.rect.x - worldX > width - (width/3)-(200) - (200 * hero.orientation)):
                        worldX += hero.speed
                if (hero.rect.x - worldX < width/3 - 200 * hero.orientation):
                        worldX -= hero.speed 
                if (hero.rect.y - worldY < (height/5)):
                        worldY -= 15
                if (hero.rect.y - worldY > height - (height / 3)):
                        worldY += 15
	

def loadWorld(file):
        global curlevel
        curlevel = file
        f = open (file)
        global background
        background = pygame.image.load(f.readline().rstrip()).convert()
        dynamics.empty()
        platforms.empty()
        global chiptunes
        try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(chiptunes[file])
                pygame.mixer.music.play(-1)
        except:
                pass
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
                                        global endSprite
                                        endSprite = pygame.image.load("sprites/arrow.png").convert_alpha()
                                if (l[0].lower() == 'drip'):
                                        dynamics.add(toxicdrip.Toxicdrip(int (l[1]), int(l[2]), int(l[3]), int(l[4])))
                                if(l[0].lower() == 'jumpingroach'):
                                        dynamics.add(jumpingroach.Jumpingroach( int (l[1]), int(l[2])))
                                if(l[0].lower() == 'web'):
                                        dynamics.add(web.Spiderweb(int (l[1]), int(l[2])))
                                if(l[0].lower() == 'dieroach'):
                                        dynamics.add(dieroach.Dieroach(int(l[1]), int(l[2])))
                                if(l[0].lower() == 'hawk'):
                                        print "hawk"
                                        dynamics.add(hawk.Hawk())
                                if(l[0].lower() == 'cutscene'):
                                        global cutscene
                                        cutscene = int(l[1])
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

# menu screen
try:
        menu = pyganim.PygAnimation(
                        [('sprites/menu0.png', 0.15),
                         ('sprites/menu1.png', 0.15),
                         ('sprites/menu2.png', 0.15),
                         ('sprites/menu3.png', 0.15),
                         ('sprites/menu2.png', 0.15),
                         ('sprites/menu1.png', 0.15),
                        ])
except:
        menu = pygame.image.load("assets/menu.png").convert()
try:
        intro_music = pygame.mixer.music.load("chiptunes/menu.wav")
except:
        print "Cannot get menu music"

pygame.mixer.music.play(-1)
intro = True
menu.play()
menu.blit(screen, (0,0))
pygame.display.flip()

# menu
while intro:
        screen.fill(16777215)
        for event in pygame.event.get():
                if event.type == KEYDOWN:
                        intro = False
                        pygame.mixer.music.stop()
                        menu.stop()
                elif event.type == pygame.QUIT: sys.exit()
                
        menu.play()
        menu.blit(screen, (0,0))
        pygame.display.update()

# intro cutscene
scene = True
background = pygame.image.load('sprites/intro-image.jpg')
backgroundpos = [0,-50]


pygame.mixer.music.load("chiptunes/intro.wav")
pygame.mixer.music.play(-1)
while scene:
        screen.fill(16777215)
        print backgroundpos
        screen.blit(background, backgroundpos)
        if backgroundpos[0] > -620:
            backgroundpos[0] -= 1.3
            backgroundpos[1] -= 0.5
        elif backgroundpos[0] > -900:
            backgroundpos[0] -= 0.9
        else:
            pass

        pygame.display.update()
        pygame.display.flip()
        for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                elif event.type == KEYDOWN:
                    scene = False
                    pygame.mixer.music.stop()
        fpsClock.tick(60)

loadWorld('tutorial.lvl')



while 1:
        getInput()
        update()
        paint()
        fpsClock.tick(60) 
        



