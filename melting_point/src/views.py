import arcade
from src import constants


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


class SkinSelectionView():
    pass
