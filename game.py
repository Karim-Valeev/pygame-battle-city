import os
import pygame
import time as t

from entities.level import Level, Point
from entities.player import Player
from entities.status_bar import StatusBar
from entities.menu import Menu
from entities.ending_screen import EndingScreen
from entities.enemy import Enemy

FPS = 40

WIN_WIDTH = 650
WIN_HEIGHT = 700

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
RED = (255, 0, 0)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    game_started, next_level = False, False
    level_count, max_level_count = 1, 3
    player = Player(8, 24)
    all_hp = player.hp
    while True:
        if level_count > max_level_count:
            game_started = False
            level_count = 1
        status_frame = pygame.Rect(0, 0, 650, 50)
        pygame.draw.rect(screen, WHITE, status_frame, 3)
        if game_started:
            level = Level('%s.txt' % level_count)
            next_level = False
            motion, player_event = False, None
            point_buff = []
            enemy_spawn_timer = t.time()
            while True:
                global_timer = t.time()
                screen.fill(BLACK)

                check_enemy_alive(level, player)
                if t.time() - enemy_spawn_timer > 2.5 and (
                        len(level.enemy_list) < 4) and (len(level.enemy_list) + player.count_enemies_killed < 10):
                    enemy_spawn_timer = t.time()
                    add_enemy_and_update_time(level, player)

                game_started, level_count = update_player_score(level, player, screen, level_count, max_level_count)

                if not game_started:
                    if level.check_eagle() and player.hp > 0 and level_count <= max_level_count:
                        next_level = True
                        player.count_enemies_killed = 0
                        player.position = Point(8, 24)
                    else:
                        player = Player(8, 24)
                    break

                sb = StatusBar(screen, player)
                sb.draw()

                # ToDo разобраться со стрельбой
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            player.move(event, level, global_timer)
                            continue
                        motion = True
                        player_event = event
                    elif event.type == pygame.KEYUP:
                        motion = False

                for enemy in level.enemy_list:
                    point = Point(enemy.position.X, enemy.position.Y)
                    level.add_none_point(point, point_buff)

                if motion:
                    player.move(player_event, level, global_timer)

                for i in range(len(level.enemy_list)):
                    cur_enemy = level.enemy_list[i]
                    cur_enemy.move(global_timer, level, 0, player)
                    point = Point(cur_enemy.position.X, cur_enemy.position.Y)
                    level.add_none_point(point, point_buff)

                for point in point_buff:
                    level.delete_point(point)
                point_buff = []

                level.blit_map(screen, player)
                pygame.display.update()
                clock.tick(FPS)
        else:
            if next_level:
                print('You are now on level', str(level_count) + '!')
                game_started = True
            else:
                # Menu launches if game ended or not started
                sb = StatusBar(screen)
                menu = Menu(screen, sb)
                game_started = menu.start()
                player.hp = all_hp

        pygame.display.update()

        # Возможно не надо
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()

        clock.tick(FPS)


def add_enemy_and_update_time(level, player):
    point = level.get_free_spawn_position(player)
    level.enemy_list.append(Enemy(point.X, point.Y))
    print('Enemy appeared')


def update_player_score(level, player, screen, level_count, max_level_count):
    eagle_is_alive = level.check_eagle()
    flag = True

    if player.count_enemies_killed == 10:
        if level_count >= max_level_count:
            end = EndingScreen(screen, True, player.score)
            end.start()
            level_count = max_level_count + 1
        else:
            level_count += 1
        flag = False

    elif not eagle_is_alive or player.hp == 0:
        end = EndingScreen(screen, False, player.score)
        end.start()
        level_count = max_level_count + 1
        flag = False

    elif 0 < player.hp < level.hp_counter:
        player.position = Point(8, 24)
        level.hp_counter -= 1
        flag = True
    return flag, level_count


def check_enemy_alive(level, player):
    i = len(level.enemy_list)
    while i != 0:
        if not level.enemy_list[i - 1].alive:
            # player.count_enemies_killed += 1
            del level.enemy_list[i - 1]
            print('Enemy died')
        i -= 1


if __name__ == '__main__':
    main()
