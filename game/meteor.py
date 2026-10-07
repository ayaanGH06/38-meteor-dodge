import pygame
import random
import math

SPLIT_MIN_RADIUS = 20    # meteors at or above this size fracture
FRAGMENT_COUNT = 2
SPREAD_ANGLE = 35        # degrees each fragment diverges from the parent's heading

class Meteor:
    def __init__(self, width):
        self.x = random.randint(0, width)
        self.y = -30
        self.radius = random.randint(12, 28)
        angle = random.uniform(70,110)
        speed = random.uniform(2,5)
        self.vx = math.cos(math.radians(angle))*speed
        self.vy = math.sin(math.radians(angle))*speed
        self.color = (
            random.randint(160,220),
            random.randint(80,120),
            random.randint(40,80)
        )
        self.rot = 0
        self.rot_speed = random.uniform(-3,3)

    def update(self):
        self.x+=self.vx; self.y+=self.vy
        self.rot=(self.rot+self.rot_speed)%360

    def off_screen(self, height):
        return self.y > height + 60

    def can_split(self):
        return self.radius >= SPLIT_MIN_RADIUS

    def split(self):
        """Return child fragments, or an empty list if this meteor is too small."""
        if not self.can_split():
            return []
        fragments = []
        heading = math.atan2(self.vy, self.vx)
        speed = math.hypot(self.vx, self.vy)
        for i in range(FRAGMENT_COUNT):
            # spread evenly from -SPREAD_ANGLE to +SPREAD_ANGLE around the parent's heading
            t = i / (FRAGMENT_COUNT - 1) if FRAGMENT_COUNT > 1 else 0.5
            offset = math.radians(-SPREAD_ANGLE + 2 * SPREAD_ANGLE * t)
            child = Meteor(0)
            child.radius = max(8, self.radius // 2)
            child.x = self.x + math.cos(heading + offset) * self.radius * 0.5
            child.y = self.y + math.sin(heading + offset) * self.radius * 0.5
            child.vx = math.cos(heading + offset) * speed * 1.2
            child.vy = math.sin(heading + offset) * speed * 1.2
            child.color = self.color
            child.rot = self.rot
            child.rot_speed = random.uniform(-5, 5)
            fragments.append(child)
        return fragments

    def collides(self, rect, pad=16):
        cx,cy=rect.centerx,rect.centery
        dx,dy=self.x-cx,self.y-cy
        return (dx**2+dy**2)**0.5 < self.radius + pad

    def draw(self, screen):
        import math
        pts=[]
        for i in range(7):
            angle=math.radians(self.rot+i*(360/7))
            r=self.radius*(0.8+0.2*(i%2))
            pts.append((int(self.x+r*math.cos(angle)),int(self.y+r*math.sin(angle))))
        pygame.draw.polygon(screen,self.color,pts)
        inner=[(int(self.x+(r*0.5)*math.cos(math.radians(self.rot+i*(360/7)))),
                int(self.y+(r*0.5)*math.sin(math.radians(self.rot+i*(360/7)))))
               for i,(cx,cy) in enumerate(pts)]
        pygame.draw.polygon(screen,tuple(max(0,c-40) for c in self.color),inner)
