import csv
import math
import time

import pygame

WIDTH, HEIGHT = 1280, 720
enemy_speed = 20

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defence")

clock = pygame.time.Clock()


class Game_Window:
    def __init__(self, path_dir):
        self.size = WIDTH * 0.75, HEIGHT * 0.75
        self.path = self.load_path(path_dir)
        self.game_screen = pygame.surface.Surface((WIDTH, HEIGHT))

    def load_path(self, path_dir):
        path = []
        with open(path_dir, "r", encoding='UTF8') as file:
            for i in csv.reader(file):
                path.append(i[0].split())
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
        progress = (
                           percent / 100 - (self.path_len(self.path[:cur_v - 1]) / self.path_len(self.path))) / (
                               (self.path_len(self.path[:cur_v]) / self.path_len(self.path)) - (
                                   self.path_len(self.path[:cur_v - 1]) / self.path_len(self.path)))
        pos = (int(self.path[cur_v - 2][0]) +
               ((int(self.path[cur_v - 1][0]) - int(self.path[cur_v - 2][0])) *
                progress), int(self.path[cur_v - 2][1]) +
               ((int(self.path[cur_v - 1][1]) - int(self.path[cur_v - 2][1])) *
                progress))
        if percent >= 100: pos = int(self.path[-1][0]), int(self.path[-1][1])
        return pos


class Side_Bar:
    def __init__(self):
        self.size = WIDTH * 0.2, HEIGHT
        self.pos = WIDTH * 0.80, 0.0
        self.health = 75
        self.holding = "Nailer"
        self.icons = {}
        self.characters = ["Nailer"]
        self.load_icons()

    def draw(self):
        pygame.draw.rect(display, (133, 101, 19), self.pos + self.size)
        # health bar
        pygame.draw.line(display, (150, 150, 150),
                         (self.pos[0] + self.size[0] * 0.1, self.pos[1] + self.size[1] * 0.05),
                         (self.pos[0] + self.size[0] * 0.9, self.pos[1] + self.size[1] * 0.05), 20)
        pygame.draw.line(display, (255, 0, 0),
                         (self.pos[0] + self.size[0] * 0.1 * 1.12, self.pos[1] + self.size[1] * 0.05 * 1.03),
                         (self.pos[0] + (self.size[0] * 0.9 * 0.99) * self.health / 100,
                          self.pos[1] + self.size[1] * 0.05 * 1.03), 15)
        char_surface = pygame.Surface((self.size[0] * 0.8, self.size[1] * 0.95))
        # draw icons
        for idx, icon in enumerate(self.icons):
            char_surface.blit(pygame.transform.scale(icon, (self.size[0] * 0.4, self.size[0] * 0.4)), ())
        # holding icon
        if self.holding is not None:
            surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(surface, (150, 150, 150, 100), (25, 25), 25)
            mx, my = pygame.mouse.get_pos()
            display.blit(surface, (mx - 25, my - 25))
        # widgets
        # for widget in self.widgets:
        #     if widget == "Nailer":
    def load_icons(self):
        for c in self.characters:
            self.icons[c] = pygame.transform.scale(pygame.image.load(c.lower()+".png"), (100, 100))


def redraw_window(game, side_bar, perc):
    game.game_screen.blit(
        pygame.transform.scale(pygame.image.load("map1/td_bg.png"),
                               (WIDTH, HEIGHT)), (0, 0))
    pygame.draw.circle(game.game_screen, (255, 0, 0),
                       game.path_evolution(perc), 20)
    display.blit(game.game_screen, (0, 0))
    side_bar.draw()


def main():
    game = Game_Window("map1/path.csv")
    side_bar = Side_Bar()
    running = True
    perc = 0
    while running:
        clock.tick(60)
        perc += 0.5
        print(perc)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     with open("map1/path.csv", "a", encoding='UTF8',
            #               newline='') as file:
            #         csv.writer(file).writerow([
            #             str(pygame.mouse.get_pos()[0]) + " " +
            #             str(pygame.mouse.get_pos()[1])
            #         ])
            #         print(
            #             str(pygame.mouse.get_pos()[0]) +
            #             str(pygame.mouse.get_pos()[1]))

        redraw_window(game, side_bar, perc)
        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()
