import pygame
import pygame_gui
pygame.init()

import gui
import function_manager

screen = pygame.display.set_mode([800, 450])
pygame.display.set_caption("Multiplayer graftegner")
clock = pygame.time.Clock()
run = True

ui = gui.UiHandler(screen)
functionManager = function_manager.Function_Manager()

while run:
    delta = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False

        # Function has been inputted
        elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == ui.functionInput:
                # Make new function
                if event.text != "":
                    functionManager.make_new_function(event.text)
                
                # Update ui
                ui.functionInput.clear()
                ui.functionInput.focus()
                # Update ui function list
                ui.inputWindow_updateFunctionList(functionManager.get_functions())
        
        ui.handleEvent(event)

    ui.update(delta)

    screen.fill([255, 255, 255])

    ui.draw()

    pygame.display.update()