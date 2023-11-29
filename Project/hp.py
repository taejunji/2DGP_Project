import random
import math
import game_framework
import game_world
import play_mode
from pico2d import *
class Hp:
    image = None

    def load_images(self):
        if Hp.image == None:
            Hp.image = load_image("image/heart.png")

    # 0 탑 1 바텀
    def __init__(self):
        self.x = 100
        self.y = 500
        self.scale = 30
        self.load_images()


    def update(self):
        pass


    def draw(self):
        Hp.image.clip_draw(0, 0, 28, 27, self.x, self.y, self.scale,self.scale)


    def handle_event(self, event):
        pass
    def handle_collision(self,group, other):
        pass
    def get_bb(self):
        return self.x - 40, self.y-(self.scale_y/2), self.x + 40, self.y+self.scale_y/2

