import pygame as pg
from config import *
from random import randint


class Enemy(pg.sprite.Sprite):
    def __init__(self, sc, player):
        super().__init__()
        self.screen = sc

        self.player = player
        self.rect = pg.Rect(0, 0, PLAYER_WIDTH * 0.75, PLAYER_HEIGHT)
        self.rect.topleft = SPAWN_PLACE_ENEMY
        self.speed = (randint(1, 5) / 10) if ENEMY_SPEED != 0 else ENEMY_SPEED
        self.health = ENEMY_HP

    # прорисовка полоски жизни
    def draw_health_bar(self, scroll):
        health_bar_width, health_bar_height = PLAYER_WIDTH, 5
        health_percentage = max(0, (self.health / ENEMY_HP) * 100)

        health_bar_x = self.rect.x - scroll[0]
        health_bar_y = self.rect.y - scroll[1] - 10

        pg.draw.rect(self.screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        fill_width = (health_percentage / 100) * health_bar_width
        pg.draw.rect(self.screen, (0, 255, 0), (health_bar_x, health_bar_y, fill_width, health_bar_height))

    # прорисовка врага
    def draw(self, scroll):
        pg.draw.rect(self.screen, (0, 0, 255),
                     (self.rect.x - scroll[0], self.rect.y - scroll[1], PLAYER_WIDTH, PLAYER_HEIGHT))

    # получение урона
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.rect.topleft = 222222222, 700

    # обновление
    def update(self, delta_time, blocks, scroll):
        self.move_towards_player(delta_time)
        self.physics(blocks)

    # движение по направлению к игроку
    def move_towards_player(self, delta_time):
        dx = self.player.rect.x - self.rect.x
        dy = self.player.rect.y - self.rect.y
        dist = max(1, ((dx ** 2) + (dy ** 2)) ** 0.5)
        dx /= dist
        dy /= dist

        self.rect.x += dx * self.speed * delta_time
        self.rect.y += dy * self.speed * delta_time

    # взаимодействие с объектами
    def physics(self, blocks):
        self.rect.x += self.speed
        collide = self.get_collision(blocks)
        for col in collide:
            if self.speed > 0:
                self.rect.right = col.left
                self.speed *= -1
            elif self.speed < 0:
                self.rect.left = col.right
                self.speed *= -1

    def get_collision(self, blocks):
        collide = []
        for col in blocks:
            if self.rect.colliderect(col):
                collide.append(col)
        return collide
