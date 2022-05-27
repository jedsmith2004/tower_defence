import pygame
import math


class Projectile:
    def __init__(self, pos, img, vel):
        self.pos = pos
        self.img = img
        self.vel = vel

    def render(self, display):
        self.pos[0] = self.pos[0] + self.vel[0]
        self.pos[1] = self.pos[1] + self.vel[1]
        rot = math.atan2(self.vel[0], self.vel[1])
        if rot < 0:
            rot += math.pi * 2
        rot = math.degrees(rot)

        display.blit(pygame.transform.rotate(self.img, rot), self.pos)


class Nailer:
    def __init__(self, pos, size, icon):
        self.pos = pos
        self.size = size
        self.icon = icon
        self.rotation = 0
        self.range = 300
        self.shoot_cooldown = 20
        self.cooldown_timer = self.shoot_cooldown
        self.projectile = None
        self.projectile_img = pygame.transform.scale(pygame.image.load("nail.png"), (int(self.size[0]*0.5), int(self.size[1]*0.5)))
        self.projectile_speed = 25

    def render(self, display, enemies, game):

        scaled = pygame.transform.rotate(pygame.transform.scale(self.icon, (int(self.size[0])*2, int(self.size[1])*2)), self.rotation)
        display.blit(scaled, (int(self.pos[0] - self.size[0]), int(self.pos[1] - self.size[1])))
        self.shoot(game, enemies)
        if self.projectile is not None:
            self.projectile.render(display)
            for enemy in enemies:
                if pygame.Rect(self.projectile.pos[0], self.projectile.pos[1], self.projectile.img.get_size()[0],
                               self.projectile.img.get_size()[1]).colliderect(enemy.get_rect()):
                    enemy.health -= 1
                    if enemy.health <= 0: enemy.dead = True

    def shoot(self, game, enemies):
        if self.cooldown_timer >= 1:
            self.cooldown_timer -= 1
        else:
            in_range = False
            for enemy in enemies[::-1]:
                steps = math.sqrt(
                    (enemy.pos[0] - self.pos[0]) ** 2 + (enemy.pos[1] - self.pos[1]) ** 2) / self.projectile_speed
                pos = game.path_evolution(enemy.perc + enemy.speed * (steps-2))
                if math.sqrt((pos[0] - self.pos[0]) ** 2 + (pos[1] - self.pos[1]) ** 2) < self.range:
                    in_range = True
                    self.rotation = math.atan2((pos[0] - self.pos[0]), (pos[1] - self.pos[1]))
                    if self.rotation < 0:
                        self.rotation += math.pi * 2
                    self.rotation = math.degrees(self.rotation - math.pi)
            if in_range:
                self.cooldown_timer = self.shoot_cooldown
                vel = math.sin(math.radians(self.rotation)-math.pi) * self.projectile_speed, math.cos(math.radians(self.rotation)-math.pi) * self.projectile_speed
                self.projectile = Projectile([self.pos[0], self.pos[1]], self.projectile_img, vel)
