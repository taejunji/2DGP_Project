# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LCTRL, SDLK_RIGHT, \
    draw_rectangle
import game_world
import game_framework
from bullet import Bullet
import End_mode
# state event check
# ( state event type, event value )

def control(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LCTRL

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

def hitted(e):
    return e[0] == 'HIT'

def dead(e):
    return e[0] == 'DEAD'
# time_out = lambda e : e[0] == 'TIME_OUT'


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
FALL_SPEED_KMPH = -10.0  # Km / Hour
FALL_SPEED_MPM = (FALL_SPEED_KMPH * 1000.0 / 60.0)
FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0)
FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER)


ANIMATION_SPEED_KMPH = 5.0  # Km / Hour
ANIMATION_SPEED_MPM = (ANIMATION_SPEED_KMPH * 1000.0 / 60.0)
ANIMATION_SPEED_MPS = (ANIMATION_SPEED_MPM / 60.0)
ANIMATION_SPEED_PPS = (ANIMATION_SPEED_MPS * PIXEL_PER_METER)

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
        if witch.hp == 0:
            witch.state_machine.handle_event(('DEAD', 0))

        witch.frame = (witch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        if witch.velocity >= -100:
            witch.updatespeed()
        witch.y += witch.velocity * game_framework.frame_time * 100/ 36 / 0.3

        if witch.y >= 760:
            witch.velocity = -10
        if witch.y <= 40:
            witch.jump()

    @staticmethod
    def draw(witch):
        witch.image.clip_draw(int(witch.frame) * 327, 323 * 2, 327, 323, witch.x, witch.y , 100, 100)




class Jump:

    @staticmethod
    def enter(witch, e):
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
        if witch.hp == 0:
            witch.state_machine.handle_event(('DEAD', 0))

        witch.frame = (witch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2


        if witch.velocity >= -100:
            witch.updatespeed()
        witch.y += witch.velocity * game_framework.frame_time * 100 / 36 / 0.3

        if witch.velocity <= 0:
            witch.state_machine.handle_event(('TIME_OUT', 0))

        if witch.y >= 760:
            witch.velocity = -10

    @staticmethod
    def draw(witch):
        if witch.frame <= 2:
            witch.image.clip_draw( 2 * 327, 323 * 1, 327, 323, witch.x, witch.y,100,100)
        else:
            witch.image.clip_draw( 1 * 327, 323 * 1, 327, 323, witch.x, witch.y,100,100)



class Hitted:

    @staticmethod
    def enter(witch, e):
        if hitted(e):
            witch.hitted = True
            witch.frame = 0
            witch.wait_time = get_time()
        pass

    @staticmethod
    def exit(witch, e):
        if space_down(e):
            witch.jump()

        if time_out(e):
            witch.wait_time = 0
            witch.hitted = False

        witch.x = 250
        pass

    @staticmethod
    def do(witch):
        if witch.hp == 0:
            witch.state_machine.handle_event(('DEAD', 0))


        witch.frame = (witch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        if witch.velocity >= -100:
            witch.updatespeed()
        witch.y += witch.velocity * game_framework.frame_time * 100 / 36 / 0.3

        if witch.y >= 760:
            witch.velocity = -10
        if witch.y <= 40:
            witch.jump()

        if witch.animation == True:
            witch.x += ANIMATION_SPEED_PPS * game_framework.frame_time
            witch.animation_moved += ANIMATION_SPEED_PPS * game_framework.frame_time
            if witch.animation_moved >= 4:
                witch.animation = False
        else:
            witch.x -= ANIMATION_SPEED_PPS * game_framework.frame_time
            witch.animation_moved -= ANIMATION_SPEED_PPS * game_framework.frame_time
            if witch.animation_moved <= -4:
                witch.animation = True

        if get_time() - witch.wait_time > 2.5:
            witch.state_machine.handle_event(('TIME_OUT', 0))
    @staticmethod
    def draw(witch):
        witch.image.clip_draw(int(witch.frame) * 327, 323 * 0, 327, 323, witch.x, witch.y , 100, 100)

class Dead:

    @staticmethod
    def enter(witch, e):
        witch.rad = 0
        pass

    @staticmethod
    def exit(witch, e):
        pass

    @staticmethod
    def do(witch):
        witch.frame = (witch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        witch.rad += 0.1
        if witch.velocity >= -100:
            witch.updatespeed()
        witch.y += witch.velocity * game_framework.frame_time * 100 / 36 / 0.3

        if witch.y >= 760:
            witch.velocity = -10


        if witch.animation == True:
            witch.x += ANIMATION_SPEED_PPS * game_framework.frame_time
            witch.animation_moved += ANIMATION_SPEED_PPS * game_framework.frame_time
            if witch.animation_moved >= 4:
                witch.animation = False


        if witch.y < -100:
            game_framework.change_mode(End_mode)
    @staticmethod
    def draw(witch):
        witch.image.clip_composite_draw(int(witch.frame) * 327, 323 * 0, 327, 323,witch.rad,'' ,witch.x, witch.y , 100, 100)
class StateMachine:
    def __init__(self, witch):
        self.witch = witch
        self.cur_state = Idle
        self.transitions = {
            Idle: {space_down: Jump, control: Idle, hitted: Hitted,dead: Dead},
            Jump: {control: Idle, time_out: Idle, space_down: Jump, hitted: Hitted,dead: Dead},
            Hitted: {time_out: Idle,space_down: Hitted,dead: Dead},
            Dead:{hitted: Dead}
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
        self.x, self.y = 250, 400
        self.frame = 0
        self.gravityaccel = 5
        self.velocity = 0
        self.image = load_image('image/witch.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.ball_count = 10
        self.wait_time = 0
        self.hitted = False
        self.animation = False
        self.animation_moved = 0
        self.hp = 3
        self.hp_image = load_image('image/heart.png')
    def fire_ball(self):
        if self.ball_count > 0:
            self.ball_count -= 1
            bullet = Bullet(self.x, self.y, self.face_dir*10)
            game_world.add_object(bullet)
            game_world.add_collision_pair('boss:bullet', None, bullet)

    def jump(self):
        self.velocity = 35
    def updatespeed(self):
        self.velocity -= self.gravityaccel * game_framework.frame_time * 100/ 36 / 0.3

    def update(self):
        self.state_machine.update()


    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb()) # 튜플을 풀어해쳐서 분리해서 인자로 제공
        print(self.hp)
        for a in range(0,self.hp):
            self.hp_image.clip_draw(0, 0, 28, 27, 100 + 40 * a, 750, 30, 30)
    def get_bb(self):
        return self.x-40, self.y -50, self.x +20, self.y+30

    def handle_collision(self,group, other):
        # 여기
        if group == 'witch:obstacle' and self.hitted == False:
           self.state_machine.handle_event(('HIT', 0))
           if self.hp > 0:
               self.hp -= 1

        if group == 'witch:potion' and self.hp < 3:
            if other.type == 2:
                self.hp += 1

        if group == 'witch:cat':
            pass
        if group == 'witch:boss':
            quit()
            pass

