import pygame
pygame.init()

class RenderObject:
    def __init__(self):
        pass
        
    def draw(self, screen, pos_x, pos_y, zoom, size, camera):
        pass

class Grid(RenderObject):
    def __init__(self):
        pass
    
class Axis(RenderObject):
    def __init__(self):
        super().__init__()

    # Tegner linjerne 
    def draw(self, screen, pos_x, pos_y, zoom, size, camera):
        pygame.draw.line(screen, "Black", (size[0] / 2 - pos_x * zoom, 0), (size[0] / 2 - pos_x * zoom, size[1]))
        pygame.draw.line(screen, "Black", (0, size[1] / 2 - pos_y * zoom), (size[0], size[1] / 2 - pos_y * zoom))

class Function(RenderObject):
    def __init__(self, functionObject, resolution = 100):
        super().__init__()

        self.functionObject = functionObject
        self.resolution = resolution
        
    def draw(self, screen, pos_x, pos_y, zoom, size, camera):
        # TODO: There should either be passed a start and endpos or made them globally available to improve performance by not repeating calculations
        self.startPos = camera.getPosFromScreenCoords([0, 0])
        self.endPos = camera.getPosFromScreenCoords([size[0], 0])
        self.drawWidth = self.endPos[0] - self.startPos[0]

        self.prevScreenPos = None

        for i in range(self.resolution):
            # Graph position
            self.currentX = self.startPos[0] + (i / (self.resolution - 1)) * self.drawWidth
            self.currentY = self.functionObject.yFunc(self.currentX)

            # Ignore complex numbers
            if not self.currentY.is_real:
                continue

            # Screen position
            self.screenPos = camera.getPosFromGraphCoords([self.currentX, self.currentY])
            self.screenPos[0] = int(self.screenPos[0])
            self.screenPos[1] = int(self.screenPos[1])

            if self.prevScreenPos != None:
                if self.screenPos[1] >= 0 and self.screenPos[1] <= size[1] or self.prevScreenPos[1] >= 0 and self.prevScreenPos[1] <= size[1]:
                    pygame.draw.line(screen, (0, 0, 0), self.prevScreenPos, self.screenPos)
                
            
            self.prevScreenPos = self.screenPos

class Camera:
    def __init__(self, pos = [0, 0], zoomAmount = 1, size = [500, 500]):
        self.pos = pos
        self.zoomAmount = zoomAmount
        self.moveSpeed = 10
        
        # Calculate actual zoom scaling level
        if self.zoomAmount > 0:
            self.zoom = 1 / abs(self.zoomAmount)
        else:
            self.zoom = abs(self.zoomAmount)

        self.size = size
        self.surface = pygame.surface.Surface(self.size)

        self.permanentRenderObjects = []
        self.axis = Axis()
        self.permanentRenderObjects.append(self.axis)

        self.functionRenderObjects = []
        
        self.collisionRect = pygame.Rect([0, 0, self.size[0], self.size[1]])

    def render(self, screen, blitpos):
        self.surface.fill([255, 255, 255]) # Clear background

        # Render renderobjects to surface
        for obj in self.permanentRenderObjects:
            obj.draw(self.surface, self.pos[0], self.pos[1], self.zoom, self.size, self)
        for obj in self.functionRenderObjects:
            obj.draw(self.surface, self.pos[0], self.pos[1], self.zoom, self.size, self)

        screen.blit(self.surface, blitpos)

        # Update collisionRect with blitpos
        self.collisionRect = pygame.Rect([blitpos[0], blitpos[1], self.size[0], self.size[1]])

    def update(self):
        self.pressed = pygame.key.get_pressed()
        if self.pressed[pygame.K_w]:
            self.pos[1] -= self.moveSpeed / self.zoom
        if self.pressed[pygame.K_s]:
            self.pos[1] += self.moveSpeed / self.zoom

        if self.pressed[pygame.K_a]:
            self.pos[0] -= self.moveSpeed / self.zoom
        if self.pressed[pygame.K_d]:
            self.pos[0] += self.moveSpeed / self.zoom
    
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

                self.pos[0] -= self.afterPos[0] - self.beforePos[0]
                self.pos[1] -= self.afterPos[1] - self.beforePos[1]

    def getPosFromScreenCoords(self, screenPos):
        return [
            (screenPos[0] - self.size[0] / 2) / self.zoom + self.pos[0],
            ((screenPos[1] - self.size[1] / 2) / self.zoom + self.pos[1])
        ]
    
    def getPosFromGraphCoords(self, graphPos):
        return [
            (graphPos[0] - self.pos[0]) * self.zoom + self.size[0] / 2,
            ((-graphPos[1] - self.pos[1]) * self.zoom + self.size[1] / 2)
        ]

    def deleteAllFunctionRenderObjects(self):
        self.functionRenderObjects = []

    def addFunctionRenderObject(self, obj):
        self.functionRenderObjects.append(obj)

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