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
    def draw(self,screen,pos_x,pos_y,zoom,size):
        pygame.draw.line(screen, "Black", (size[0]/2 + pos_x, 0), (size[0]/2 + pos_x, size[1]))
        pygame.draw.line(screen, "Black", (0, size[1]/2 + pos_y), (size[0], size[1]/2 + pos_y))

class Function(RenderObject):
    def __init__(self,screen):
        super().__init__(screen)

class Camera:
    def __init__(self, pos = [0, 0], zoom = 1, size = [500, 500]):
        self.pos = pos
        self.zoom = zoom
        self.size = size
        self.surface = pygame.surface.Surface(self.size)

        self.renderObjects = []
        self.axis = Axis()
        self.renderObjects.append(self.axis)

    def render(self, screen, blitpos):
        self.surface.fill([255, 255, 255]) # Clear background

        # Render renderobjects to surface
        for obj in self.renderObjects:
            obj.draw(self.surface, self.pos[0], self.pos[1], self.zoom, self.size)

        screen.blit(self.surface, blitpos)

    def update(self):
        self.pressed = pygame.key.get_pressed()
        if self.pressed[pygame.K_w]:
            print("w is pressed")
            self.pos[1] += 1
        if self.pressed[pygame.K_s]:
            print("s is pressed")
            self.pos[1] -= 1  

        if self.pressed[pygame.K_a]:
            print("a is pressed")
            self.pos[0] += 1
        if self.pressed[pygame.K_d]:
            print("d is pressed")
            self.pos[0] -= 1  
            
       
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    cam = Camera()

    while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("White")

        cam.update()
        cam.render(screen, [0, 0])

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60