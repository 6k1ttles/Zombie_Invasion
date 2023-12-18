import pygame
import os
import sys

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
tile_width = tile_height = 50
pygame.mixer.music.load("data/background_music.mp3")

BLOOD_RED = (150, 0, 0)
LIGHTNING_RED = (250, 20, 40)
WHITE = (255, 255, 255)


def load_image(name, colorkey=None, size=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if size:
        image = pygame.transform.scale(image, size)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    pygame.mixer.music.play(-1)
    fon = pygame.transform.scale(load_image('fon2.png'), size)
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 80)
    text = font.render('Zombie Invasion', True, LIGHTNING_RED)
    text_rect = text.get_rect(center=(width // 2, 150))

    font1 = pygame.font.Font(None, 50)
    text1 = font1.render('Нажмите "Space", чтобы начать', True, WHITE)
    text1_rect = text1.get_rect(center=(width // 2, 600))

    blink_timer = pygame.time.get_ticks()
    blink_duration = 1000

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    pass
            screen.blit(fon, (0, 0))
            screen.blit(text, text_rect)
            screen.blit(text1, text1_rect)

            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - blink_timer
            progress = elapsed_time % (2 * blink_duration) / (2 * blink_duration)
            alpha = int(255 * (1 - abs(2 * progress - 1)))
            text1.set_alpha(alpha)

            pygame.display.flip()
            pygame.time.delay(10)
    except Exception as e:
        print(f'Внимание! Ошибка {e}')
        terminate()


start_screen()
pygame.quit()
