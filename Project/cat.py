import random
import math
import game_framework
import game_world
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
TIME_PER_ACTION = 0.8
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2.0

class Cat:
    images_first_cat = None
    images_second_cat = None
    images_red = None
    def load_images(self):
        if Cat.images_first_cat == None:
            Cat.images_first_cat = load_image("image/cat_1.png")
        if Cat.images_second_cat == None:
            Cat.images_second_cat = load_image("image/cat_2.png")
        # if Cat.images_red == None:
        #     Cat.images_red = load_image("image/item_3.png")


    # 0 그린 1 블루 2레드
    def __init__(self,num):
        self.type = 0 #random.randint(0,2)
        self.x = random.randint(800 * num + 850, 800 * num + 1200)
        self.y = random.randint(100, 500)
        self.load_images()
        self.frame = 0
        self.scale = 80
        self.animation = True
        self.animation_moved = 0
        self.confined = True

    def update(self):

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        if(self.confined):
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

            self.x -= RUN_SPEED_PPS * game_framework.frame_time
            if self.x < -50:
                game_world.remove_object(self)

        else:

            pass


    def draw(self):
        if self.confined:
            if self.type == 0:
                Cat.images_first_cat.clip_draw(int(self.frame+1) * 145, 0, 145, 180, self.x, self.y,self.scale, self.scale)
                draw_rectangle(*self.get_bb())
            elif self.type == 1:
                Cat.images_second_cat.clip_draw(int(self.frame+1) * 145, 0, 145, 180, self.x, self.y, self.scale, self.scale)
                draw_rectangle(*self.get_bb())
            else :
                Cat.images_red.clip_draw(int(self.frame)%2 * 256, int(self.frame)// 2, 256, 256, self.x, self.y, self.scale,self.scale)
                draw_rectangle(*self.get_bb())
        else:
            pass
    def handle_event(self, event):
        pass
    def handle_collision(self,group, other):
        if group == 'witch:cat':
            self.confined = False


    def get_bb(self):
        return self.x - 30, self.y - 35, self.x + 30, self.y+35

