import pygame, time, math

pygame.init()
resX, resY = 108 * 5, 192 * 5
screen = pygame.display.set_mode((resX, resY))
clock = pygame.time.Clock()

class Cube():
    def __init__(self, surface, color, posX, posY, height, width, outline, velX, velY, center):
        self.surface = surface
        self.color = color
        self.rect = (posX, posY, width, height)
        self.outline = outline
        self.velX = velX
        self.velY = velY
        self.center = list[center]

    def draw(self):
        self.center[0] += self.velX
        self.center[1] += self.velY
        self.velY += self.new_vel

        distance_from_center = math.sqrt((self.center[0] - resX / 2) ** 2 + (self.center[1] - resY / 2) ** 2)
        if distance_from_center + self.radius > resX / 2.1:
            angle = math.atan2(self.center[1] - resY / 2, self.center[0] - resX / 2)
            normal = (math.cos(angle), math.sin(angle))
            dot_product = self.velX * normal[0] + self.velY * normal[1]
            self.velX -= 2 * dot_product * normal[0]
            self.velY -= 2 * dot_product * normal[1]

            overlap = (distance_from_center + self.radius - resX / 2.1)
            self.center[0] -= overlap * normal[0]
            self.center[1] -= overlap * normal[1]

Cube = Cube(surface=screen, color=(0, 0, 0), posX=0, posY=0, height=1, width=1, outline=0, velX=5, velY=5, center=(resX / 2, resY / 2))

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        pygame.draw.rect(surface=screen, color=(0, 255, 0), rect=(0, 0, resX, resY), width=5)

        Cube.draw()

        pygame.display.flip()
        clock.tick(60) 
    pygame.quit()

main()