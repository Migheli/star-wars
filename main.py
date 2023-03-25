import asyncio
import curses
import math
from os import listdir
from os.path import isfile, join
import time
from random import randint, choice
from animations.animate_spaceship import animate_spaceship
from animations.stars import blink, sleep
from animations.space_garbage import fly_garbage
from game_scenario import get_garbage_delay_tics, PHRASES


TIC_TIMEOUT = 0.1
START_YEAR = 1951
GUN_AVAILABLE_YEAR = 2020
start_time = time.time()
coroutines = []
obstacles = []
obstacles_in_last_collisions = []


async def show_current_year(canvas):
    while True:
        canvas.addstr(1, 1, str(year))
        canvas.refresh()
        await asyncio.sleep(0)


async def show_phrases(canvas):
    while True:
        if year in PHRASES:
            canvas.addstr(1, 6, PHRASES[year])
        else:
            canvas.addstr(1, 6, ' ' * 45)
        canvas.refresh()
        await asyncio.sleep(0)


async def update_current_year(start_time):
    while True:
        seconds_left = time.time() - start_time
        years_left = math.floor(seconds_left/1.5)
        global year
        year = START_YEAR + years_left
        await asyncio.sleep(0)


async def fill_orbit_with_garbage(canvas, garbage, start_column, border_x, obstacles, obstacles_in_last_collisions):
    while True:
        if year:
            garbage_delay = get_garbage_delay_tics(year)
            if garbage_delay:
                coroutines.append(fly_garbage(canvas, randint(start_column, border_x), choice(garbage), obstacles, obstacles_in_last_collisions))
                await sleep(garbage_delay)
        await asyncio.sleep(0)


def draw(canvas):
    canvas.nodelay(True)

    curses.curs_set(0)

    rocket_animation = []
    rocket_frame_dir = 'frames/rocket'
    rocket_frames = [join(rocket_frame_dir, frame) for frame in listdir(rocket_frame_dir)]
    
    for rocket_frame in rocket_frames:
        with open(rocket_frame, 'r') as rocket_frame_unit:
            rocket_animation.append(rocket_frame_unit.read())

    rocket_frame_1, rocket_frame_2 = rocket_animation


    window_width, window_height = curses.window.getmaxyx(canvas)
    border_y, border_x = window_width-1, window_height-1

    garbage = []
    garbage_frame_dir = 'frames/garbage'
    garbage_frames = [join(garbage_frame_dir, frame) for frame in listdir(garbage_frame_dir)]

    for garbage_frame in garbage_frames:
        with open(garbage_frame, 'r') as garbage_unit:
            garbage.append(garbage_unit.read())


    center_y, center_x = border_y//2, border_x//2

    stars_signs = ['+', '*', '.', ':']
    start_row = start_column = 1
    coroutines.append(update_current_year(start_time))
    stat_canvas = canvas.derwin(1, 1)
    coroutines.append(show_current_year(stat_canvas))
    coroutines.append(show_phrases(stat_canvas))
    ship = animate_spaceship(canvas, center_y, center_x, rocket_frame_1, rocket_frame_2, coroutines, obstacles, obstacles_in_last_collisions, start_time, START_YEAR, GUN_AVAILABLE_YEAR)
    coroutines.append(ship)
    min_number_of_stars = 10
    max_number_of_stars = 145

    for i in range(randint(min_number_of_stars, max_number_of_stars)):
        offset_tics = randint(3, 20)
        coroutines.append(blink(canvas, randint(start_row, border_y), randint(start_column, border_x), choice(stars_signs), offset_tics))

    coroutines.append(fill_orbit_with_garbage(canvas, garbage, start_column, border_x, obstacles, obstacles_in_last_collisions))

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        if not len(coroutines):
            break

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
