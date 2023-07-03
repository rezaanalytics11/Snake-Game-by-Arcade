import arcade
import random
import os
import time


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


SPRITE_SCALING_STONE = 0.5
STONE_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite with Moving Platforms'
SPRITE_SCALING = 0.5


SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * SPRITE_SCALING)

VIEWPORT_MARGIN = SPRITE_PIXEL_SIZE * SPRITE_SCALING
RIGHT_MARGIN = 4 * SPRITE_PIXEL_SIZE * SPRITE_SCALING

MOVEMENT_SPEED = 10 * SPRITE_SCALING
JUMP_SPEED = 28 * SPRITE_SCALING
GRAVITY = .9 * SPRITE_SCALING

class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Menu Screen", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.all_wall_list = None
        self.static_wall_list = None
        self.moving_wall_list = None
        self.player_list = None
        self.player_sprite = None
        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.end_of_map = 0
        self.time_taken = 0
        self.stone_sprite_list=None
        self.score = 0
        self.start=time.time()
        self.end=time.time()
        self.stone=0
        self.frame_count=0
        self.cacti=0

        self.player_list = arcade.SpriteList()
        self.all_wall_list= arcade.SpriteList()
        self.static_wall_list= arcade.SpriteList()
        self.moving_wall_list = arcade.SpriteList()
        self.stone_sprite_list= arcade.SpriteList()
        self.cacti_sprite_list=arcade.SpriteList()
        self.score_sprite_list=arcade.SpriteList()

        self.score = 0

        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING)
        self.player_list.append(self.player_sprite)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 3 * GRID_PIXEL_SIZE
        self.player_sprite.height = 80
        self.player_sprite.width = 50

        self.gun_sound = arcade.sound.load_sound(":resources:sounds/laser2.wav")
        self.hit_sound = arcade.sound.load_sound(":resources:sounds/explosion2.wav")
        self.jump_sound = arcade.sound.load_sound(":resources:sounds/jump2.wav")
        self.gameover_sound = arcade.sound.load_sound(":resources:sounds/gameover3.wav")


        for i in range(100):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)
            wall.bottom = 0
            wall.center_x = i * GRID_PIXEL_SIZE

            self.static_wall_list.append(wall)
            self.all_wall_list.append(wall)

        self.physics_engine = \
            arcade.PhysicsEnginePlatformer(self.player_sprite,
                                           self.all_wall_list,
                                           gravity_constant=GRAVITY)


    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.player_list.draw()
        self.static_wall_list.draw()
        self.moving_wall_list.draw()
        self.stone_sprite_list.draw()
        self.cacti_sprite_list.draw()



        output = f"Score: {self.score}"
        #arcade.draw_text(output, 10, 30, arcade.color.WHITE, 14)
        output_total = f"Total Score: {self.window.total_score}"
        #arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

        distance = int(self.player_sprite.right)
        output = f"Distance: {distance}"
        arcade.draw_text(output, self.view_left + 10, self.view_bottom + 20,
        arcade.color.WHITE, 14)


    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
                arcade.sound.play_sound(self.jump_sound)
        elif key == arcade.key.DOWN:
                self.player_sprite.height= self.player_sprite.height//2


        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -2*MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 2*MOVEMENT_SPEED


    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        if key == arcade.key.DOWN:
            self.player_sprite.height= 2* self.player_sprite.height



    def on_update(self, delta_time):
        #self.frame_count += 1
        self.time_taken += delta_time
        self.physics_engine.update()
        self.all_wall_list.update()

        if self.time_taken> 50:
         # if self.frame_count % 5 == 0:
         self.stone = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big1.png", SPRITE_SCALING_STONE)
         self.stone.center_x = SCREEN_WIDTH + (200*random.randrange(SCREEN_WIDTH))
         self.stone.center_y = 200
         self.stone_sprite_list.append(self.stone)
         self.stone.change_x -= 8

        for self.stone in self.stone_sprite_list:

          hit_list = arcade.check_for_collision_with_list(self.stone, self.player_list)

          for self.stone in hit_list:
            self.stone.kill()
            self.score =0
            self.window.total_score = 0
            game_over_view = GameOverView()
            game_over_view.time_taken = self.time_taken
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)
            arcade.sound.play_sound(self.hit_sound)
            time.sleep(1.0)
            arcade.sound.play_sound(self.gameover_sound)

        for self.stone in self.stone_sprite_list:
                if self.stone.right < 0:
                    self.stone.remove_from_sprite_lists()

        self.stone_sprite_list.update()

        for i in range(40):
            self.cacti = arcade.Sprite(":resources:images/tiles/spikes.png", 0.5)
            self.cacti_sprite_list.append(self.cacti)
        self.cacti.center_x = (150 * random.randint(2, 30))
        self.cacti.center_y = 95

        for self.cacti in self.cacti_sprite_list:
            hit_list = arcade.check_for_collision_with_list(self.cacti, self.player_list)

            for self.cacti in hit_list:
                self.cacti.kill()
                self.score = 0
                self.score_sprite_list.append(self.score)
                self.window.total_score = 0
                game_over_view = GameOverView()
                game_over_view.time_taken = self.time_taken
                self.window.set_mouse_visible(True)
                self.window.show_view(game_over_view)
                arcade.sound.play_sound(self.hit_sound)
                time.sleep(1.0)
                arcade.sound.play_sound(self.gameover_sound)

        self.cacti_sprite_list.update()


        if (self.player_sprite.right < -39) and (self.player_sprite.top < -39) :
            game_over_view = GameOverView()
            game_over_view.time_taken = self.time_taken
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)
            arcade.sound.play_sound(self.gameover_sound)


        if self.time_taken > 150:
                self.score = 1
                self.window.total_score = 1
                self.score_sprite_list.append(self.score)
                game_over_view = GameWinView()
                game_over_view.time_taken = self.time_taken
                self.window.set_mouse_visible(True)
                self.window.show_view(game_over_view)
                arcade.sound.play_sound(self.gameover_sound)

        changed = False

        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        arcade.draw_text("Game Over", 240, 400, arcade.color.WHITE, 54)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.WHITE, 24)

        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        arcade.draw_text(f"Time taken: {time_taken_formatted}",
                         SCREEN_WIDTH / 2,
                         200,
                         arcade.color.GRAY,
                         font_size=15,
                         anchor_x="center")


        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)



class GameWinView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ORANGE)

    def on_draw(self):
        self.clear()

        arcade.draw_text("Congradulations, You Won !!", 240, 400, arcade.color.WHITE, 40)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.WHITE, 24)

        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        arcade.draw_text(f"Time taken: {time_taken_formatted}",
                         SCREEN_WIDTH / 2,
                         200,arcade.color.GRAY,font_size=15,anchor_x="center")

        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, SCREEN_WIDTH//3, 100, arcade.color.WHITE, 14)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.total_score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()