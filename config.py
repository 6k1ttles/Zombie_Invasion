# размеры блока
BLOCK_SIZE = 25

FPS = 200

# количество жизней игрока
PLAYER_HP = 100

# скорость игрока
PLAYER_SPEED = 0.5

# размеры игрока
PLAYER_WIDTH = 75
PLAYER_HEIGHT = 75
PLAYER_SIZE = PLAYER_WIDTH, PLAYER_HEIGHT

# урон игрока
PLAYER_DAMAGE = 5

ENEMY_SPEED = 1
ENEMY_HP = 500

ATTACK_WIDTH, ATTACK_HEIGHT = 100, 20

# размеры экрана
SIZE = WIDTH, HEIGHT = 800, 800

# коэффициент интерполяции - плавность следования камеры за игроком.
INTERP_COEFFICIENT = 0.5  # Чем больше,тем резче и быстрее камера

# точка появления игрока
SPAWN_PLACE_PLAYER = [(100 * BLOCK_SIZE) / 2, (100 * BLOCK_SIZE) / 2]  # "100" - ширина поля в символах
SPAWN_PLACE_ENEMY = [(100 * BLOCK_SIZE) / 2, (100 * BLOCK_SIZE) / 2 - 500]  # "100" - ширина поля в символах

# цвета
LIGHTNING_RED = (250, 20, 40)
WHITE = (255, 255, 255)

