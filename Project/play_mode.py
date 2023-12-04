import random
from pico2d import *
import game_framework
import game_world
from background import Background
from witch import Witch
from bullet import Bullet
from potion import Potion
from Boss import Boss
from obstacle import Obstacle
from cat import Cat
from Coin import Coin

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

    background = Background()
    game_world.add_object(background, 0)

    witch = Witch()
    game_world.add_object(witch, 1)
    game_world.add_collision_pair('witch:obstacle', witch, None)
    game_world.add_collision_pair('witch:potion', witch, None)
    game_world.add_collision_pair('witch:cat', witch, None)
    game_world.add_collision_pair('witch:coin',  witch, None)
    game_world.add_collision_pair('witch:monster', witch, None)

    # potions = [Potion(i) for i in range(5,10,5)]
    # game_world.add_objects(potions, 1)
    # for potion in potions:
    #     game_world.add_collision_pair('witch:potion', None, potion)

    cats = [Cat(i, i/10) for i in range(2, 40, 10)]
    game_world.add_objects(cats, 1)
    for cat in cats:
        game_world.add_collision_pair('witch:cat', None, cat)
        game_world.add_collision_pair('cat:obstacle', cat, None)


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

