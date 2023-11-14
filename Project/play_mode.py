import random
from pico2d import *
import game_framework
import game_world
from background import Background
from witch import Witch
from ball import Ball
from potion import Potion
from zombie import Zombie
from obstacle import Obstacle
# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            witch.handle_event(event)

def init():
    global background
    global witch
    global balls
    global obstacles
    global potions
    running = True

    background = Background()
    game_world.add_object(background, 0)

    witch = Witch()
    game_world.add_object(witch, 1)
    game_world.add_collision_pair('witch:obstacle', witch, None)
    game_world.add_collision_pair('witch:r_potion', witch, None)

    potions = [Potion(i) for i in range(1,20,2)]
    game_world.add_objects(potions, 1)
    for potion in potions:
        game_world.add_collision_pair('witch:r_potion', None, potion)



def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

