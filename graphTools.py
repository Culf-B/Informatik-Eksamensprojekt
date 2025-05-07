import pygame
pygame.init()

class RenderObject:
    def __init__(self):
        pass
        
    def draw(self, screen, pos_x, pos_y, zoom, size, camera):
        pass


class Axis(RenderObject):
    def __init__(self):
        super().__init__()

    # Tegner linjerne 
    def draw(self, screen, pos_x, pos_y, zoom, size, camera,):
        self.ox = size[0] / 2 - pos_x * zoom
        self.oy = size[1] / 2 - pos_y * zoom
                 # Indstillinger for ticks
        min_px     = 80           # mindste afstand i pixels mellem to labels
        world_step = 1            # start med 1 verdens-enhed
        # gang med 5 indtil labels er mindst min_px pixels fra hinanden
        while world_step * zoom < min_px:
            world_step *= 5
        PIXEL_INTERVAL = int(world_step * zoom)  # én world_step i pixels
        PIXEL_INTERVAL = max(PIXEL_INTERVAL, 1)
        # afstand mellem ticks i pixels
        TICK_SIZE      = 5      # halve tick-længde i pixels
        COLOR          = (0,0,0)  
         # --- Font til tal ---
        font = pygame.font.SysFont(None, 18) # størelsen for fontet 
        text_color = (0, 0, 0)
        
             # <-- Grid-linjer (let grå) -->
        offset_x = int(self.ox % PIXEL_INTERVAL)
        offset_y = int(self.oy % PIXEL_INTERVAL)
        for x in range(offset_x, int(size[0]), PIXEL_INTERVAL):
            pygame.draw.line(screen, (230,230,230), (x, 0), (x, size[1]), 1)
        for y in range(offset_y, int(size[1]), PIXEL_INTERVAL):
            pygame.draw.line(screen, (230,230,230), (0, y), (size[0], y), 1)
        pygame.draw.line(screen, "Black", (self.ox, 0), (self.ox, size[1]))
        pygame.draw.line(screen, "Black", (0,self.oy ), (size[0], self.oy))


        

        # --- X-aksens ticks ---
        # Beregn offset, så ticks følger origo
        offset_x = int(self.ox % PIXEL_INTERVAL)
        for x in range(offset_x, int(size[0]), PIXEL_INTERVAL):
            start = (x, self.oy - TICK_SIZE)
            end   = (x, self.oy + TICK_SIZE)
            pygame.draw.line(screen, COLOR, start, end, 1)
            #beregner tallet der sættes på ticks for x 
            val = (x - self.ox) / zoom
            txt_surf = font.render(str(int(val)), True, text_color)
            txt_rect = txt_surf.get_rect(           # <-- definer txt_rect her
            midtop=(x, self.oy + TICK_SIZE + 2))
            screen.blit(txt_surf, txt_rect)

        # --- Y-aksens ticks ---
        offset_y = int(self.oy % PIXEL_INTERVAL)
        for y in range(offset_y, int(size[1]), PIXEL_INTERVAL):
            start = (self.ox - TICK_SIZE, y)
            end   = (self.ox + TICK_SIZE, y)
            pygame.draw.line(screen, COLOR, start, end, 1)
            #beregner tallet der sættes på ticks for y
            val = -(y - self.oy) / zoom
            txt_surf = font.render(str(int(val)), True, text_color)
            txt_rect = txt_surf.get_rect(midright=(self.ox - TICK_SIZE - 2, y))
            screen.blit(txt_surf, txt_rect)




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
    def __init__(self, pos = [0, 0], zoom = 1, size = [500, 500]):
        self.pos = pos
        self.moveSpeed = 10
        
        # Calculate actual zoom scaling level
        self.zoom = zoom

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

                if event.y > 0:
                    self.zoom = self.zoom + self.zoom * 0.2
                elif event.y < 0:
                    self.zoom = self.zoom - self.zoom * 0.2

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