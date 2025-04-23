import pygame
import pygame_gui
pygame.init()

class Hiding_UIWindow(pygame_gui.elements.ui_window.UIWindow):
    def on_close_window_button_pressed(self):
        self.hide()
        pygame.event.post(
            pygame.event.Event(
                pygame_gui.UI_WINDOW_CLOSE, {"ui_element": self, "ui_object_id": self.object_ids[0]}
            )
        )

class UiHandler:
    def __init__(self, parentSurface):
        self.parentSurface = parentSurface
        self.renderSurface = pygame.surface.Surface(self.parentSurface.get_size())

        self.graphicsSurface = pygame.surface.Surface(
            [self.parentSurface.get_width(), self.parentSurface.get_height() * 0.9]
        )


        self.manager = pygame_gui.UIManager(self.parentSurface.get_size())

        # Button to show inputwindow
        self.showInputWindowButton = pygame_gui.elements.ui_button.UIButton(
            relative_rect = pygame.Rect(
                (0, self.graphicsSurface.get_height()),
                (self.renderSurface.get_width() * 0.2, self.renderSurface.get_height() * 0.1)
            ),
            text = "Vis funktions vindue"
        )

        # --- Inputwindow ---

        self.inputWindow = Hiding_UIWindow(
            rect = pygame.Rect((0, 0), (300, 400)),
            manager = self.manager,
            visible = False
        )
        

        self.functionWindowHeaderLabel = pygame_gui.elements.ui_label.UILabel(
            relative_rect = pygame.Rect((0, 0), (300, 50)),
            text = "Funktions input",
            manager = self.manager,
            container = self.inputWindow,
        )

        self.functionInput = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect = pygame.Rect((0, 50), (300, 50)),
            manager = self.manager,
            container = self.inputWindow,
            placeholder_text = "Input funktion..."
        )

        self.functionWindowFuncListLabel = pygame_gui.elements.ui_label.UILabel(
            relative_rect = pygame.Rect((0, 100), (300, 50)),
            text = "Funktioner",
            manager = self.manager,
            container = self.inputWindow,
        )
    
    def handleEvent(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.showInputWindowButton:
                if self.inputWindow.visible:
                    self.inputWindow.hide()
                    self.showInputWindowButton.set_text("Vis funktions vindue")
                else:
                    self.inputWindow.show()
                    self.showInputWindowButton.set_text("Skjul funktions vindue")
        elif event.type == pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_element == self.inputWindow:
                self.showInputWindowButton.set_text("Vis funktions vindue")

        self.manager.process_events(event)

    def update(self, delta):
        if self.inputWindow.visible:
            # Make sure top of window doesn't go out of bounds
            # TODO make sure there is no way to move top bar out of bounds
            if self.inputWindow.get_abs_rect().y <= 0:
                self.inputWindow.set_position((self.inputWindow.get_abs_rect().x, 0))

        self.manager.update(delta)

    def draw(self):
        self.renderSurface.fill([255, 255, 255])
        self.graphicsSurface.fill([200, 200, 200])

        self.renderSurface.blit(self.graphicsSurface, [0, 0])

        self.manager.draw_ui(self.renderSurface)

        self.parentSurface.blit(self.renderSurface, [0, 0])

def _GUI_test():
    screen = pygame.display.set_mode([800, 450])
    pygame.display.set_caption("GUI test")
    clock = pygame.time.Clock()
    run = True

    ui = UiHandler(screen)

    while run:
        delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False

            ui.handleEvent(event)

        ui.update(delta)

        screen.fill([255, 255, 255])

        ui.draw()

        pygame.display.update()

if __name__ == "__main__":
    _GUI_test()