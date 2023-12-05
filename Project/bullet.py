from pico2d import *
import game_world
import game_framework
import play_mode
from cat import Cat


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 35.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# potion Action Speed
TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6.0

class Bullet:
    image = None

    def __init__(self):
        if Bullet.image == None:
            Bullet.image = load_image('image/bullet.png')
        self.x, self.y = (play_mode.witch.x + 40), (play_mode.witch.y - 20)
        self.scale_x = 70
        self.scale_y = 50
        self.frame = 0
    def draw(self):
        Bullet.image.clip_draw(int(self.frame) % 6 * 117, 0, 117, 69, self.x, self.y, self.scale_x,
                              self.scale_y)
        # draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * game_framework.frame_time
        if self.x > 1700:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self,group, other):
        if group == 'monster:bullet':
            game_world.remove_object(self)
