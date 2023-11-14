from pico2d import *
import game_world
import game_framework
from obstacle import Obstacle

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 40.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Background:

    def __init__(self):
        self.image = load_image('image/back_1stage.png')
        self.width = 1600
        self.height = 800
        self.x = 800
        self.y = 400
        self.check = False
    def update(self):
        self.x -= RUN_SPEED_PPS * game_framework.frame_time

        if self.x <=0 and self.check == False:
            self.check = True
            obstacle = Obstacle(1)
            game_world.add_object(obstacle)
            game_world.add_collision_pair('witch:obstacle', None, obstacle)

        if self.x <= -800:
            self.x = 800
            self.check = False
            obstacle = Obstacle(1)
            game_world.add_object(obstacle)
            game_world.add_collision_pair('witch:obstacle', None, obstacle)

    def draw(self):
        self.image.clip_draw(0,0,3652,2436,
                             self.x,self.y,
                             self.width,self.height)
        self.image.clip_draw(0, 0, 3652, 2436,
                             self.x + self.width, self.y,
                             self.width, self.height)


    def get_bb(self):
        return 0, 0, 1600 - 1, 50
