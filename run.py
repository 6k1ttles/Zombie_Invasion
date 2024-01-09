import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
GROUND_COLOR = (139, 69, 19)
WALL_COLOR = (169, 169, 169)
PLAYER_COLOR = (255, 0, 0)
UNARMED_ENEMY_COLOR = (0, 255, 0)
ARMED_ENEMY_COLOR = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Game")

player_size = 25
player_x = random.randint(0, WIDTH - player_size)
player_y = random.randint(0, HEIGHT - player_size)
player_speed = 5

count_enemy = 5
count_enemy1 = 2

enemy_size = 25
unarmed_enemy_speed = 3
armed_enemy_speed = 3
bullet_speed = 5
bullet_width = 5
bullet_height = 10

wall_width = 20
wall_height = 20
min_wall_distance = player_size + 50


def terminate():
    pygame.quit()
    sys.exit()


def load_level_from_file(filename):
    with open(filename, 'r') as file:
        level_data = [line.strip() for line in file]
    return level_data


walls = []
level_filename = 'data/map.txt'
level_data = load_level_from_file(level_filename)

for y, row in enumerate(level_data):
    for x, cell in enumerate(row):
        if cell == '#':
            walls.append((x * wall_width, y * wall_height))


def create_unarmed_enemy():
    enemy_x = random.randint(0, WIDTH - enemy_size)
    enemy_y = random.randint(0, HEIGHT - enemy_size)
    return UnarmedEnemy(enemy_x, enemy_y)


def create_armed_enemy():
    enemy_x = random.randint(0, WIDTH - enemy_size)
    enemy_y = random.randint(0, HEIGHT - enemy_size)
    return ArmedEnemy(enemy_x, enemy_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((player_size, player_size))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 100
        self.weapon_cooldown = 1000
        self.last_weapon_time = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_weapon_time >= self.weapon_cooldown:
            if keys[pygame.K_SPACE]:
                self.last_weapon_time = now
                weapon = Weapon(self)
                all_sprites.add(weapon)
                weapons.add(weapon)

    def draw_health_bar(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, player_size, 5))
        pygame.draw.rect(screen, (0, 255, 0), (
            self.rect.x + player_size * (1 - self.health / 100), self.rect.y - 10, player_size * (self.health / 100),
            5))


class UnarmedEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((enemy_size, enemy_size))
        self.image.fill(UNARMED_ENEMY_COLOR)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist != 0:
            dx /= dist
            dy /= dist

        if dist > 25:
            new_enemy_x = self.rect.x + dx * unarmed_enemy_speed
            new_enemy_y = self.rect.y + dy * unarmed_enemy_speed

            for wall_x, wall_y in walls:
                if not (wall_x > new_enemy_x + enemy_size or
                        wall_x + wall_width < new_enemy_x or
                        wall_y > new_enemy_y + enemy_size or
                        wall_y + wall_height < new_enemy_y):
                    break
            else:
                self.rect.x = new_enemy_x
                self.rect.y = new_enemy_y


class ArmedEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((enemy_size, enemy_size))
        self.image.fill(ARMED_ENEMY_COLOR)
        self.rect = self.image.get_rect(center=(x, y))
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist != 0:
            dx /= dist
            dy /= dist

        if dist > 75:
            new_enemy_x = self.rect.x + dx * armed_enemy_speed
            new_enemy_y = self.rect.y + dy * armed_enemy_speed

            for wall_x, wall_y in walls:
                if not (wall_x > new_enemy_x + enemy_size or
                        wall_x + wall_width < new_enemy_x or
                        wall_y > new_enemy_y + enemy_size or
                        wall_y + wall_height < new_enemy_y):
                    break
            else:
                self.rect.x = new_enemy_x
                self.rect.y = new_enemy_y

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.centery, dx, dy, is_armed=True)
            all_sprites.add(bullet)
            bullets.add(bullet)


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        weapon_radius = 40
        self.image = pygame.Surface((weapon_radius * 2, weapon_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255, 128), (weapon_radius, weapon_radius), weapon_radius)
        self.rect = self.image.get_rect(center=player.rect.center)
        self.lifespan = 1500
        self.creation_time = pygame.time.get_ticks()

    def update(self):
        global count_enemy
        global count_enemy1
        c_enemy = count_enemy
        c_enemy1 = count_enemy1

        now = pygame.time.get_ticks()
        if now - self.creation_time >= self.lifespan:
            self.kill()
        else:
            hits_unarmed = pygame.sprite.spritecollide(self, unarmed_enemies, True)
            c_enemy -= len(hits_unarmed)
            spawn_rand(abs(count_enemy - c_enemy))

            hits_armed = pygame.sprite.spritecollide(self, armed_enemies, True)
            c_enemy1 -= len(hits_armed)
            spawn_rand(abs(count_enemy1 - c_enemy1))

            hits_bullets = pygame.sprite.spritecollide(self, bullets, True)
            for bullet in hits_bullets:
                bullet.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, is_armed=False):
        super().__init__()
        self.image = pygame.Surface((bullet_width, bullet_height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx * bullet_speed
        self.dy = dy * bullet_speed
        self.is_ranged = is_armed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        for wall_x, wall_y in walls:
            if not (wall_x > self.rect.x + bullet_width or
                    wall_x + wall_width < self.rect.x or
                    wall_y > self.rect.y + bullet_height or
                    wall_y + wall_height < self.rect.y):
                self.kill()
                return

        if self.is_ranged and pygame.sprite.collide_rect(self, player):
            player.health -= 5
            if player.health <= 0:
                terminate()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        return obj.rect.move(self.dx, self.dy)

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.width // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.height // 2 - HEIGHT // 2)


bullets = pygame.sprite.Group()
weapons = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
player = Player(player_x, player_y)
all_sprites.add(player)
all_sprites.add(weapons)

unarmed_enemies = pygame.sprite.Group()
armed_enemies = pygame.sprite.Group()


def spawn(k):
    for _ in range(k):
        unarmed_enemy = create_unarmed_enemy()
        unarmed_enemies.add(unarmed_enemy)
        all_sprites.add(unarmed_enemy)


def spawn1(k):
    for _ in range(k):
        armed_enemy = create_armed_enemy()
        armed_enemies.add(armed_enemy)
        all_sprites.add(armed_enemy)


def spawn_rand(k):
    if random.randint(0, 1) == 1:
        spawn(k)
    else:
        spawn1(k)


spawn(count_enemy)
spawn1(count_enemy1)

camera = Camera()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            terminate()
    keys = pygame.key.get_pressed()

    new_player_x = player.rect.x
    new_player_y = player.rect.y

    if keys[pygame.K_a] and player.rect.x > 0:
        new_player_x -= player_speed
    if keys[pygame.K_d] and player.rect.x < WIDTH - player_size:
        new_player_x += player_speed
    if keys[pygame.K_w] and player.rect.y > 0:
        new_player_y -= player_speed
    if keys[pygame.K_s] and player.rect.y < HEIGHT - player_size:
        new_player_y += player_speed

    collision = False
    for wall_x, wall_y in walls:
        if not (wall_x > new_player_x + player_size or
                wall_x + wall_width < new_player_x or
                wall_y > new_player_y + player_size or
                wall_y + wall_height < new_player_y):
            collision = True
            break

    if not collision:
        player.rect.x = new_player_x
        player.rect.y = new_player_y

    all_sprites.update()
    weapons.update()

    camera.update(player)

    screen.fill(GROUND_COLOR)

    for wall_x, wall_y in walls:
        pygame.draw.rect(screen, WALL_COLOR, (wall_x, wall_y, wall_width, wall_height))

    all_sprites.draw(screen)
    player.draw_health_bar()
    pygame.time.Clock().tick(60)

    if pygame.sprite.spritecollide(player, unarmed_enemies, False):
        player.health -= 3
        if player.health <= 0:
            terminate()

    if pygame.sprite.spritecollide(player, armed_enemies, False):
        player.health -= 1
        if player.health <= 0:
            terminate()

    pygame.display.flip()
