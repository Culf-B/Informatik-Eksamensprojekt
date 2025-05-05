import pygame
import pygame_gui
pygame.init()
import json

import gui
import function_manager
from networking import client

screen = pygame.display.set_mode([800, 450])
pygame.display.set_caption("Multiplayer graftegner")
clock = pygame.time.Clock()
run = True

ui = gui.UiHandler(screen)
functionManager = function_manager.Function_Manager()
isFunctionlistUpdated = True

def functionListUpdated():
    # Update ui
    ui.functionInput.clear()
    ui.functionInput.focus()
    # Update ui function list
    ui.inputWindow_updateFunctionList(functionManager.get_functions())

def updateCallback(data):
    global isFunctionlistUpdated
    try:
        print(f'Data received: {data}')
        objectifiedData = json.loads(data)
        print("test 1")
        if objectifiedData["status"] == 200:
            print("test 2")
            functionManager.delete_all_functions()
            print("test 3")
            for functionString in objectifiedData["content"]:
                print("test 4", functionString)
                functionManager.choose_action(functionString)

        isFunctionlistUpdated = True
        
    except Exception as e:
        print(f'Error when parsing received data: {e}')

# Connect to server and get all functions
connectionClient = client.Client(
    input("Server IP (leave blank for any local ip): "),
    int(input("Server address: ")),
    updateCallback
)
connectionClient.connect()

# Load functions from the server
connectionClient.request(
    json.dumps(
        {
            "action": "GET"
        }
    )
)

functionListUpdated()

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
                    functionManager.choose_action(event.text)
                
                # Update ui
                functionListUpdated()
                
                # Send to server
                connectionClient.request(
                    json.dumps(
                        {
                            "action": "POST",
                            "content": event.text
                        }
                    )
                )

        # Pass events onto UIHandlers eventhandler
        ui.handleEvent(event)

    if isFunctionlistUpdated:
        print("Updating ui", functionManager.get_function_strings())
        isFunctionlistUpdated = False
        functionListUpdated()

    ui.update(delta)

    screen.fill([255, 255, 255])

    ui.draw()

    pygame.display.update()
    clock.tick(60)

# Disconnect from server when closing program
connectionClient.disconnect()