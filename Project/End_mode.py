import random
from pico2d import *
import game_framework
import game_world
import play_mode
from background import Background, Title_background , End_background



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            play_mode.init()
            game_framework.change_mode(play_mode)


def init():
    global image
    global score
    global font
    font = load_font('YJ_Obang_TTF.ttf', 100)
    score = play_mode.background.score
    game_world.clear()
    image = End_background()
    game_world.add_object(image,0)
    play_mode.background.bgm.stop()
    End_background.dead_sound.play()

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    font.draw(700, 450, f'{int(score)}', (255, 255, 255))
    update_canvas()

def pause():
    pass

def resume():
    pass

