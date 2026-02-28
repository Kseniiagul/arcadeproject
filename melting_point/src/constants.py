SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Melting Point"

AVAILABLE_SKINS = [
    {
        "name": "Классика",
        "file": "player.png",
        "game_scale": 0.3,
        "menu_scale": 0.5
    },
    {
        "name": "Слизень",
        "file": "player_slime.png",
        "game_scale": 0.2,
        "menu_scale": 0.3
    },
    {
        "name": "Кристалл",
        "file": "player_pink.png",
        "game_scale": 0.2,
        "menu_scale": 0.3
    }
]

DIFFICULTY_SETTINGS = {
    "EASY": {
        "LABEL": "ЛЕГКО",
        "COLOR": arcade.color.LIGHT_GREEN,
        "MELT_RATE": 0.0001,  # скорость таяния (здесь медленно)
        "FIRE_CHANCE": 0.10,
        "FIRE_DAMAGE": 0.02,
        "LIGHT_HEAL": 0.20,
        "SAFE_ZONE": 300  # безопасные зоны (здесь длинные)
    },
    "MEDIUM": {
        "LABEL": "НОРМАЛЬНО",
        "COLOR": arcade.color.YELLOW,
        "MELT_RATE": 0.0003,
        "FIRE_CHANCE": 0.20,
        "FIRE_DAMAGE": 0.05,
        "LIGHT_HEAL": 0.15,
        "SAFE_ZONE": 150
    },
    "HARD": {
        "LABEL": "СЛОЖНО",
        "COLOR": arcade.color.RED_DEVIL,
        "MELT_RATE": 0.0007,
        "FIRE_CHANCE": 0.35,
        "FIRE_DAMAGE": 0.10,
        "LIGHT_HEAL": 0.10,
        "SAFE_ZONE": 100
    }
}

# платформы
TILE_SCALING = 0.5
TILE_OVERLAP = 10  # нахлест друг на друга, чтобы не было щелей

# финиш
FRIDGE_SCALING = 0.8
GOAL_X = 2000  # финиш (координата)

# огонь
FIRE_SCALING = 0.07
FIRE_COUNT = 5
FIRE_DAMAGE = 0.05

# снежинки (бонусы)
LIGHT_SCALING = 0.3
LIGHT_HEAL = 0.15

# настройки игрока
PLAYER_SPEED = 5
PLAYER_SCALE = 0.3
PLAYER_START_X = 100
PLAYER_START_Y = 300

BG_COLOR = arcade.csscolor.CORNFLOWER_BLUE
PLAYER_COLOR = arcade.color.CYAN

# физика
GRAVITY = 1.0
PLAYER_JUMP_SPEED = 20

# таяние
MELT_RATE = 0.0003
MIN_SCALE = 0.1
MAX_SCALE = 0.3
