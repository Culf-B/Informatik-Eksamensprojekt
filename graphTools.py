import pygame
pygame.init()

class RenderObject:
    def __init__(self):
        pass

    def draw(self, destination, absolutePosition):
        pass

class Grid(RenderObject):
    def __init__(self):
        pass

class Axis(RenderObject):
    def __init__(self):
        pass

class Function(RenderObject):
    def __init__(self):
        pass

class Camera:
    def __init__(self, pos = [0, 0], zoom = 1, size = [500, 500]):
        self.pos = pos
        self.zoom = zoom
        self.size = size
        self.surface = pygame.surface.Surface(self.size)

        self.renderObjects = []

    def render(self, screen, blitpos):
        self.surface.fill([0, 0, 0]) # Clear background

        # Render renderobjects to surface
        for obj in self.renderObjects:
            obj.draw(self.surface, self.pos)

        screen.blit(self.surface, blitpos)

    def update(self):
        pass