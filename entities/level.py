import pygame
import os
import math
import random


def get_tiles():
    result = []
    return result


EPS = 1e-09


class Point:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __hash__(self):
        return hash((self.X, self.Y))

    def __eq__(self, other):
        return math.isclose(self.X, other.X, rel_tol=EPS) and math.isclose(self.Y, other.Y, rel_tol=EPS)

    def __str__(self):
        return str(self.X) + ' : ' + str(self.Y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, name_img, point):
        pygame.sprite.Sprite.__init__(self)
        scale = 25
        if name_img == 'eagle' or name_img == 'player' or name_img == 'enemy' or name_img == 'shot':
            scale *= 2
        self.image = transform_img(name_img, scale)
        self.position = point
        self.angle = 0

    def rotate(self, should_angle):
        self.image = pygame.transform.rotate(self.image, self.angle - should_angle)
        self.angle = should_angle


class Level:
    height, width = 26, 26
    width_tile = 25

    def __init__(self, lev_name):
        self.name = lev_name
        self.map_objects = self.get_map()  # неподвижные объекты
        self.shot_list = []

        self.enemy_list = []
        self.hp_counter = 3

    def get_map(self):
        map_objects = {}
        with open(os.path.join('levels', self.name), 'r') as level:
            lines = level.readlines()
            for i in range(len(lines)):
                line = lines[i]
                # последний символ - перенос строки
                for j in range(len(line) - 1):
                    if line[j] == '.':
                        continue
                    tile_name = ''
                    if line[j] == 'B':
                        tile_name = 'brick'
                    if line[j] == 'S':
                        tile_name = 'stone'
                    if line[j] == 'E':
                        tile_name = 'eagle'
                    if line[j] == 'P':
                        tile_name = 'empty'
                    if tile_name == '':
                        raise Exception('This element does not contain in our base')
                    map_objects[Point(j, i)] = tile_name
        return map_objects

    def check_eagle(self):
        return 'eagle' in self.map_objects.values()

    def add_none_point(self, point, point_buff):
        points = [None, None, None, None]
        points[0] = Point(point.X, point.Y)
        points[1] = Point(point.X + 1, point.Y)
        points[2] = Point(point.X, point.Y + 1)
        points[3] = Point(point.X + 1, point.Y + 1)
        for i in range(len(points)):
            self.map_objects[points[i]] = 'None'
            point_buff.append(points[i])

    def delete_point(self, point):
        if point in self.map_objects.keys():
            del self.map_objects[point]
        else:
            pass
            # print('THIS POINT WASNT IN THE LIST BUT TRIED TO DELETE', point)

    # Прорисовка карты, игрока. списка пуль, списка врагов

    def blit_map(self, display, player):
        self.delete_collision(player)
        for shot in self.shot_list:
            self.blit_sprite(display, shot)
        for enemy in self.enemy_list:
            self.blit_sprite(display, enemy)
        self.blit_sprite(display, player)
        for key, value in self.map_objects.items():
            tile = Tile(value, key)
            self.blit_sprite(display, tile)

    def get_free_spawn_position(self, player):
        free_pos = []
        flag = True
        for i in range(0, 24, 2):
            point = Point(i, 0)
            if flag:
                if point == player.position:
                    flag = False
            if flag:
                for shot in self.shot_list:
                    if point == shot.position:
                        flag = False
                        break
            if flag:
                for enemy in self.enemy_list:
                    if point == enemy.position:
                        flag = False
                        break
            if flag:
                if point in self.map_objects.keys():
                    flag = False
            if flag:
                free_pos.append(point)
            flag = True

        random.shuffle(free_pos)
        return free_pos[0]

    def delete_collision(self, player):
        delete_shot, delete_point_p, delete_en = [], [], []
        for shot in self.shot_list:
            shot.move()
            delete_shot, delete_point_p = shot.find_collision(self, player, delete_shot, delete_point_p)
        for shot in delete_shot:
            if shot in self.shot_list:
                self.shot_list.remove(shot)
        for point in delete_point_p:
            del self.map_objects[point]

    # Прорисовка спрайта
    def blit_sprite(self, display, tile):
        display.blit(tile.image, (tile.position.X * self.width_tile, tile.position.Y * self.width_tile + 50))


def empty_next_tile_horiz(tile, x, y, level):
    return not (Point(x, y) in level.map_objects or
                Point(x, math.floor(y)) in level.map_objects or
                Point(x, math.ceil(y)) in level.map_objects or
                Point(x, math.ceil(y + tile.size)) in level.map_objects)


def empty_next_tile_vert(tile, x, y, level):
    return not (Point(x, y) in level.map_objects or
                Point(math.floor(x), y) in level.map_objects or
                Point(math.ceil(x), y) in level.map_objects or
                Point(math.ceil(x + tile.size), y) in level.map_objects)


def transform_img(name_img, scale):
    img = pygame.image.load(os.path.join('sprites', name_img + '.png'))
    return pygame.transform.scale(img, (scale, scale))
