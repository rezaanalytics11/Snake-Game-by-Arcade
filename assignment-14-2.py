import arcade
import random

# from player import Player
# from ground import Ground
# from enemy import Enemy
import time
import imageio
import os


class Ground(arcade.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.texture=arcade.load_texture(":resources:images/tiles/grassMid.png")
        self.center_x=x
        self.center_y=y
        self.width=120
        self.height=120


class Box(arcade.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.texture=arcade.load_texture(":resources:images/tiles/grassHalf_mid.png")
        self.center_x=x
        self.center_y=y
        self.width=120
        self.height=120


class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture=arcade.load_texture(":resources:images/animated_characters/female_person/femalePerson_walk3.png")
        self.center_x=random.randint(0,1000)
        self.center_y=400
        self.speed=4
        self.change_x=random.choice([-1,1])

class Player(arcade.AnimatedWalkingSprite):
    def __init__(self):
        super().__init__()
        self.texture=arcade.load_texture(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png")
        self.center_x=100
        self.center_y=200
        self.pocket=[]
        self.speed=4
        self.stand_right_textures=[arcade.load_texture(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png")]
        self.walk_right_textures=[arcade.load_texture(":resources:images/animated_characters/male_adventurer/maleAdventurer_walk0.png"),
                                  arcade.load_texture(":resources:images/animated_characters/male_adventurer/maleAdventurer_walk1.png"),
                                  arcade.load_texture(":resources:images/animated_characters/male_adventurer/maleAdventurer_walk2.png"),
                                  arcade.load_texture(":resources:images/animated_characters/male_adventurer/maleAdventurer_walk3.png"),
                                  arcade.load_texture(":resources:images/animated_characters/male_adventurer/maleAdventurer_walk4.png"),
                                  arcade.load_texture(":resources:images/animated_characters/male_adventurer/maleAdventurer_walk5.png"),
                                  arcade.load_texture(":resources:images/animated_characters/male_adventurer/maleAdventurer_walk6.png"),
                                  arcade.load_texture(":resources:images/animated_characters/male_adventurer/maleAdventurer_walk7.png")
                                  ]


class Game(arcade.Window):
    def __init__(self):
        self.w=1800
        self.h=900
        self.gravity=0.5
        super().__init__(self.w,self.h,'Platformer Game')
        #self.background_image=arcade.load_texture(":resources:images/tiles/stoneMid.png")
        self.me=Player()
        self.t1=time.time()
        self.ground_list=arcade.SpriteList()
        self.enemy_list=arcade.SpriteList()
        self.box_list=arcade.SpriteList()
        self.key=1


        self.key=arcade.Sprite(":resources:images/items/keyRed.png")
        self.key.center_x=1200
        self.key.center_y = 150
        self.key.width=50
        self.key.height=50

        self.lock=arcade.Sprite(":resources:images/items/coinSilver_test.png")
        self.lock.center_x=100
        self.lock.center_y =800


        for i in range (0,1500,120):
            ground= Ground(i,40)
            self.ground_list.append(ground)

        for i in range(400,800,120):
            box=Box(i,250)
            self.ground_list.append(box)

        for i in range(100, 400, 120):
                box = Box(i, 500)
                self.ground_list.append(box)



        self.enemy_physics_engine=arcade.PhysicsEnginePlatformer(self.me,self.ground_list,gravity_constant=0.2)

        self.enemy_physics_engine_list=[]
        for i in range (random.randrange(10)):
            if i%2 ==0 :
             arcade.set_background_color(arcade.color.AMAZON)
            else:
                arcade.set_background_color(arcade.color.BLACK)


    def on_draw(self):
        arcade.start_render()
        #arcade.draw_lrwh_rectangle_textured(0,0,self.w,self.h,self.background_image)
        try:
             self.key.draw()

        except:
              pass



        self.lock.draw()

        self.me.draw()
        for enemy in self.enemy_list:
            enemy.draw()

        for ground in self.ground_list:
            ground.draw()

    def on_update(self, delta_time):
        self.t2 = time.time()
        try:
            if arcade.check_for_collision(self.me,self.key):
             self.me.pocket.append(self.key)
             del self.key

        except:
               pass

        if arcade.check_for_collision(self.me, self.lock) and len(self.me.pocket) == 1:
            print('you are winner)')
            self.lock.texture = arcade.load_texture(":resources:images/items/coinGold_ul.png")


        if self.t2-self.t1 >5:
            new_enemy=Enemy()
            self.enemy_list.append(new_enemy)
            self.enemy_physics_engine_list.append(arcade.PhysicsEnginePlatformer(new_enemy,self.ground_list,0.2))
            self.t1=time.time()

        self.me.update_animation()


        self.enemy_physics_engine.update()

        for item in self.enemy_physics_engine_list:
            item.update()

    def on_key_press(self, key, modifiers):

                if key == arcade.key.UP:
                    if self.enemy_physics_engine.can_jump():
                        self.me.change_y = 10
                elif key == arcade.key.LEFT:
                    self.me.change_x = -1* self.me.speed
                elif key == arcade.key.RIGHT:
                    self.me.change_x = 1* self.me.speed

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.me.change_x = 0



mygame=Game()
arcade.run()
