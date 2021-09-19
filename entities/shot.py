import math
from entities.level import Point, Tile


class Shot(Tile):
    def __init__(self, point, angle, owner):
        super().__init__('shot', point)
        self.rotate(angle)
        self.size = 1
        # If owner = 0, then player's shot
        # If owner = 1 then enemy's shot
        self.owner = owner

    def move(self):
        if self.angle == 0:
            self.position.Y -= 1
        elif self.angle == 90:
            self.position.X += 1
        elif self.angle == 180:
            self.position.Y += 1
        elif self.angle == 270:
            self.position.X -= 1

    def check_collision_with_obj(self, delete_shot, delete_point, objects):
        x = self.position.X
        y = self.position.Y
        point1, point2 = None, None
        if self.angle == 0 or self.angle == 180:
            y = self.round(y)
            point1, point2 = self.check_vert(objects, x, y)
        elif self.angle == 270 or self.angle == 90:
            x = self.round(x)
            point1, point2 = self.check_horiz(objects, x, y)
        if not (point1 is None) and not(objects[point1] == 'empty')\
                or not (point2 is None) and not(objects[point2] == 'empty'):
            delete_shot.append(self)
            add_delete_point(point1, delete_point, objects)
            add_delete_point(point2, delete_point, objects)
        return delete_shot, delete_point

    def check_collision_with_enemy(self, shots, enemy_list, player):
        if self.owner == 1:
            return shots
        for enemy in enemy_list:
            if self.__contains_in_point(enemy):
                enemy.alive = False
                player.score += 100
                player.count_enemies_killed += 1
                if not (self in shots):
                    shots.append(self)
        return shots

    def check_collision_with_shot(self, del_shot, shots_list):
        for shot in shots_list:
            if self.__contains_in_point(shot) and not (shot == self) and not(shot in del_shot):
                del_shot.append(shot)
                del_shot.append(self)
        return del_shot

    def check_collision_with_player(self, player):
        if self.owner == 1 and self.__contains_in_point(player):
            player.hp -= 1

    def round(self, y):
        if self.angle % 270 == 0:
            y = math.floor(y)
        else:
            y = math.ceil(y)
        return y

    def check_vert(self, map_objects, x, y):
        point1, point2 = None, None
        if self.contains(map_objects, math.ceil(x), y):
            point1 = Point(math.ceil(x), y)
        if self.contains(map_objects, x + self.size, y):
            point2 = Point(x + self.size, y)
        return point1, point2

    def check_horiz(self, map_objects, x, y):
        point1, point2 = None, None
        if self.contains(map_objects, x, math.ceil(y)):
            point1 = Point(x, math.ceil(y))
        if self.contains(map_objects, x, y + self.size):
            point2 = Point(x, y + self.size)
        return point1, point2

    def contains(self, objects, x, y):
        if Point(x, y) in objects:
            return True
        return False

    def __contains_in_point(self, tile):
        return lies_in_tile(tile, self) or lies_in_tile(self, tile)

    def find_collision(self, level, player, delete_shot, delete_point_p):
        if self.position.X < -1 or self.position.X > level.width or \
                self.position.Y < -1 or self.position.Y > level.height:
            delete_shot.append(self)
            return delete_shot, delete_point_p
        delete_shot, delete_point_p = self.check_collision_with_obj(delete_shot, delete_point_p, level.map_objects)
        delete_shot = self.check_collision_with_enemy(delete_shot, level.enemy_list, player)
        self.check_collision_with_player(player)
        delete_shot = self.check_collision_with_shot(delete_shot, level.shot_list)
        return delete_shot, delete_point_p


def lies_in_tile(tile1, tile2):
    return tile1.position.X <= tile2.position.X <= tile1.position.X + tile1.size and \
           tile1.position.Y <= tile2.position.Y <= tile1.position.Y + tile1.size


def add_delete_point(point, delete_point, objects):
    if point is None:
        return
    if not (objects[point] == 'stone'):
        delete_point.append(point)
