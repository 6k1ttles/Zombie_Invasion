import pygame
from config import *
from media import background


# стартовое окно
def start_screen():
    pygame.mixer.music.load('sounds/background_music.mp3')
    pygame.mixer.music.set_volume(0.1)

    pygame.mixer.music.play(-1)
    fon = pygame.transform.scale(background, SIZE)
    screen = pygame.display.set_mode(SIZE)
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 80)
    text = font.render('Zombie Invasion', True, LIGHTNING_RED)
    text_rect = text.get_rect(center=(WIDTH // 2, 150))

    font1 = pygame.font.Font(None, 50)
    text1 = font1.render('Нажмите "Enter", чтобы начать', True, WHITE)
    text1_rect = text1.get_rect(center=(WIDTH // 2, 600))

    blink_timer = pygame.time.get_ticks()
    blink_duration = 1000
    cont = True

    try:
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    cont = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    cont = False
                    run = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    run = False
                    cont = True
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
        pygame.display.quit()
    return cont
