import random
import math
import game_framework
import game_world
import play_mode
from pico2d import *

# cat Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 25.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

ANIMATION_SPEED_KMPH = 3.0  # Km / Hour
ANIMATION_SPEED_MPM = (ANIMATION_SPEED_KMPH * 1000.0 / 60.0)
ANIMATION_SPEED_MPS = (ANIMATION_SPEED_MPM / 60.0)
ANIMATION_SPEED_PPS = (ANIMATION_SPEED_MPS * PIXEL_PER_METER)

# cat Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
CONFINED_FRAMES_PER_ACTION = 2.0
FREE_FRAMES_PER_ACTION = 3.0
class Cat:
    vaild_cat_idx = []
    images_first_cat = None
    images_second_cat = None
    images_third_cat = None
    images_fourth_cat = None
    def load_images(self):
        if Cat.images_first_cat == None:
            Cat.images_first_cat = load_image("image/cat_1.png")
        if Cat.images_second_cat == None:
            Cat.images_second_cat = load_image("image/cat_2.png")
        if Cat.images_third_cat == None:
            Cat.images_third_cat = load_image("image/cat_3.png")
        if Cat.images_fourth_cat == None:
            Cat.images_fourth_cat = load_image("image/cat_4.png")


    # 0 그린 1 블루 2레드
    def __init__(self,num,type):
        self.type = int(type) #random.randint(0,2)
        self.x = random.randint(800 * num + 850, 800 * num + 1200)
        self.y = random.randint(100, 500)
        self.load_images()
        self.frame = 0
        self.scale = 50
        self.animation = True
        self.animation_moved = 0
        self.confined = True

    def update(self):



        if(self.confined):
            self.frame = (self.frame + CONFINED_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % CONFINED_FRAMES_PER_ACTION

            self.x -= RUN_SPEED_PPS * game_framework.frame_time
            if self.x < -50:
                game_world.remove_object(self)

        else:
            self.frame = (self.frame + FREE_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FREE_FRAMES_PER_ACTION
            for i in range(len(Cat.vaild_cat_idx)):
                if Cat.vaild_cat_idx[i] == self.type:
                    self.y = (play_mode.witch.y - 30) - 30 * i +self.animation_moved
                    self.x = (play_mode.witch.x - 80) - 40 * i +self.animation_moved


        if self.animation == True:
            self.y += ANIMATION_SPEED_PPS * game_framework.frame_time
            self.animation_moved += ANIMATION_SPEED_PPS * game_framework.frame_time
            if self.animation_moved >= 3:
                self.animation = False
        else:
            self.y -= ANIMATION_SPEED_PPS * game_framework.frame_time
            self.animation_moved -= ANIMATION_SPEED_PPS * game_framework.frame_time
            if self.animation_moved <= -3:
                self.animation = True

    def draw(self):
        if self.confined:
            if  self.type == 0:
                Cat.images_first_cat.clip_draw(int(self.frame+1) * 145, 0, 145, 180, self.x, self.y,self.scale, self.scale)
                draw_rectangle(*self.get_bb())
            elif self.type == 1:
                Cat.images_second_cat.clip_draw(int(self.frame+1) * 155, 0, 155, 171, self.x, self.y, self.scale, self.scale)
                draw_rectangle(*self.get_bb())
            elif self.type == 2:
                Cat.images_third_cat.clip_draw(int(self.frame + 1) * 150, 0, 150, 169, self.x, self.y, self.scale,self.scale)
                draw_rectangle(*self.get_bb())
            elif self.type == 3 :
                Cat.images_fourth_cat.clip_draw(int(self.frame + 1) * 147, 0, 147, 189, self.x, self.y, self.scale,self.scale)
                draw_rectangle(*self.get_bb())
        else:
            if self.type == 0:
                Cat.images_first_cat.clip_draw(int(self.frame) * 145, 180, 145, 180, self.x, self.y, self.scale,
                                               self.scale)
                draw_rectangle(*self.get_bb())
            elif self.type == 1:
                Cat.images_second_cat.clip_draw(int(self.frame) * 155, 171, 155, 171, self.x, self.y, self.scale,
                                                self.scale)
                draw_rectangle(*self.get_bb())
            elif self.type == 2:
                Cat.images_third_cat.clip_draw(int(self.frame) * 150, 169, 150, 169, self.x, self.y, self.scale,
                                               self.scale)
                draw_rectangle(*self.get_bb())
            elif self.type == 3:
                Cat.images_fourth_cat.clip_draw(int(self.frame) * 147, 189, 147, 189, self.x, self.y, self.scale,
                                                self.scale)
                draw_rectangle(*self.get_bb())
    def handle_event(self, event):
        pass
    def handle_collision(self,group, other):
        if group == 'witch:cat':
            if self.type == 0: Cat.vaild_cat_idx.append(0)
            elif self.type == 1: Cat.vaild_cat_idx.append(1)
            elif self.type == 2: Cat.vaild_cat_idx.append(2)
            elif self.type == 3: Cat.vaild_cat_idx.append(3)
            self.confined = False
            self.frame = 0
            game_world.remove_collision_object(self)

    def get_bb(self):
        return self.x - 30, self.y - 35, self.x + 30, self.y+35

