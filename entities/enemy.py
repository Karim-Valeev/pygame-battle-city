import pygame
import math
import time as t
import random

from entities.level import Level, Point, Tile, empty_next_tile_horiz, empty_next_tile_vert
from entities.shot import Shot
from entities.tank import Tank

POSSIBLE_WAYS = [0, 1, 2, 3]


def find_random_path(angle):
    angle //= 90
    random.shuffle(POSSIBLE_WAYS)
    while angle == POSSIBLE_WAYS[0]:
        random.shuffle(POSSIBLE_WAYS)
    angle = POSSIBLE_WAYS[0] * 90
    return angle


class Enemy(Tile, Tank):

    def __init__(self, x=None, y=None):
        super().__init__('enemy', Point(x, y))
        self.alive = True
        self.size = 1
        self.shoot_timer = t.time()
        self.angle = 0
        self.previous_angle = 180
        self.rotate_enemy()
        self.rect = pygame.Rect(self.position.X * 25, self.position.Y * 25 + 50, 26, 26)

    def shoot(self, level, global_timer):
        if global_timer - self.shoot_timer > 2:
            shot = Shot(Point(self.position.X, self.position.Y), self.angle, 1)
            level.shot_list.append(shot)
            self.shoot_timer = t.time()

    def move(self, global_timer, level, counter, player):

        self.shoot(level, global_timer)

        movement_speed = 0.25

        flag = False
        if self.angle == 90:
            flag = self.update_position(movement_speed, 'h',
                                        math.ceil(self.position.X + self.size + movement_speed),
                                        Level.width,
                                        math.ceil(self.position.X + movement_speed + self.size), self.position.Y, level,
                                        player)
        elif self.angle == 270:
            flag = self.update_position(-movement_speed, 'h', -movement_speed, self.position.X - movement_speed,
                                        math.floor(self.position.X - movement_speed), self.position.Y, level, player)
        elif self.angle == 0:
            flag = self.update_position(-movement_speed, 'v', -movement_speed, self.position.Y - movement_speed,
                                        self.position.X, math.floor(self.position.Y - movement_speed), level, player)
        elif self.angle == 180:
            flag = self.update_position(movement_speed, 'v',
                                        math.ceil(self.position.Y + self.size + movement_speed),
                                        Level.height,
                                        self.position.X, math.ceil(self.position.Y + self.size + movement_speed), level,
                                        player)

        if not flag:
            if counter == 3:
                return
            else:
                counter += 1
                self.angle = find_random_path(self.angle)
                self.move(global_timer, level, counter, player)

    def update_position(self, movement_speed, method_name, condition1, condition2, x, y, level, player):
        self.rotate_enemy()
        self.previous_angle = self.angle
        if condition1 < condition2:
            if method_name == 'h' and empty_next_tile_horiz(self, x, y, level):
                self.rect = pygame.Rect((self.position.X + movement_speed * 2) * 25, self.position.Y * 25 + 50, 26, 26)
                if not pygame.sprite.collide_rect(self, player):
                    self.position.X += movement_speed
                    return True
            elif method_name == 'v' and empty_next_tile_vert(self, x, y, level) and not pygame.sprite.collide_rect(self,
                                                                                                                   player):
                self.rect = pygame.Rect(self.position.X * 25, (self.position.Y + movement_speed * 2) * 25 + 50, 26, 26)
                if not pygame.sprite.collide_rect(self, player):
                    self.position.Y += movement_speed
                    return True
            self.rect = pygame.Rect(self.position.X * 25, self.position.Y * 25 + 50, 26, 26)
        return False

    def rotate_enemy(self):
        self.image = pygame.transform.rotate(self.image, self.previous_angle - self.angle)
