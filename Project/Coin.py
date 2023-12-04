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
TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4.0

class Coin:
    images = None

    def load_images(self):
        if Coin.images == None:
            Coin.images = load_image("image/Coin.png")



    # 0 그린 1 블루 2레드
    def __init__(self):
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
            Coin.images.clip_draw(int(self.frame) % 4 * 256, int(self.frame) // 4, 256, 256, self.x, self.y,self.scale,self.scale)
            draw_rectangle(*self.get_bb())
    def handle_event(self, event):
        pass
    def handle_collision(self,group, other):
        if group == 'witch:coin':
            game_world.remove_object(self)
        if group == 'coin:obstacle':
            self.x += 50
    def get_bb(self):
        return self.x - 30, self.y - 35, self.x + 30, self.y+35

