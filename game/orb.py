import pygame
import random
import math

ORB_RADIUS = 12
ORB_SPEED = 1.5

class ShieldOrb:
    def __init__(self, width):
        self.base_x = random.randint(40, width - 40)
        self.x = self.base_x
        self.y = -20
        self.age = 0

    def update(self):
        self.age += 1
        self.y += ORB_SPEED
        self.x = self.base_x + math.sin(self.age * 0.05) * 30  # gentle sideways drift

    def off_screen(self, height):
        return self.y > height + 30

    def collides(self, rect):
        dx, dy = self.x - rect.centerx, self.y - rect.centery
        return (dx**2 + dy**2) ** 0.5 < ORB_RADIUS + 20

    def draw(self, screen):
        pulse = 1 + 0.25 * math.sin(self.age * 0.15)
        glow_r = int(ORB_RADIUS * 2 * pulse)
        glow = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (80, 220, 255, 70), (glow_r, glow_r), glow_r)
        screen.blit(glow, (int(self.x) - glow_r, int(self.y) - glow_r))
        pygame.draw.circle(screen, (120, 240, 255), (int(self.x), int(self.y)), ORB_RADIUS)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), ORB_RADIUS // 2)