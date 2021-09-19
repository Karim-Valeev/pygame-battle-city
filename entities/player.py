import pygame
import math
import time as t

from entities.level import Level, Point, Tile, empty_next_tile_horiz, empty_next_tile_vert
from entities.shot import Shot
from entities.tank import Tank


class Player(Tile, Tank):
    def __init__(self, x, y):
        super().__init__("player", Point(x, y))
        self.score = 0
        self.count_enemies_killed = 0
        self.size = 1
        self.angle = 0
        self.hp = 3
        self.rect = pygame.Rect(self.position.X * 25, self.position.Y * 25 + 50, 26, 26)
        self.shoot_timer = t.time()

    def shoot(self, level, global_timer):
        if global_timer - self.shoot_timer > 0.5:
            shot = Shot(Point(self.position.X, self.position.Y), self.angle, 0)
            level.shot_list.append(shot)
            self.shoot_timer = t.time()

    def move(self, event, level, global_timer):
        movement_speed = 0.25
        if event.key == pygame.K_RIGHT:
            self.update_position(
                90,
                movement_speed,
                "h",
                math.ceil(self.position.X + self.size + movement_speed),
                Level.width,
                math.ceil(self.position.X + movement_speed + self.size),
                self.position.Y,
                level,
            )
        elif event.key == pygame.K_LEFT:
            self.update_position(
                270,
                -movement_speed,
                "h",
                -movement_speed,
                self.position.X - movement_speed,
                math.floor(self.position.X - movement_speed),
                self.position.Y,
                level,
            )
        elif event.key == pygame.K_UP:
            self.update_position(
                0,
                -movement_speed,
                "v",
                -movement_speed,
                self.position.Y - movement_speed,
                self.position.X,
                math.floor(self.position.Y - movement_speed),
                level,
            )
        elif event.key == pygame.K_DOWN:
            self.update_position(
                180,
                movement_speed,
                "v",
                math.ceil(self.position.Y + self.size + movement_speed),
                Level.height,
                self.position.X,
                math.ceil(self.position.Y + self.size + movement_speed),
                level,
            )
        elif event.key == pygame.K_SPACE:
            self.shoot(level, global_timer)

    def update_position(self, should_angle, movement_speed, method_name, condition1, condition2, x, y, level):
        self.rotate(should_angle)
        if condition1 < condition2:
            no_collision = True
            if method_name == "h" and empty_next_tile_horiz(self, x, y, level):
                test_rect = pygame.Rect((self.position.X + movement_speed) * 25, self.position.Y * 25 + 50, 26, 26)
                for enemy in level.enemy_list:
                    enemy.rect = pygame.Rect(enemy.position.X * 25, enemy.position.Y * 25 + 50, 50, 50)
                    if test_rect.colliderect(enemy.rect):
                        no_collision = False
                        break
                if no_collision:
                    self.position.X += movement_speed
            elif method_name == "v" and empty_next_tile_vert(self, x, y, level):
                test_rect = pygame.Rect(self.position.X * 25, (self.position.Y + movement_speed) * 25 + 50, 26, 26)
                for enemy in level.enemy_list:
                    enemy.rect = pygame.Rect(enemy.position.X * 25, enemy.position.Y * 25 + 50, 50, 50)
                    if test_rect.colliderect(enemy.rect):
                        no_collision = False
                        break
                if no_collision:
                    self.position.Y += movement_speed
            self.rect = pygame.Rect(self.position.X * 25, self.position.Y * 25 + 50, 26, 26)
