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


class DifficultyView(arcade.View):
    def __init__(self):
        super().__init__()
        self.selected_skin = "player.png"

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()
        arcade.draw_text("СЛОЖНОСТЬ", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 + 100,
                         arcade.color.WHITE, 40, anchor_x="center", bold=True)

        arcade.draw_text("1 - ЛЕГКО", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 30,
                         constants.DIFFICULTY_SETTINGS["EASY"]["COLOR"], 18, anchor_x="center")
        arcade.draw_text("2 - НОРМАЛЬНО", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 70,
                         constants.DIFFICULTY_SETTINGS["MEDIUM"]["COLOR"], 18, anchor_x="center")
        arcade.draw_text("3 - СЛОЖНО", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 110,
                         constants.DIFFICULTY_SETTINGS["HARD"]["COLOR"], 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.KEY_1 or key == arcade.key.NUM_1:
            self.start_game("EASY")
        elif key == arcade.key.KEY_2 or key == arcade.key.NUM_2:
            self.start_game("MEDIUM")
        elif key == arcade.key.KEY_3 or key == arcade.key.NUM_3:
            self.start_game("HARD")

    def start_game(self, difficulty_key):
        game_view = GameView()
        game_view.difficulty_preset = constants.DIFFICULTY_SETTINGS[difficulty_key]
        game_view.player_skin = self.selected_skin
        game_view.setup()
        self.window.show_view(game_view)


class GameOverView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text("ТЫ РАСТАЯЛ...", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2, arcade.color.RED, 50,
                         anchor_x="center")
        arcade.draw_text("Клик для меню", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 50,
                         arcade.color.WHITE, 20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.show_view(MenuView())


class VictoryView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.FOREST_GREEN)

    def on_draw(self):
        self.clear()
        arcade.draw_text("ПОБЕДА!", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2, arcade.color.GOLD, 50,
                         anchor_x="center")
        arcade.draw_text("Клик для меню", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 50,
                         arcade.color.WHITE, 20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.show_view(MenuView())


class GameView():
    pass
