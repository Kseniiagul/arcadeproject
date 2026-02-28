import arcade
from src import constants
import arcade.gui
import random
from src.player import IceCube


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


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # настройки по умолчанию
        self.difficulty_preset = constants.DIFFICULTY_SETTINGS["MEDIUM"]
        self.player_skin = "player.png"

        self.scene = None
        self.player = None
        self.physics_engine = None
        self.camera = None
        self.gui_camera = None

    def setup(self):
        self.scene = arcade.Scene()
        self.camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        fire_chance = self.difficulty_preset["FIRE_CHANCE"]
        safe_size = self.difficulty_preset["SAFE_ZONE"]
        MAX_JUMP_HEIGHT = 150
        MAX_JUMP_DISTANCE = 250
        self.player = IceCube(self.player_skin)
        self.player.setup_difficulty(self.difficulty_preset)
        self.scene.add_sprite("Player", self.player)
        platform_path = "assets/images/ground.png"
        light_path = "assets/images/light.png"
        fire_path = "assets/images/fire.png"
        fridge_path = "assets/images/fridge.png"
        try:
            texture = arcade.load_texture(platform_path)
            tile_width = texture.width * constants.TILE_SCALING
            tile_height = texture.height * constants.TILE_SCALING
        except:
            texture = arcade.make_soft_square_texture(50, arcade.color.GRAY)
            tile_width = 50 * constants.TILE_SCALING
            tile_height = 50 * constants.TILE_SCALING
        floor_y = tile_height / 2
        floor_top = tile_height
        step = tile_width - constants.TILE_OVERLAP
        if step < 1: 
            step = 1
        num_tiles = int((constants.GOAL_X + 400) / step)
        safe_counter = 400

        for i in range(num_tiles):
            current_x = i * step + (tile_width / 2)
            wall = arcade.Sprite(scale=constants.TILE_SCALING)
            wall.texture = texture
            wall.center_x = current_x
            wall.center_y = floor_y
            self.scene.add_sprite("Walls", wall)
            if safe_counter > 0:
                safe_counter -= step
                continue
            if current_x < constants.GOAL_X - 300 and random.random() < fire_chance:
                try:
                    fire = arcade.Sprite(fire_path, constants.FIRE_SCALING)
                except:
                    fire = arcade.SpriteSolidColor(40, 40, arcade.color.RED)
                fire.center_x = current_x
                fire.bottom = floor_top
                self.scene.add_sprite("Traps", fire)
                safe_counter = safe_size
            elif random.random() < 0.05:
                try:
                    light = arcade.Sprite(light_path, constants.LIGHT_SCALING)
                except:
                    light = arcade.SpriteCircle(15, arcade.color.YELLOW)
                light.center_x = current_x
                light.bottom = floor_top + 10
                self.scene.add_sprite("Coins", light)
                safe_counter = 50

        platform_x = 400
        platform_y = floor_top
        player_height = 64 * constants.PLAYER_SCALE
        req_gap = player_height + 30

        while platform_x < constants.GOAL_X - 300:
            min_gap = tile_width + 20
            max_gap = MAX_JUMP_DISTANCE
            gap = random.randrange(int(min_gap), int(max_gap))
            new_x = platform_x + gap
            min_y = floor_top + 110
            max_y_reach = platform_y + MAX_JUMP_HEIGHT
            max_y_abs = 500
            real_max_y = min(max_y_reach, max_y_abs)
            if real_max_y < min_y:
                new_y = min_y
            else:
                new_y = random.randrange(int(min_y), int(real_max_y))
            platform = arcade.Sprite(scale=constants.TILE_SCALING)
            platform.texture = texture
            platform.center_x = new_x
            platform.center_y = new_y
            self.scene.add_sprite("Walls", platform)
            is_fire_below = False
            if "Traps" in self.scene:
                for trap in self.scene["Traps"]:
                    if abs(trap.center_x - new_x) < tile_width:
                        is_fire_below = True
                        break
            gap = (new_y - tile_height / 2) - floor_top
            pass_under = gap > req_gap
            trap_prob = fire_chance + 0.1
            if (not is_fire_below) and pass_under and (random.random() < trap_prob):
                try:
                    item = arcade.Sprite(fire_path, constants.FIRE_SCALING)
                    layer = "Traps"
                except:
                    item = arcade.SpriteSolidColor(32, 32, arcade.color.RED)
                    layer = "Traps"
            else:
                try:
                    item = arcade.Sprite(light_path, constants.LIGHT_SCALING)
                    layer = "Coins"
                except:
                    item = arcade.SpriteCircle(15, arcade.color.YELLOW)
                    layer = "Coins"
            item.center_x = new_x
            item.bottom = new_y + (tile_height / 2) + 5
            self.scene.add_sprite(layer, item)
            platform_x = new_x
            platform_y = new_y

        try:
            self.goal = arcade.Sprite(fridge_path, constants.FRIDGE_SCALING)
        except:
            self.goal = arcade.SpriteSolidColor(50, 80, arcade.color.GREEN)
        self.goal.center_x = constants.GOAL_X
        self.goal.bottom = floor_top
        self.scene.add_sprite("Goal", self.goal)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, gravity_constant=constants.GRAVITY, walls=self.scene["Walls"])
        arcade.set_background_color(constants.BG_COLOR)

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.scene.update(delta_time=delta_time)
        time = self.window.time

        if "Coins" in self.scene:
            for light in self.scene["Coins"]:
                base = constants.LIGHT_SCALING
                if isinstance(light, arcade.SpriteCircle):
                    base = 1.0
                light.scale = base + (math.sin(time * 5) * 0.1)

        screen_x = self.player.center_x - (self.window.width / 2)
        if screen_x < 0:
            screen_x = 0
        self.camera.bottom_left = (screen_x, 0)

        if self.player.scale[0] < self.player.death_scale:
            view = GameOverView()
            self.window.show_view(view)

        if "Coins" in self.scene:
            hit_list = arcade.check_for_collision_with_list(self.player, self.scene["Coins"])
            for light in hit_list:
                light.remove_from_sprite_lists()
                self.player.heal()

        if "Traps" in self.scene:
            fire_hit_list = arcade.check_for_collision_with_list(self.player, self.scene["Traps"])
            if fire_hit_list:
                current_width = self.player.scale[0]
                damage = self.difficulty_preset["FIRE_DAMAGE"]
                new_size = current_width - damage
                if new_size < 0:
                    new_size = 0
                self.player.scale = new_size

        if arcade.check_for_collision(self.player, self.goal):
            view = VictoryView()
            self.window.show_view(view)

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()

        self.gui_camera.use()

        current_size = self.player.scale[0]

        life_percent = int((current_size / self.player.start_scale) * 100)

        if life_percent < 0: life_percent = 0

        arcade.draw_text(
            f"Life: {life_percent}%",
            10, constants.SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 16, bold=True
        )

        arcade.draw_text(
            f"Mode: {self.difficulty_preset['LABEL']}",
            constants.SCREEN_WIDTH - 150, constants.SCREEN_HEIGHT - 30,
            self.difficulty_preset['COLOR'], 14, bold=True
        )

    def on_key_press(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.W, arcade.key.SPACE] and self.physics_engine.can_jump():
            self.player.change_y = constants.PLAYER_JUMP_SPEED
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.player.change_x = -constants.PLAYER_SPEED
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.player.change_x = constants.PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D]:
            self.player.change_x = 0




