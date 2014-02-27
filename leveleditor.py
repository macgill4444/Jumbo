import pygame, sys

pygame.init()
background = pygame.image.load(sys.argv[1])
screen = pygame.display.set_mode((1024, 768))
platforms = []
while 1:
        clicks = pygame.mouse.get_pressed()
        cursor = pygame.mouse.get_cursor()

        for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
        
        screen.blit(background, background.get_rect())
        pygame.display.flip()
