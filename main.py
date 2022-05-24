import csv
import math

import pygame

WIDTH, HEIGHT = 1600, 900
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
            for i in csv.reader(file): path.append(i[0].split())
        return path


    def path_len(self, path):
        if len(path) > 1: length = math.sqrt((int(path[1][0]) - int(path[0][0])) ** 2 + (int(path[1][1]) - int(path[0][1])) ** 2)
        else: length = 0
        for idx in range(1, len(path)-1):
            v = int(path[idx+1][0]) - int(path[idx][0]), int(path[idx+1][1]) - int(path[idx][1])
            length += math.sqrt(v[0] ** 2 + v[1] ** 2)
    
        return length


    def path_evolution(self, percent):
        cur_length = self.path_len(self.path) / 100 * percent
        cur_v = len(self.path)
        for idx in range(len(self.path)):
            if cur_length - self.path_len(self.path[:idx]) < 0:
                cur_v = idx
                break
        progress = (percent/100 - (self.path_len(self.path[:cur_v-1]) / self.path_len(self.path))) / ((self.path_len(self.path[:cur_v]) / self.path_len(self.path)) - (self.path_len(self.path[:cur_v-1]) / self.path_len(self.path)))
        pos = (
            int(self.path[cur_v-2][0]) + ((int(self.path[cur_v-1][0]) - int(self.path[cur_v - 2][0])) * progress),
            int(self.path[cur_v-2][1]) + ((int(self.path[cur_v-1][1]) - int(self.path[cur_v - 2][1])) * progress)
        )
        if percent >= 100: pos = int(self.path[-1][0]), int(self.path[-1][1])
        return pos


class Side_Bar:
    def __init__(self):
        self.size = WIDTH * 0.2, HEIGHT
        self.pos = WIDTH * 0.80, 0

    def draw(self):
        pygame.draw.rect(display, (133, 101, 19), self.pos + self.size)


def redraw_window(game, side_bar, perc):
    game.game_screen.blit(pygame.transform.scale(pygame.image.load("map1/td_bg.png"), (WIDTH, HEIGHT)), (0, 0))
    pygame.draw.circle(game.game_screen, (255, 0, 0), game.path_evolution(perc), 20)
    display.blit(game.game_screen, (0, 0))
    side_bar.draw()



def main():
    game = Game_Window("map1/path.csv")
    side_bar = Side_Bar()
    running = True
    perc = 0
    while running:
        clock.tick(60)
        perc += 0.2
        # print(path_evolution(path, perc))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                with open("map1/path.csv", "a", encoding='UTF8', newline='') as file:
                    csv.writer(file).writerow([str(pygame.mouse.get_pos()[0]) + " " + str(pygame.mouse.get_pos()[1])])
                    print(str(pygame.mouse.get_pos()[0]) + str(pygame.mouse.get_pos()[1]))

        redraw_window(game, side_bar, perc)
        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()
