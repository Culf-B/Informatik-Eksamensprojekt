import pygame
import pygame_gui
pygame.init()

import gui
import Function_Manager

screen = pygame.display.set_mode([800, 450])
pygame.display.set_caption("Multiplayer graftegner")
clock = pygame.time.Clock()
run = True

ui = gui.UiHandler(screen)
functionManager = Function_Manager.Function_Manager()

while run:
    delta = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False

        elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == ui.functionInput:
                functionManager.make_new_function(event.text)
                ui.functionInput.set_text("")
                print("New function made!")
        
        ui.handleEvent(event)

    ui.update(delta)

    screen.fill([255, 255, 255])

    ui.draw()

    pygame.display.update()