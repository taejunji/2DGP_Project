import random

import game_framework
import game_world
from pico2d import *


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0



class Boss:
    images = None

    def load_images(self):
        if Boss.images == None:
            Boss.images = {}


    def __init__(self):
        self.x, self.y = random.randint(1600-800, 1600), 150
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])
        self.scale = 2


    def update(self):

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 1600:
            self.dir = -1
        elif self.x < 800:
            self.dir = 1
        self.x = clamp(800, self.x, 1600)
        pass


    def draw(self):
        if self.dir < 0:
            Boss.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y - (2 - self.scale) * 50, self.scale * 100, self.scale * 100)
            draw_rectangle(*self.get_bb())
        else:
            Boss.images['Walk'][int(self.frame)].draw(self.x, self.y - (2 - self.scale) * 50, self.scale * 100, self.scale * 100)
            draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass
    def handle_collision(self,group, other):
        if group == 'zombie:throwball':
            self.scale -= 1
            if self.scale == 0:
                game_world.remove_object(self)
                game_world.remove_collision_object(self)
    def get_bb(self):
        return self.x - self.scale * 30, self.y-(2-self.scale)*50 - self.scale * 50, self.x + self.scale * 30, self.y-(2-self.scale)*50 +self.scale * 50

