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
        super().__init__()

    #tegner linjerne 
    def draw(self, screen, pos_x, pos_y, zoom, size):
        pygame.draw.line(screen, "Black", (size[0] / 2 + pos_x * zoom, 0), (size[0] / 2 + pos_x * zoom, size[1]))
        pygame.draw.line(screen, "Black", (0, size[1] / 2 + pos_y * zoom), (size[0], size[1] / 2 + pos_y * zoom))

class Function(RenderObject):
    def __init__(self,screen):
        super().__init__(screen)

class Camera:
    def __init__(self, pos = [0, 0], zoomAmount = 1, size = [500, 500]):
        self.pos = pos
        self.zoomAmount = zoomAmount
        
        # Calculate actual zoom scaling level
        if self.zoomAmount > 0:
            self.zoom = 1 / abs(self.zoomAmount)
        else:
            self.zoom = abs(self.zoomAmount)

        self.size = size
        self.surface = pygame.surface.Surface(self.size)

        self.renderObjects = []
        self.axis = Axis()
        self.renderObjects.append(self.axis)

        self.collisionRect = pygame.Rect([0, 0, self.size[0], self.size[1]])

    def render(self, screen, blitpos):
        self.surface.fill([255, 255, 255]) # Clear background

        # Render renderobjects to surface
        for obj in self.renderObjects:
            obj.draw(self.surface, self.pos[0], self.pos[1], self.zoom, self.size)

        screen.blit(self.surface, blitpos)

        # Update collisionRect with blitpos
        self.collisionRect = pygame.Rect([blitpos[0], blitpos[1], self.size[0], self.size[1]])

    def update(self):
        self.pressed = pygame.key.get_pressed()
        if self.pressed[pygame.K_w]:
            self.pos[1] += 1
        if self.pressed[pygame.K_s]:
            self.pos[1] -= 1  

        if self.pressed[pygame.K_a]:
            self.pos[0] += 1
        if self.pressed[pygame.K_d]:
            self.pos[0] -= 1
    
    def handleEvent(self, event):
        if event.type == pygame.MOUSEWHEEL:
            # Check if mouse is on camera surface (last known blitpos)
            self.mousePos = pygame.mouse.get_pos()
            if self.collisionRect.collidepoint(self.mousePos):
                self.beforePos = self.getPosFromScreenCoords(self.mousePos)

                # Apply zoom without getting zoomAmount = 0
                if self.zoomAmount != event.y:
                    self.zoomAmount -= event.y
                else:
                    self.zoomAmount -= 2 * event.y

                # Calculate actual zoom scaling level
                if self.zoomAmount > 0:
                    self.zoom = 1 / abs(self.zoomAmount)
                else:
                    self.zoom = abs(self.zoomAmount)

                self.afterPos = self.getPosFromScreenCoords(self.mousePos)

                self.pos[0] += self.afterPos[0] - self.beforePos[0]
                self.pos[1] += self.afterPos[1] - self.beforePos[1]

    def getPosFromScreenCoords(self, screenPos):
        return [(p - self.size[i] / 2) / self.zoom + self.pos[i] for i, p in enumerate(screenPos)] # Funky math to convert position on screen to position on graph
    
if __name__ == '__main__': 
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    cam = Camera()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("White")

        cam.update()
        cam.render(screen, [0, 0])

        pygame.display.flip()

        clock.tick(60)