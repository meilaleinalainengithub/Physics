import pygame, time, math, os

pygame.init()
resX, resY = 108 * 5, 192 * 5
screen = pygame.display.set_mode((resX, resY))
clock = pygame.time.Clock()
corrected = []

sound_files = ["E2", "E2", "C2", "E2", "G2", "G", "C2", "G", "E", "A", "B", "A", "A", "G", "E2", "G2", "G2", "F2", "G2", "E2", "C2", "D2", "B"]

for name in sound_files:
    name = f"audio/{name}.wav"
    corrected.append(name)

sounds = [pygame.mixer.Sound(file) for file in corrected]

def hsv_to_rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    return int(r * 255), int(g * 255), int(b * 255)

class BouncyBall:
    def __init__(self, surface, center, radius, width, velX, velY):
        self.center = list(center)
        self.surface = surface
        self.radius = radius
        self.width = width
        self.velX = velX
        self.velY = velY
        self.next_sound_index = 0
        self.new_vel = 0.1
        self.trail = []
        self.circle_radius = resX / 2.1
        self.circle_centerX = resX / 2
        self.circle_centerY = resY / 2

        self.speed = False
        self.grow = False
        self.circle_grow = False

    def get_color(self):
        elapsed_time = time.time() % 4.5
        hue = (elapsed_time / 4.5) * 360
        return hsv_to_rgb(hue, 1, 1)

    def draw(self):
        pygame.draw.circle(surface=screen, color=(0, 255, 0), center=(self.circle_centerX, self.circle_centerY), radius=self.circle_radius, width=int((resX / 2.3) / 40))
        self.center[0] += self.velX
        self.center[1] += self.velY
        self.velY += self.new_vel
        print(f"VELOCITY: {self.velY}\nRADIUS: {self.radius}")

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

            if self.speed:
                self.new_vel += 0.1
            if self.grow:
                self.radius += 1.0

            pygame.draw.circle(surface=screen, color=(0, 255, 0), center=(self.circle_centerX, self.circle_centerY), radius=self.circle_radius, width=int((resX / 2.3) / 40))

            if self.radius <= 0 or self.radius >= resX / 2.1:
                time.sleep(3)
                pygame.quit()
            self.play_sound()

        color = self.get_color()
        self.trail.append((self.center[0], self.center[1], 255))
        if len(self.trail) > 120:
            self.trail.pop(0)
        
        for pos in self.trail:
            trail_color = (*color, pos[2])
            trail_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, trail_color, (self.radius, self.radius), self.radius)
            self.surface.blit(trail_surface, (pos[0] - self.radius, pos[1] - self.radius))

        for i in range(len(self.trail)):
            self.trail[i] = (self.trail[i][0], self.trail[i][1], max(0, self.trail[i][2] - 3))

        pygame.draw.circle(self.surface, color, (int(self.center[0]), int(self.center[1])), self.radius, int((resX / 2.3) / 40))
        
    def play_sound(self):
        sounds[self.next_sound_index].play()
        self.next_sound_index = (self.next_sound_index + 1) % len(sounds)

ball = BouncyBall(surface=screen, center=(resX / 2, resY / 2), radius=20, width=0, velX=5, velY=5)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        ball.draw()

        pygame.display.flip()
        clock.tick(60) 
    pygame.quit()

if __name__ == "__main__":
    BouncyBall = BouncyBall(surface=screen, center=(resX / 2, resY / 2), radius=20, width=0, velX=5, velY=5)

    if input("Faster every bounce? (Y/N): ").lower() == "y":
        ball.speed = True
    if input("Grow every bounce? (Y/N): ").lower() == "y":
        ball.grow = True
    if input("Circle grow every bounce? (Y/N): ").lower() == "y":
        ball.circle_grow = True

    main()
