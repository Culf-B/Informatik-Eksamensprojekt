# importer graf tegner 
import matplotlib.pyplot as plt
import numpy as np
import pygame 

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
pos_y = 0
pos_x = 0
while running:
 # poll for events
 # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
#Bevæger grafen op og ned samt højre og venstre det gøres med wasd
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        print("w is pressed")
        pos_y += 1
    if pressed[pygame.K_s]:
        print("s is pressed")
        pos_y -= 1  

    if pressed[pygame.K_a]:
        print("a is pressed")
        pos_x += 1
    if pressed[pygame.K_d]:
        print("d is pressed")
        pos_x -= 1  
        

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("White")
    #tegner linjerne 
    pygame.draw.line(screen, "Black", (0, 360 + pos_y),(1280,360 + pos_y))
    pygame.draw.line(screen, "Black", (640 + pos_x, 0),(640 + pos_x,1200))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60


    
pygame.quit()