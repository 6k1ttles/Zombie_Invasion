import pygame as pg

from config import *


class Player(pg.sprite.Sprite):
    def __init__(self, sc, player_images_r, player_images_l, player_images_stand):
        super().__init__()
        self.delta_time = None
        self.screen = sc
        self.images_right = player_images_r
        self.images_left = player_images_l
        self.images_stand = player_images_stand
        self.health = PLAYER_HP
        self.speed = PLAYER_SPEED

        self.movement = [0, 0]
        self.rect = pg.Rect(0, 0, PLAYER_WIDTH * 0.75, PLAYER_HEIGHT)

        self.rect.topleft = SPAWN_PLACE_PLAYER

        self.anim_count = 0
        self.is_run = False

        self.dir_x = 1
        self.scroll_x = 0
        self.scroll_y = 0
        self.attack = False
        self.attack_anim_count = 0
        self.weapon_timer = 0

        self.rect_weapon = pg.Rect(self.rect.x + self.rect.width,
                                   self.rect.y + self.rect.height / 2,
                                   ATTACK_WIDTH, ATTACK_HEIGHT)

    # прорисовка атаки
    def draw_attack(self):
        if self.dir_x > 0:
            weapon_x = self.rect.x + self.rect.width
            weapon_y = self.rect.y + self.rect.height / 2 - ATTACK_HEIGHT / 2
        else:
            weapon_x = self.rect.x - ATTACK_WIDTH
            weapon_y = self.rect.y + self.rect.height / 2 - ATTACK_HEIGHT / 2

        self.rect_weapon = pg.Rect(weapon_x, weapon_y,
                                   ATTACK_WIDTH, ATTACK_HEIGHT)

        pg.draw.rect(self.screen, (255, 0, 0), pg.draw.rect(self.screen, (255, 0, 0), (
            weapon_x - self.scroll_x, weapon_y - self.scroll_y, ATTACK_WIDTH,
            ATTACK_HEIGHT)))

        self.weapon_timer += self.delta_time
        if self.weapon_timer >= 1000.0:  # Weapon visibility duration is 1 second
            self.attack = False
            self.weapon_timer = 0

    # прорисовка полоски жизни
    def draw_health_bar(self, camera):
        health_bar_width, health_bar_height = PLAYER_WIDTH * 0.75, PLAYER_HEIGHT * 0.1
        health_percentage = 100

        health_bar_x = self.rect.x + (self.rect.width - health_bar_width) / 2 - camera.x + PLAYER_WIDTH * 0.2
        health_bar_y = self.rect.y - health_bar_height - 5 - camera.y

        pg.draw.rect(self.screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        fill_width = (health_percentage / 100) * health_bar_width
        pg.draw.rect(self.screen, (0, 255, 0), (health_bar_x, health_bar_y, fill_width, health_bar_height))

    # прорисовка анимация с учетом направления движения
    def draw(self):
        self.anim_count %= 500
        if self.is_run:
            if self.movement[0] > 0:
                self.screen.blit(self.images_right[int(self.anim_count * 0.001 * 8)],
                                 (self.rect.x - self.scroll_x, self.rect.y - self.scroll_y))
                self.dir_x = 1
            elif self.movement[0] < 0:
                self.screen.blit(self.images_left[int(self.anim_count * 0.001 * 8)],
                                 (self.rect.x - self.scroll_x, self.rect.y - self.scroll_y))
                self.dir_x = -1
            elif self.movement[1] > 0:
                if self.dir_x > 0:
                    self.screen.blit(self.images_right[int(self.anim_count * 0.001 * 8)],
                                     (self.rect.x - self.scroll_x, self.rect.y - self.scroll_y))
                if self.dir_x < 0:
                    self.screen.blit(self.images_left[int(self.anim_count * 0.001 * 8)],
                                     (self.rect.x - self.scroll_x, self.rect.y - self.scroll_y))
            elif self.movement[1] < 0:
                if self.dir_x > 0:
                    self.screen.blit(self.images_right[int(self.anim_count * 0.001 * 8)],
                                     (self.rect.x - self.scroll_x, self.rect.y - self.scroll_y))
                if self.dir_x < 0:
                    self.screen.blit(self.images_left[int(self.anim_count * 0.001 * 8)],
                                     (self.rect.x - self.scroll_x, self.rect.y - self.scroll_y))
        else:
            if self.dir_x > 0:
                self.screen.blit(self.images_stand[0],
                                 (self.rect.x - self.scroll_x, self.rect.y - self.scroll_y))
            if self.dir_x < 0:
                self.screen.blit(self.images_stand[1],
                                 (self.rect.x - self.scroll_x, self.rect.y - self.scroll_y))

        if self.attack:
            self.draw_attack()

    def update_attack(self):
        if self.attack:
            self.attack_anim_count += self.delta_time / 0.2
        else:
            self.weapon_timer = 0

    # нанесение урона
    def attack_action(self, enemies):
        keys = pg.key.get_pressed()
        space = keys[pg.K_SPACE]
        if space and not self.attack:
            self.attack = True
            self.attack_anim_count = 0

        for enemy in enemies:
            if self.rect_weapon.colliderect(enemy.rect):
                enemy.take_damage(PLAYER_DAMAGE)

    # обновление
    def update(self, delta_time, blocks, scroll, enemies):
        self.scroll_x, self.scroll_y = scroll[0], scroll[1]
        self.delta_time = delta_time
        self.change_dir()
        self.anim_count += delta_time / self.speed
        self.physics(blocks)

        self.attack_action(enemies)
        self.update_attack()

        if self.attack:
            self.draw_attack()
            self.update_attack()

    # движение игрока
    def change_dir(self):
        keys = pg.key.get_pressed()
        a = keys[pg.K_a]
        d = keys[pg.K_d]
        w = keys[pg.K_w]
        s = keys[pg.K_s]
        if a and not d:
            self.movement[0] = -1
            self.is_run = True
        if d and not a:
            self.movement[0] = 1
            self.is_run = True
        if w and not s:
            self.movement[1] = -1
            self.is_run = True
        if s and not w:
            self.movement[1] = 1
            self.is_run = True
        if (not a) and (not d) and (not w) and (not s):
            self.is_run = False
            self.movement = [0, 0]

    # взаимодействие с объектами
    def physics(self, blocks):
        self.rect.x += self.movement[0] * self.delta_time
        collide = self.get_collision(blocks)
        for col in collide:
            if self.movement[0] > 0:
                self.rect.right = col.left
            elif self.movement[0] < 0:
                self.rect.left = col.right

        self.rect.y += self.movement[1] * self.delta_time
        collide = self.get_collision(blocks)
        for col in collide:
            if self.movement[1] > 0:
                self.rect.bottom = col.top
            elif self.movement[1] < 0:
                self.rect.top = col.bottom

    def get_collision(self, blocks):
        collide = []
        for col in blocks:
            if self.rect.colliderect(col):
                collide.append(col)
        return collide
