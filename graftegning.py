# importer graf tegner 
import matplotlib.pyplot as plt
import numpy as np
import pygame 

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("White")
    #tegner linjerne 
    pygame.draw.line(screen, "Black", (0, 360),(1280,360))
    pygame.draw.line(screen, "Black", (640, 0),(640,1200))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
   
    
pygame.quit()