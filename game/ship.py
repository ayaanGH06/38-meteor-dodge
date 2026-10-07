import pygame

SPEED = 5
LASER_SPEED = 10
FIRE_COOLDOWN = 12

class Laser:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 2, y - 14, 4, 14)

    def update(self):
        self.rect.y -= LASER_SPEED

    def off_screen(self):
        return self.rect.bottom < 0

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 80, 80), self.rect, border_radius=2)
        
class Ship:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x-20, y-20, 40, 40)
        self.color = (80, 160, 240)
        self.trail = []
        self.lasers = []
        self.cooldown = 0

    def move(self, keys, width, height):
        dx=dy=0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx=-SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx=SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy=-SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy=SPEED
        self.rect.x=max(0,min(width-self.rect.width,self.rect.x+dx))
        self.rect.y=max(0,min(height-self.rect.height,self.rect.y+dy))
        self.trail.append(tuple(self.rect.center))
        if len(self.trail)>10: self.trail.pop(0)

    def shoot(self, keys):
        if self.cooldown > 0:
            self.cooldown -= 1
        if keys[pygame.K_SPACE] and self.cooldown == 0:
            self.lasers.append(Laser(self.rect.centerx, self.rect.top))
            self.cooldown = FIRE_COOLDOWN

    def update_lasers(self):
        for laser in self.lasers:
            laser.update()
        self.lasers = [l for l in self.lasers if not l.off_screen()]

    def draw(self, screen):
        for laser in self.lasers:
            laser.draw(screen)
        for i,pos in enumerate(self.trail):
            alpha=20+i*20
            r=3+i//2
            s=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
            pygame.draw.circle(s,(80,160,240,alpha),(r,r),r)
            screen.blit(s,(pos[0]-r,pos[1]-r))
        # ship body
        cx,cy=self.rect.center
        pts=[(cx,cy-18),(cx-14,cy+14),(cx,cy+6),(cx+14,cy+14)]
        pygame.draw.polygon(screen,self.color,pts)
        # engine glow
        pygame.draw.circle(screen,(255,180,60),(cx,cy+12),5)
