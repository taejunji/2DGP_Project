# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LCTRL, SDLK_RIGHT, \
    draw_rectangle
from ball import Ball
import game_world
import game_framework

# state event check
# ( state event type, event value )

def control(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LCTRL

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

# time_out = lambda e : e[0] == 'TIME_OUT'


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
FALL_SPEED_KMPH = -10.0  # Km / Hour
FALL_SPEED_MPM = (FALL_SPEED_KMPH * 1000.0 / 60.0)
FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0)
FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER)

def update_Fall_speed(a,b,c,d):
    b = (a * 1000.0 / 60.0)
    c = (b / 60.0)
    d = (c * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2




class Idle:

    @staticmethod
    def enter(witch, e):
        witch.frame = 0

        pass

    @staticmethod
    def exit(witch, e):

        if control(e):
            witch.fire_ball()

        if space_down(e):
            witch.jump()

        pass

    @staticmethod
    def do(witch):

        witch.frame = (witch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        if witch.velocity >= -50:
            witch.updatespeed(FALL_SPEED_KMPH)
        witch.y += witch.velocity * 100/ 36 / 0.3 * game_framework.frame_time



    @staticmethod
    def draw(witch):
        witch.image.clip_draw(int(witch.frame) * 327, 323 * 2, 327, 323, witch.x, witch.y , 100, 100)



class Jump:

    @staticmethod
    def enter(witch, e):
        witch.savespeed = witch.velocity
        witch.frame = 0

    @staticmethod
    def exit(witch, e):
        if space_down(e):
            witch.jump()

        if control(e):
            witch.fire_ball()

        if time_out(e):
            pass
        pass

    @staticmethod
    def do(witch):

        witch.frame = (witch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        if witch.velocity >= -60:
            witch.updatespeed(FALL_SPEED_KMPH)
        witch.y += witch.velocity * 100 / 36 / 0.3 * game_framework.frame_time

        if witch.velocity <= 0:
            witch.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(witch):
        if witch.frame <= 1:
            witch.image.clip_draw( 2 * 327, 323 * 1, 327, 323, witch.x, witch.y,100,100)
        else:
            witch.image.clip_draw( 1 * 327, 323 * 1, 327, 323, witch.x, witch.y,100,100)
        print(witch.frame)


class Sleep:

    @staticmethod
    def enter(witch, e):
        witch.frame = 0
        pass

    @staticmethod
    def exit(witch, e):
        pass

    @staticmethod
    def do(witch):
        witch.frame = (witch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8


    @staticmethod
    def draw(witch):
        if witch.face_dir == -1:
            witch.image.clip_composite_draw(int(witch.frame) * 100, 200, 100, 100,
                                          -3.141592 / 2, '', witch.x + 25, witch.y - 25, 100, 100)
        else:
            witch.image.clip_composite_draw(int(witch.frame) * 100, 300, 100, 100,
                                          3.141592 / 2, '', witch.x - 25, witch.y - 25, 100, 100)


class StateMachine:
    def __init__(self, witch):
        self.witch = witch
        self.cur_state = Idle
        self.transitions = {
            Idle: {space_down: Jump, control: Idle},
            Jump: {control: Idle, time_out: Idle, space_down: Idle},

        }

    def start(self):
        self.cur_state.enter(self.witch, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.witch)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.witch, e)
                self.cur_state = next_state
                self.cur_state.enter(self.witch, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.witch)





class Witch:
    def __init__(self):
        self.x, self.y = 100, 400
        self.frame = 0
        self.gravityaccel = 0.1
        self.savespeed = 0
        self.velocity = 0
        self.image = load_image('image/witch.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.ball_count = 10


    def fire_ball(self):
        if self.ball_count > 0:
            self.ball_count -= 1
            ball = Ball(self.x, self.y, self.face_dir*10)
            game_world.add_object(ball)
            game_world.add_collision_pair('zombie:throwball', None, ball)

    def jump(self):
        self.velocity = 25
    def updatespeed(self,a):
        self.velocity -= self.gravityaccel
        a -= self.velocity
    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

        draw_rectangle(*self.get_bb()) # 튜플을 풀어해쳐서 분리해서 인자로 제공

    def get_bb(self):
        return self.x-40, self.y -50, self.x +20, self.y+30

    def handle_collision(self,group, other):
        # 여기
        if group == 'boy:ball':
            self.ball_count += 1
        if group == 'boy:zombie':
            quit()
            pass

