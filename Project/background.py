from pico2d import *
import game_world
import game_framework
from obstacle import Obstacle
from potion import Potion
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 35.0  # Km / Hour
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
        self.obstacle_check = False
        self.potion_check = False
        self.roof = 0
        self.score = 0
        self.font = load_font('YJ_Obang_TTF.ttf',32)
    def update(self):
        self.x -= RUN_SPEED_PPS * game_framework.frame_time
        self.score += RUN_SPEED_MPS * game_framework.frame_time
        if self.x <=0 and self.obstacle_check == False:
            self.obstacle_check = True
            obstacle = Obstacle(1)
            game_world.add_object(obstacle)
            game_world.add_collision_pair('witch:obstacle', None, obstacle)

        if self.x <= -800:
            self.roof += 1
            self.x = 800
            self.obstacle_check = False
            obstacle = Obstacle(1)
            game_world.add_object(obstacle)
            game_world.add_collision_pair('witch:obstacle', None, obstacle)

        if self.roof % 8 == 3 and self.potion_check == False:
            self.potion_check = True
            potion = Potion()
            game_world.add_object(potion)
            game_world.add_collision_pair('witch:potion', None, potion)
        elif self.roof % 8 != 3 : self.potion_check = False



    def draw(self):
        self.image.clip_draw(0,0,3652,2436,
                             self.x,self.y,
                             self.width,self.height)
        self.image.clip_draw(0, 0, 3652, 2436,
                             self.x + self.width, self.y,
                             self.width, self.height)
        self.font.draw(1400, 750, f'Score : {int(self.score)}', (200, 0, 255))
        print(self.score)
    def get_bb(self):
        return 0, 0, 1600 - 1, 50


class Title_background:
    def __init__(self):
        self.image = load_image('image/start.png')
        self.width = 1600
        self.height = 800
        self.x = 800
        self.y = 400
        self.check = False

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(100, 0, self.image.w-200, self.image.h,
                             self.x, self.y,
                             self.width, self.height)


    def get_bb(self):
        return 0, 0, 1600 - 1, 50

class End_background:
    def __init__(self):
        self.image = load_image('image/Score .png')
        self.width = 1600
        self.height = 800
        self.x = 800
        self.y = 400
        self.check = False

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w, self.image.h,
                             self.x, self.y,
                             self.width, self.height)


    def get_bb(self):
        return 0, 0, 1600 - 1, 50