import pygame, time, math

pygame.init()
resX, resY = 108 * 5, 192 * 5
screen = pygame.display.set_mode((resX, resY))
clock = pygame.time.Clock()
corrected = []

sound_files = ["C", "D", "E", "F", "G", "A", "B", "C2", "D2", "E2", "F2", "G2", "F2", "E2", "D2", "C2", "B", "A", "G", "F", "E", "D", "C"]

for name in sound_files:
    name = f"audio/{name}.wav"
    corrected.append(name)

sounds = [pygame.mixer.Sound(file) for file in corrected]

class Cube():
    def __init__(self, surface, color, posX, posY, height, width, outline, velX, velY, center):
        self.center = list(center)
        self.surface = surface
        self.color = color
        self.rect = pygame.Rect(posX, posY, width, height)
        self.outline = outline
        self.velX = velX
        self.velY = velY
        self.new_vel = 0.1
        self.next_sound_index = 0

    def draw(self):
        self.center[0] += self.velX
        self.center[1] += self.velY

        collision_event = False
        
        if self.center[0] - self.rect.width / 2 < 0:
            self.center[0] = self.rect.width / 2
            self.velX *= -1
            collision_event = True
        elif self.center[0] + self.rect.width / 2 > resX:
            self.center[0] = resX - self.rect.width / 2
            self.velX *= -1
            collision_event = True
        if self.center[1] - self.rect.height / 2 < 0:
            self.center[1] = self.rect.height / 2
            self.velY *= -1
            collision_event = True
        elif self.center[1] + self.rect.height / 2 > resY:
            self.center[1] = resY - self.rect.height / 2
            self.velY *= -1
            collision_event = True

        if collision_event:
            sounds[self.next_sound_index].play()
            self.next_sound_index = (self.next_sound_index + 1) % len(sounds)

        self.rect.center = self.center
        pygame.draw.rect(self.surface, self.color, self.rect, 0)

cube = Cube(surface=screen, color=(0, 255, 0), posX=resX // 2, posY=resY // 2, height=50, width=50, outline=0, velX=5, velY=5, center=(resX // 2, resY // 2))

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        pygame.draw.rect(surface=screen, color=(0, 255, 0), rect=(0, 0, resX, resY), width=5)

        cube.draw()

        pygame.display.flip()
        clock.tick(60) 
    pygame.quit()

if __name__ == "__main__":
    main()