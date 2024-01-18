import pygame as pg
from config import PLAYER_SIZE, BLOCK_SIZE, SIZE

pg.init()
screen = pg.display.set_mode(SIZE)

# images
player_images_right = \
    [pg.transform.scale(pg.image.load('assets/animation/pl_anim1.png'), PLAYER_SIZE),
     pg.transform.scale(pg.image.load('assets/animation/pl_anim2.png'), PLAYER_SIZE),
     pg.transform.scale(pg.image.load('assets/animation/pl_anim3.png'), PLAYER_SIZE),
     pg.transform.scale(pg.image.load('assets/animation/pl_anim4.png'), PLAYER_SIZE)]

player_images_left = \
    [pg.transform.flip(player_images_right[0], True, False),
     pg.transform.flip(player_images_right[1], True, False),
     pg.transform.flip(player_images_right[2], True, False),
     pg.transform.flip(player_images_right[3], True, False)]

player_images_stand = [pg.transform.scale(pg.image.load('assets/animation/pl_0.png'), PLAYER_SIZE),
                       pg.transform.flip(pg.transform.scale(pg.image.load('assets/animation/pl_0.png'),
                                                            PLAYER_SIZE), True, False)]

textures = {'stone': pg.transform.scale(pg.image.load('assets/ground5.png'), (BLOCK_SIZE, BLOCK_SIZE)).convert_alpha(),
            'ground_bottom': pg.transform.scale(pg.image.load('assets/stone.png'),
                                                (BLOCK_SIZE, BLOCK_SIZE)).convert_alpha(),
            # 'ground_top': pg.transform.scale(pg.image.load('assets/clouds.png'), (WIDTH, HEIGHT)).convert_alpha()
            }

background = pg.image.load('assets/background_image.png')
