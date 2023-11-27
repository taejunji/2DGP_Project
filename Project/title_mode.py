import random
from pico2d import *
import game_framework
import game_world
import play_mode
from background import Background, Title_background
from witch import Witch
from bullet import Bullet
from potion import Potion
from Boss import Boss
from obstacle import Obstacle
from cat import Cat


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)

def init():
    global image
    image = Title_background()
    game_world.add_object(image,0)

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

