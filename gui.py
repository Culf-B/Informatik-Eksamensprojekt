import sympy
import pygame
import pygame_gui
pygame.init()

class Graftegner:
    def __init__(self, parentSurface, size):
        self.size = size

        self.parentSurface = parentSurface
        self.renderSurace = pygame.surface.Surface(size)

    def draw(self, offset = [0, 0]):
        self.renderSurace.fill([200, 200, 200])

        self.parentSurface.blit(self.renderSurace, offset)

def _graftegner_test():
    screen = pygame.display.set_mode([800, 450])
    clock = pygame.time.Clock()
    run = True

    graftegner = Graftegner(screen, [200, 200])

    manager = pygame_gui.UIManager([800, 450])

    inputWindow = pygame_gui.elements.ui_window.UIWindow(
        rect = pygame.Rect((0, 0), (300, 400)),
        manager = manager
    )

    functionWindowHeaderLabel = pygame_gui.elements.ui_label.UILabel(
        relative_rect = pygame.Rect((0, 0), (300, 50)),
        text = "Funktions input",
        manager = manager,
        container = inputWindow,
    )

    submitFunctionButton = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
        relative_rect=pygame.Rect((0, 50), (300, 50)),
        manager=manager,
        container = inputWindow,
        placeholder_text = "Input funktion..."
    )

    functionWindowFuncListLabel = pygame_gui.elements.ui_label.UILabel(
        relative_rect = pygame.Rect((0, 100), (300, 50)),
        text = "Funktioner",
        manager = manager,
        container = inputWindow,
    )

    while run:
        delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == submitFunctionButton:
                    print('Hello World!')


            manager.process_events(event)

        manager.update(delta)

        screen.fill([255, 255, 255])

        graftegner.draw()
        manager.draw_ui(screen)

        pygame.display.update()

if __name__ == "__main__":
    _graftegner_test()