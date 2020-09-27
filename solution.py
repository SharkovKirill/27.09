import pygame
from random import random, uniform
from math import sqrt

SCREEN_SIZE = (1280, 720)


class Vector():
    def __init__(self, tuple, speed=(random() * 2, random() * 2)):
        self.x = tuple[0]
        self.y = tuple[1]
        self.pos = tuple
        self.speed = speed

    def __len__(self):
        return int(sqrt((self.x ^ 2) + (self.y ^ 2)))

    def __add__(self, other):
        return Vector((self.x + other.x, self.y + other.y), self.speed)

    def __sub__(self, other):
        return Vector((self.x - other.x, self.y - other.y), self.speed)

    def __mul__(self, int):
        return Vector((self.x * int, self.y * int), self.speed)

    def int_pair(self):
        return tuple(int(self.x), int(self.y))


class Line():
    vectors = []

    def __init__(self):
        pass

    def add_vector(cls, vector):
        Line.vectors.append(vector)

    def draw_points(cls, points='Line.vectors', style="points", width=4, color=(255, 255, 255)):
        if points == 'Line.vectors':
            if style == "line":
                for point_number in range(-1, len(Line.vectors) - 1):
                    pygame.draw.line(gameDisplay, color,
                                     (int(Line.vectors[point_number].x), int(Line.vectors[point_number].y)),
                                     (int(Line.vectors[point_number + 1].x), int(Line.vectors[point_number + 1].y)),
                                     width)

            elif style == "points":
                for vector in Line.vectors:
                    pygame.draw.circle(gameDisplay, color,
                                       (int(vector.x), int(vector.y)), width)
        else:
            if style == "line":
                for point_number in range(-1, len(points) - 1):
                    pygame.draw.line(gameDisplay, color, (int(points[point_number].x), int(points[point_number].y)),
                                     (int(points[point_number + 1].x), int(points[point_number + 1].y)), width)

            elif style == "points":
                for point in points:
                    pygame.draw.circle(gameDisplay, color,
                                       (int(point[0]), int(point[1])), width)

    def set_points(cls):
        for vector in range(len(Line.vectors)):
            Line.vectors[vector] = Line.vectors[vector] + Vector(Line.vectors[vector].speed)
            if Line.vectors[vector].x > SCREEN_SIZE[0] or Line.vectors[vector].x < 0:
                Line.vectors[vector].speed = (- Line.vectors[vector].speed[0], Line.vectors[vector].speed[1])
            if Line.vectors[vector].y > SCREEN_SIZE[1] or Line.vectors[vector].y < 0:
                Line.vectors[vector].speed = (Line.vectors[vector].speed[0], -Line.vectors[vector].speed[1])


class Joint(Line):
    def get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha) + ((Joint.get_point(points, alpha, deg - 1)) * (1 - alpha))

    def get_points(base_points, count):
        alpha = 1 / count
        result = []
        for i in range(count):
            result.append(Joint.get_point(base_points, i * alpha))
        return result

    def get_joint(count):
        if len(Line.vectors) < 3:
            return []
        result = []
        for i in range(-2, len(Line.vectors) - 2):
            pnt = []
            pnt.append((Line.vectors[i] + Line.vectors[i + 1]) * 0.5)
            pnt.append(Line.vectors[i + 1])
            pnt.append((Line.vectors[i + 1] + Line.vectors[i + 2]) * 0.5)
            result.extend(Joint.get_points(pnt, count))

        return result


class Help():
    @staticmethod
    def display():
        gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("arial", 30)
        font2 = pygame.font.SysFont("serif", 30)
        data = [["F1", "Помощь"], ["R", "Перезапуск"], ["P", "Воспроизвести / Пауза"], ["Num+", "Добавить точку"],
                ["Num-", "Удалить точку"], ["H", "Ускорение движения"], ["L", "Замедление движения"],
                ["", ""], [count_points, "текущих точек"]]

        pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for item, text in enumerate(data):
            gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
            gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * item))


if __name__ == "__main__":
    line = Line()
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    steps = 10
    working = True
    show_help = False
    pause = False

    color_param = 0
    color = pygame.Color(0)

    while working:
        count_points = str(len(Line.vectors))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    Line.vectors = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                    line.add_vector(Vector((uniform(1, 1279), uniform(1, 720))))
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                    try:
                        Line.vectors.pop()
                    except:
                        pass
                if event.key == pygame.K_h:
                    for vector in Line.vectors:
                        sp0 = vector.speed[0]
                        sp1 = vector.speed[1]
                        vector.speed = (sp0 * 1.2, sp1 * 1.2)
                if event.key == pygame.K_l:
                    for vector in Line.vectors:
                        sp0 = vector.speed[0]
                        sp1 = vector.speed[1]
                        vector.speed = (sp0 * 0.8, sp1 * 0.8)



            if event.type == pygame.MOUSEBUTTONDOWN:
                line.add_vector(Vector(event.pos))

        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)
        line.draw_points()
        line.draw_points(Joint.get_joint(steps), "line", 4, color)
        if not pause:
            line.set_points()
        if show_help:
            Help.display()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
