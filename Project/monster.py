import random
import math
import game_framework
import game_world
from pico2d import *
import play_mode
from cat import Cat

# potion Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 35.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# potion Action Speed
TIME_PER_ACTION = 0.8
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4.0

ANIMATION_SPEED_KMPH = 3.0  # Km / Hour
ANIMATION_SPEED_MPM = (ANIMATION_SPEED_KMPH * 1000.0 / 60.0)
ANIMATION_SPEED_MPS = (ANIMATION_SPEED_MPM / 60.0)
ANIMATION_SPEED_PPS = (ANIMATION_SPEED_MPS * PIXEL_PER_METER)

class Monster:

    image_1 = None
    image_2 = None
    image_3 = None
    image_4 = None
    sound_1 = None
    sound_2 = None
    def load_images(self):
        if Monster.image_1 == None:
            Monster.image_1 = load_image("image/monster_1.png")
        if Monster.image_2 == None:
            Monster.image_2 = load_image("image/monster_2.png")
        if Monster.image_3 == None:
            Monster.image_3 = load_image("image/monster_3.png")
        if Monster.image_4 == None:
            Monster.image_4 = load_image("image/monster_4.png")
        if Monster.sound_1 == None:
            Monster.sound_1 = load_wav("sound/monterhit.wav")
        if Monster.sound_2 == None:
            Monster.sound_2 = load_wav("sound/monsterdead.wav")
        Monster.sound_1.set_volume(25)
        Monster.sound_2.set_volume(25)
    def __init__(self, type):
        self.x = random.randint(800 + 850, 800 + 1200)
        self.y = random.randint(100, 500)
        self.load_images()
        self.frame = 0
        self.scale = 200
        self.type = type
        if type == 1:
            self.hp = 3
        elif type == 2:
            self.hp = 2
        elif type == 3:
            self.hp = 2
        elif type == 4:
            self.hp = 1
        self.animation = True # 위 아래 움직임
        self.animation_moved = 0
    def update(self):
        if self.hp == 0:
            self.y -= RUN_SPEED_PPS * game_framework.frame_time * 2.5
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
            if self.type == 1:
                self.x -= RUN_SPEED_PPS * game_framework.frame_time

            elif self.type == 2:
                self.x -= RUN_SPEED_PPS * game_framework.frame_time * 1.2
            elif self.type == 3:
                self.x -= RUN_SPEED_PPS * game_framework.frame_time * 1.8
            elif self.type == 4:
                self.x -= RUN_SPEED_PPS * game_framework.frame_time * 2

            if self.animation == True:
                self.y += ANIMATION_SPEED_PPS * game_framework.frame_time
                self.animation_moved += ANIMATION_SPEED_PPS * game_framework.frame_time
            if self.animation_moved >= 5:
                self.animation = False
            else:
                self.y -= ANIMATION_SPEED_PPS * game_framework.frame_time
                self.animation_moved -= ANIMATION_SPEED_PPS * game_framework.frame_time
            if self.animation_moved <= -5:
                self.animation = True

        if self.x < -50 and self.y < -50:
            game_world.remove_object(self)
        pass


    def draw(self):
        if self.type == 1:
            Monster.image_1.clip_draw(int(self.frame) % 2 * 512, 0, 512, 512, self.x, self.y,self.scale,self.scale)
        elif self.type == 2:
            Monster.image_2.clip_draw(int(self.frame) % 2 * 512, 0, 512, 512, self.x, self.y,self.scale,self.scale)
        elif self.type == 3:
            Monster.image_3.clip_draw(int(self.frame) % 2 * 512, 0, 512, 512, self.x, self.y, self.scale, self.scale)
        elif self.type == 4:
            Monster.image_4.clip_draw(int(self.frame) % 2 * 512, 0, 512, 512, self.x, self.y,self.scale,self.scale)


        #draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass
    def handle_collision(self,group, other):
        if group == 'witch:monster':
           pass
        if group == 'monster:bullet':
           if self.hp == 1:
               self.sound_2.play()
               if len(Cat.vaild_cat_idx) >= 4:
                    play_mode.background.score += 600
               else : play_mode.background.score += 200
           else: self.sound_1.play()
           self.hp -= 1


    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y+50

