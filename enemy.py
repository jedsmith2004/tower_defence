import pygame

class L1:
    def __init__(self):
        self.perc = 0
        self.pos = 0,0
        self.speed = 0.3
        self.damage = 1
        self.radius = 20
        self.dead = False

    def render(self, display, positon):
        self.perc += self.speed
        self.pos = positon
        pygame.draw.circle(display, (255, 0, 0),
                           positon, self.radius)
        if self.perc >= 100: return False
        return True

    def get_rect(self):
        return pygame.Rect(self.pos[0]-self.radius, self.pos[1]-self.radius, self.radius, self.radius)