import csv
import math
import time

import pygame

import enemy
import tower

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1280, 720
enemy_speed = 20

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defence")

clock = pygame.time.Clock()

towers = {"Nailer": tower.Nailer}

class Game_Window:
    def __init__(self, path_dir):
        self.size = WIDTH * 0.75, HEIGHT * 0.75
        self.path = self.load_path(path_dir)
        self.game_screen = pygame.surface.Surface((WIDTH, HEIGHT))
        self.path_ar = 0

    def load_path(self, path_dir):
        path = []
        with open(path_dir, "r", encoding='UTF8') as file:
            for idx, i in enumerate(csv.reader(file)):
                if idx == 0:
                    self.path_ar = [int(i[0]),int(i[1][0:].strip('\n'))]
                    # print(WIDTH/int(self.path_ar[0]))
                else:
                    # print(self.path_ar[1])
                    vx, vy = int(i[0].split()[0]) * (WIDTH/int(self.path_ar[0])), int(i[0].split()[1]) * (HEIGHT/int(self.path_ar[1]))
                    path.append((vx, vy))
        return path

    def path_len(self, path):
        if len(path) > 1:
            length = math.sqrt((int(path[1][0]) - int(path[0][0])) ** 2 +
                               (int(path[1][1]) - int(path[0][1])) ** 2)
        else:
            length = 0
        for idx in range(1, len(path) - 1):
            v = int(path[idx + 1][0]) - int(path[idx][0]), int(
                path[idx + 1][1]) - int(path[idx][1])
            length += math.sqrt(v[0] ** 2 + v[1] ** 2)

        return length

    def path_evolution(self, percent):
        cur_length = self.path_len(self.path) / 100 * percent
        cur_v = len(self.path)
        for idx in range(len(self.path)):
            if cur_length - self.path_len(self.path[:idx]) < 0:
                cur_v = idx
                break
        progress = (percent / 100 - (self.path_len(self.path[:cur_v - 1]) / self.path_len(self.path))) / (
                    (self.path_len(self.path[:cur_v]) / self.path_len(self.path)) - (
                    self.path_len(self.path[:cur_v - 1]) / self.path_len(self.path)))
        pos = (int(self.path[cur_v - 2][0]) +
               ((int(self.path[cur_v - 1][0]) - int(self.path[cur_v - 2][0])) *
                progress), int(self.path[cur_v - 2][1]) +
               ((int(self.path[cur_v - 1][1]) - int(self.path[cur_v - 2][1])) *
                progress))
        if percent >= 100: pos = int(self.path[-1][0]), int(self.path[-1][1])
        return pos

    def check_placement(self, mx, my, radius):
        for v in range(len(self.path)-1):
            vx, vy = int(self.path[v][0]), int(self.path[v][1])
            nx, ny = int(self.path[v + 1][0]), int(self.path[v + 1][1])

            vec_l = math.sqrt((nx - vx) ** 2 + (ny - vy) ** 2)
            nv_l = math.sqrt((mx - nx) ** 2 + (my - ny) ** 2)
            pv_l = math.sqrt((mx - vx) ** 2 + (my - vy) ** 2)
            # print(vec_l, vec_l + (HEIGHT / 18), nv_l, pv_l, (nv_l + pv_l))
            if vec_l + radius/(vec_l/81) + 3 > (nv_l + pv_l): return False
        return True

class Side_Bar:
    def __init__(self):
        self.size = WIDTH * 0.2, HEIGHT
        self.pos = WIDTH * 0.80, 0.0
        self.health = 100
        self.holding = None
        self.icons = {}
        self.characters = ["Nailer"]
        self.top_icons = {}
        self.load_icons()
        self.box_rects = []
        self.left_edge = self.pos[0] + self.size[0] * 0.1
        self.mid_edge = self.pos[0] + self.size[0] * 0.55
        self.top_edge = self.pos[1] + self.size[1] * 0.15
        self.cash = 0
        self.revenue = 10

        for box in range(10):
            b_x = int(self.left_edge if not box % 2 else self.mid_edge)
            b_y = int(self.top_edge + (box//2)*self.size[0]*0.45)
            self.box_rects.append((b_x, b_y, int(self.size[0] * 0.35), int(self.size[0] * 0.35)))

    def draw(self):
        pygame.draw.rect(display, (133, 101, 19), self.pos + self.size)
        # health bar
        pygame.draw.line(display, (150, 150, 150),
                         (self.pos[0] + self.size[0] * 0.1, self.pos[1] + self.size[1] * 0.05),
                         (self.pos[0] + self.size[0] * 0.8, self.pos[1] + self.size[1] * 0.05), 20)
        if self.health != 0:
            pygame.draw.line(display, (255, 0, 0),
                         (self.pos[0] + self.size[0] * 0.1 * 1.12, self.pos[1] + self.size[1] * 0.05),
                         (self.pos[0] + self.size[0] * 0.1 * 1.12 + (self.size[0] * 0.7 * 0.96) * self.health / 100,
                          self.pos[1] + self.size[1] * 0.05), 15)
        # health number
        font = pygame.font.SysFont("",30,True)
        text = font.render(str(self.health), True, (255,0,0))
        display.blit(text, (self.pos[0] + self.size[0] * 0.82, self.pos[1] + self.size[1] * 0.052-20/2))
        # draw cash
        font = pygame.font.SysFont("", 30, False)
        text = font.render("$" + str(self.cash), True, (0, 200, 0))
        display.blit(text, (self.pos[0] + self.size[0] * 0.1, self.pos[1] + self.size[1] * 0.095))
        # draw revenue
        font = pygame.font.SysFont("", 30, False)
        text = font.render("^" + str(self.cash), True, (0, 255, 0))
        display.blit(text, (self.pos[0] + self.size[0] * 0.55, self.pos[1] + self.size[1] * 0.095))
        # draw icons
        for box in range(10):
            col = (150,150,150) if box < len(self.icons) else (100,100,100)
            pygame.draw.rect(display, col, self.box_rects[box])
        for idx, c in enumerate(self.characters):
            new_icon = pygame.transform.scale(self.icons[c], (int(self.size[0] * 0.35), int(self.size[0] * 0.35)))
            display.blit(new_icon, (self.left_edge if not idx % 2 else self.mid_edge, self.top_edge + (idx//2)*self.size[0]*0.45))

    def collide_boxes(self):
        mx, my = pygame.mouse.get_pos()
        for idx, box in enumerate(self.box_rects):
            if pygame.Rect(box).collidepoint(mx, my): return idx
        return False


    def load_icons(self):
        for c in self.characters:
            self.icons[c] = pygame.transform.scale(pygame.image.load(c.lower()+".png"), (1000, 1000))
            self.top_icons[c] = pygame.transform.scale(pygame.image.load(c.lower()+"_top.png"), (1000, 1000))


    def render_holding(self, game):
        radius = HEIGHT / 18
        surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        col = (150, 150, 150, 100) if game.check_placement(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], radius) else (255, 0, 0, 100)
        pygame.draw.circle(surface, col, (radius, radius), radius)
        mx, my = pygame.mouse.get_pos()
        display.blit(surface, (mx - radius, my - radius))
        display.blit(pygame.transform.scale(self.top_icons[self.holding], (int(radius*2),int(radius*2))), (mx - radius, my - radius))


def redraw_window(game, side_bar, placed, enemies):
    game.game_screen.blit(
        pygame.transform.scale(pygame.image.load("map1/td_bg.png"),
                               (WIDTH, HEIGHT)), (0, 0))

    for c_enemy in enemies:
        if c_enemy.dead:
            enemies.remove(c_enemy)
            del c_enemy
            continue
        if not c_enemy.render(game.game_screen, game.path_evolution(c_enemy.perc)):
            if side_bar.health >= c_enemy.damage: side_bar.health -= c_enemy.damage
            else: side_bar.health = 0
            enemies.remove(c_enemy)
            del c_enemy
    for t in placed: t.render(game.game_screen, enemies, game)

    display.blit(game.game_screen, (0, 0))
    side_bar.draw()
    if side_bar.holding: side_bar.render_holding(game)


def main():
    game = Game_Window("map1/path.csv")
    side_bar = Side_Bar()
    running = True
    placed = []
    enemies = []
    last_time = time.time()
    rounds = [x.strip("\n").split() for x in open("rounds.txt", "r")]
    round = 0
    enemies_left = int(rounds[0][0])

    while running:
        clock.tick(60)

        if time.time()-last_time >= float(rounds[round][2]):
            print(enemies_left, round)
            if enemies_left > 0: enemies_left -= 1
            else:
                round += 1
                enemies_left = int(rounds[round][0])
            enemies.append(eval("enemy." + rounds[round][1] + "()"))
            last_time = time.time()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if side_bar.holding is None:
                    box = side_bar.collide_boxes()
                    if box is not False and box < len(side_bar.characters): side_bar.holding = side_bar.characters[box]
                else:
                    mx, my = pygame.mouse.get_pos()
                    if pygame.Rect(side_bar.pos[0], side_bar.pos[1], side_bar.size[0], side_bar.size[1]).collidepoint(mx, my):
                        side_bar.holding = None
                    elif game.check_placement(mx, my, HEIGHT / 18):
                        placed.append(towers[side_bar.holding]([mx,my],(HEIGHT / 18, HEIGHT / 18), side_bar.top_icons[side_bar.holding]))
                        side_bar.holding = None

                # with open("map1/path.csv", "a", encoding='UTF8',
                #           newline='') as file:
                #     csv.writer(file).writerow([
                #         str(pygame.mouse.get_pos()[0]) + " " +
                #         str(pygame.mouse.get_pos()[1])
                #     ])
                #     print(
                #         str(pygame.mouse.get_pos()[0]) +
                #         str(pygame.mouse.get_pos()[1]))

        redraw_window(game, side_bar, placed, enemies)
        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()
