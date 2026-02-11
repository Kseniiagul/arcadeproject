import arcade
from src import constants


class IceCube(arcade.Sprite):
    def __init__(self, skin_filename="player.png"):
        target_scale = constants.PLAYER_SCALE
        for skin in constants.AVAILABLE_SKINS:
            if skin["file"] == skin_filename:
                target_scale = skin.get("game_scale", constants.PLAYER_SCALE)
                break
        super().__init__(scale=target_scale)
        self.start_scale = target_scale
        self.death_scale = self.start_scale * 0.25
        try:
            self.texture = arcade.load_texture(f"assets/images/{skin_filename}")
        except:
            print(f"Ошибка загрузки: {skin_filename}")
            self.texture = arcade.make_soft_square_texture(64, arcade.color.WHITE)
        self.center_x = constants.PLAYER_START_X
        self.center_y = constants.PLAYER_START_Y
        self.melt_rate = 0.0003
        self.heal_amount = 0.15

    def update(self, delta_time):
        current_size = self.scale[0]
        new_size = current_size - self.melt_rate
        if new_size < 0: new_size = 0
        self.scale = new_size
        if self.left < 0: self.left = 0

    def setup_difficulty(self, settings):
        self.melt_rate = settings["MELT_RATE"]
        ratio = self.start_scale / constants.PLAYER_SCALE
        self.heal_amount = settings["LIGHT_HEAL"] * ratio

    def heal(self):
        current_size = self.scale[0]
        new_size = current_size + self.heal_amount
        if new_size > self.start_scale:
            new_size = self.start_scale
        self.scale = new_size
