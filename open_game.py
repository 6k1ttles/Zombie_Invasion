import pygame
from media import background, player_images_right, player_images_left, player_images_stand, textures
from config import *
from player import Player
from enemy import Enemy
from level import Level
from logg import log_time
from final_window import final_show
from start_window import start_screen
from cheat_console import cheats_mode


def main():
    pygame.init()
    log_time()
    pygame.display.init()
    cont = start_screen()
    if cont:
        pygame.mixer.music.load('sounds/background_battle.mp3')
        pygame.mixer.music.set_volume(0.1)

        screen = pygame.display.set_mode(SIZE)
        clock = pygame.time.Clock()

        player = Player(screen, player_images_right, player_images_left, player_images_stand)
        enemies = pygame.sprite.Group()
        for _ in range(5):
            enemy = Enemy(screen, player)
            enemies.add(enemy)
        camera = pygame.Rect(0, 0, WIDTH, HEIGHT)

        level = Level(screen, textures)
        pygame.mixer.music.play(-1)

        run = True
        paused = False
        paused_timer = False

        i = 5
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    paused = not paused

                # к сожалению, не работает
                # if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                #     paused = not paused
                #     cheats_mode(player)

            delta_time = clock.tick(FPS) * player.speed

            if not paused:
                if paused_timer:
                    i -= 1
                if i <= 0:
                    paused = True
                screen.blit(background, (-camera.x / 4, -camera.y / 4))

                player.update(delta_time, level.update(scroll=[camera.x, camera.y]), (camera.x, camera.y), enemies)

                for enemy in enemies:
                    enemy.update(delta_time, level.update(scroll=[camera.x, camera.y]), (camera.x, camera.y))
                    enemy.draw((camera.x, camera.y))
                    enemy.draw_health_bar((camera.x, camera.y))

                player.draw()

                # Плавная работа камеры
                camera.x += (player.rect.x - camera.x - WIDTH / 2 + player.rect.width / 2) * INTERP_COEFFICIENT
                camera.y += (player.rect.y - camera.y - HEIGHT / 2 + player.rect.height / 2) * INTERP_COEFFICIENT

                player.attack_action(enemies)
                player.draw_health_bar(camera)

                if abs(enemy.rect.x) > 10000 or abs(enemy.rect.y) > 10000:
                    paused_timer = True
                if paused:
                    pygame.mixer.music.stop()
                    final_show()

                pygame.display.update()


