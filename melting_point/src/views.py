import arcade
from src import constants
import arcade.gui


class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()
        arcade.draw_text("MELTING POINT", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 + 50,
                         arcade.color.WHITE, font_size=60, anchor_x="center", bold=True)
        arcade.draw_text("Нажми ENTER, чтобы начать", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 50,
                         arcade.color.LIGHT_BLUE, font_size=20, anchor_x="center")

    def on_key_press(self, key):
        if key == arcade.key.ENTER:
            skin_view = SkinSelectionView()
            self.window.show_view(skin_view)


class SkinSelectionView(arcade.View):
        def __init__(self):
        super().__init__()
        self.selected_index = 0
        self.skins = constants.AVAILABLE_SKINS
        self.ui_sprites = arcade.SpriteList()

        self.preview_sprite = arcade.Sprite()
        self.preview_sprite.center_x = constants.SCREEN_WIDTH / 2
        self.preview_sprite.center_y = constants.SCREEN_HEIGHT / 2 + 80

        self.ui_sprites.append(self.preview_sprite)

        self.update_preview()

    def update_preview(self):
        skin_data = self.skins[self.selected_index]
        filename = skin_data["file"]

        target_scale = skin_data.get("menu_scale", 0.5)

        try:
            self.preview_sprite.texture = arcade.load_texture(f"assets/images/{filename}")
            self.preview_sprite.scale = target_scale
        except:
            self.preview_sprite.texture = arcade.make_soft_square_texture(64, arcade.color.WHITE)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.SLATE_GRAY)

    def on_draw(self):
        self.clear()

        arcade.draw_text("ВЫБЕРИ ПЕРСОНАЖА", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT - 100,
                         arcade.color.WHITE, 30, anchor_x="center", bold=True)

        self.ui_sprites.draw()

        skin_name = self.skins[self.selected_index]["name"]
        arcade.draw_text(f"< {skin_name} >", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 100,
                         arcade.color.GOLD, 25, anchor_x="center", bold=True)

        arcade.draw_text("Стрелки влево/вправо для выбора", constants.SCREEN_WIDTH / 2,
                         constants.SCREEN_HEIGHT / 2 - 150,
                         arcade.color.WHITE, 15, anchor_x="center")
        arcade.draw_text("ENTER - Подтвердить", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 200,
                         arcade.color.GREEN, 15, anchor_x="center")

    def on_key_press(self, key):
        if key == arcade.key.RIGHT:
            self.selected_index += 1
            if self.selected_index >= len(self.skins):
                self.selected_index = 0
            self.update_preview()

        elif key == arcade.key.LEFT:
            self.selected_index -= 1
            if self.selected_index < 0:
                self.selected_index = len(self.skins) - 1
            self.update_preview()

        elif key == arcade.key.ENTER:
            chosen_skin_file = self.skins[self.selected_index]["file"]
            diff_view = DifficultyView()
            diff_view.selected_skin = chosen_skin_file
            self.window.show_view(diff_view)


def DifficultyView():
    pass
