import random
import math
import game_framework
import game_world
from pico2d import *

# potion Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 25.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# potion Action Speed
TIME_PER_ACTION = 0.8
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4.0

class Potion:
    images_green = None
    images_blue = None
    images_red = None
    def load_images(self):
        if Potion.images_green == None:
            Potion.images_green = load_image("image/item_1.png")
        if Potion.images_blue == None:
            Potion.images_blue = load_image("image/item_2.png")
        if Potion.images_red == None:
            Potion.images_red = load_image("image/item_3.png")


    # 0 그린 1 블루 2레드
    def __init__(self):
        self.type = 2 #random.randint(0,2)
        self.x = random.randint(800 + 850, 800 + 1200)
        self.y = random.randint(100, 500)
        self.load_images()
        self.frame = 0
        self.scale = 80

    def update(self):

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x -= RUN_SPEED_PPS * game_framework.frame_time

        if self.x < -50:
            game_world.remove_object(self)
        pass


    def draw(self):
        if self.type == 0:
            Potion.images_green.clip_draw(int(self.frame)%2 * 256, int(self.frame)// 2, 256, 256, self.x, self.y,self.scale,self.scale)
            draw_rectangle(*self.get_bb())
        elif self.type == 1:
            Potion.images_blue.clip_draw(int(self.frame)%2 * 256, int(self.frame)// 2, 256, 256, self.x, self.y, self.scale, self.scale)
            draw_rectangle(*self.get_bb())
        else :
            Potion.images_red.clip_draw(int(self.frame)%2 * 256, int(self.frame)// 2, 256, 256, self.x, self.y, self.scale,self.scale)
            draw_rectangle(*self.get_bb())
    def handle_event(self, event):
        pass
    def handle_collision(self,group, other):
        if group == 'witch:potion':
            game_world.remove_object(self)
    def get_bb(self):
        return self.x - 30, self.y - 35, self.x + 30, self.y+35

