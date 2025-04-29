import pygame
import pygame_gui
pygame.init()

import graphTools

class Hiding_UIWindow(pygame_gui.elements.ui_window.UIWindow):
    def on_close_window_button_pressed(self):
        self.hide()
        pygame.event.post(
            pygame.event.Event(
                pygame_gui.UI_WINDOW_CLOSE, {"ui_element": self, "ui_object_id": self.object_ids[0]}
            )
        )

class BetterUIScrollingContainer(pygame_gui.elements.ui_scrolling_container.UIScrollingContainer):
    """
    A version of UIScrollingContainer that ignores some errors in the hide() method.
    """
    def hide(self, hide_contents: bool = True):
        """
        In addition to the base UIElement.hide() - call hide() of owned container - _root_container.
        All other sub-elements (view_container, scrollbars) are children of _root_container, so
        it's visibility will propagate to them - there is no need to call their hide() methods
        separately.

        :param hide_contents: whether to also hide the contents of the container. Defaults to True.
        """
        if not self.visible:
            return
        try:
            self._root_container.hide(hide_contents=False)
            if self.vert_scroll_bar is not None:
                self.vert_scroll_bar.hide()
            if self.horiz_scroll_bar is not None:
                self.horiz_scroll_bar.hide()

            if self._view_container is not None:
                self._view_container.hide(hide_contents)
            super().hide()
        except Exception as e:
            print(f'Error caught when hiding UIScrollingContainer: {e}')

class UiHandler:
    def __init__(self, parentSurface):
        self.parentSurface = parentSurface
        self.renderSurface = pygame.surface.Surface(self.parentSurface.get_size())

        self.graphicsSurface = pygame.surface.Surface(
            [self.parentSurface.get_width(), self.parentSurface.get_height() * 0.9]
        )

        self.graphCam = graphTools.Camera(size = self.graphicsSurface.get_size())

        self.manager = pygame_gui.UIManager(self.parentSurface.get_size())

        self.functionLabels = []

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
            container = self.inputWindow
        )

        self.functionWindowFuncLabelContainer = None
        self.remakeFunctionWindowFuncLabelContainer()
        
    
    def remakeFunctionWindowFuncLabelContainer(self):
        if self.functionWindowFuncLabelContainer != None:
            self.functionWindowFuncLabelContainer.kill()
        self.functionWindowFuncLabelContainer = BetterUIScrollingContainer(
            relative_rect = pygame.Rect((0, 150), (300, 225)),
            manager = self.manager,
            allow_scroll_x = False,
            allow_scroll_y = True,
            visible = True,
            container = self.inputWindow
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
        self.graphCam.update()
        
        if self.inputWindow.visible:
            # Make sure top of window doesn't go out of bounds
            # TODO make sure there is no way to move top bar out of bounds
            if self.inputWindow.get_abs_rect().y <= 0:
                self.inputWindow.set_position((self.inputWindow.get_abs_rect().x, 0))

        self.manager.update(delta)

    def draw(self):
        self.renderSurface.fill([200, 200, 200])
        self.graphicsSurface.fill([200, 200, 200])

        self.graphCam.render(self.graphicsSurface, [0, 0])
        self.renderSurface.blit(self.graphicsSurface, [0, 0])

        self.manager.draw_ui(self.renderSurface)
        self.parentSurface.blit(self.renderSurface, [0, 0])

    def inputWindow_updateFunctionList(self, functionList):
        for element in self.functionLabels:
            element.kill()
        self.functionLabels = []
        self.remakeFunctionWindowFuncLabelContainer()

        for i in range(len(functionList)):
            self.functionLabels.append(
                pygame_gui.elements.ui_label.UILabel(
                    relative_rect = pygame.Rect((0, 50 * i), (300, 50)),
                    text = f'{functionList[i].func_name}({functionList[i].var_name}) = {functionList[i].func}',
                    manager = self.manager,
                    container = self.functionWindowFuncLabelContainer
                )
            )

        self.functionWindowFuncLabelContainer.set_scrollable_area_dimensions((300, 50 * len(functionList)))

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