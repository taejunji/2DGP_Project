import random
import math
import game_framework
import game_world
from pico2d import *

# obstancle Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 25.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# obstancle Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2.0

class Obstacle:
    images_top = None
    images_bottom = None

    def load_images(self):
        if Obstacle.images_top == None:
            Obstacle.images_top = load_image("image/spider.png")
        if Obstacle.images_bottom == None:
            Obstacle.images_bottom = load_image("image/obstacle.png")


    # 0 탑 1 바텀
    def __init__(self,num):
        self.topbottom = random.randint(0,1)
        self.x = random.randint(800 * num + 850, 800 * num + 1200)
        self.scale_y = random.randint(300, 350)

        if self.topbottom == 0:
            self.y = 600 - self.scale_y / 2
        else:
            self.y = self.scale_y / 2

        self.load_images()
        self.frame = 0


    def update(self):

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x -= RUN_SPEED_PPS * game_framework.frame_time

        if self.x < -50:
            game_world.remove_object(self)
        pass


    def draw(self):
        if self.topbottom == 0:
            Obstacle.images_top.clip_draw(int(self.frame) * 256, 0, 256, 1500, self.x, self.y,100,self.scale_y)
            draw_rectangle(*self.get_bb())
        else:
            Obstacle.images_bottom.clip_draw(int(self.frame) * 256, 0, 256, 1500, self.x, self.y, 100, self.scale_y)
            draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass
    def handle_collision(self,group, other):
        if group == 'witch:obstacle':
            print("x")
            pass
    def get_bb(self):
        return self.x - 35, self.y-(self.scale_y/2 - 10), self.x + 35, self.y+(self.scale_y/2 - 10)

