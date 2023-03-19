import time
import curses
from random import randint, choice
from animations.fire_animation import fire
from animations.animate_spaceship import animate_spaceship
from animations.stars import blink
from animations.space_garbage import fly_garbage
from animations.stars import sleep
from animations.obstacles import show_obstacles
import time 
import math
from game_scenario import get_garbage_delay_tics, PHRASES

import asyncio


TIC_TIMEOUT = 0.1
GARBAGE_DELAY = 10
coroutines = []
obstacles = []
obstacles_in_last_collisions = []
start_time = time.time()
year = None

def draw(canvas):
    canvas.nodelay(True)

    curses.curs_set(0)

    with open("rocket_frame_1.txt", "r") as frame_file1, open("rocket_frame_2.txt", "r") as frame_file2:
        rocket_frame_1, rocket_frame_2 = frame_file1.read(), frame_file2.read()

    window_width, window_height = curses.window.getmaxyx(canvas)
    border_y, border_x = window_width-1, window_height-1

    """ window.getmaxyx - return tuple of values width and height of window, not coordinates of last cells in rows and columns. Numeration of width and height of window starts from 0 and it values always more, than coordinates of last cells in rows/columns (+1). That's why we need to makes (-1) in border_x, border_y declaration """

    with open("trash_small.txt", "r") as trash_small, open("trash_large.txt", "r") as trash_large, open("trash_xl.txt", "r") as trash_xl:
        garbage = [trash_small.read(), trash_large.read(), trash_xl.read()]

    center_y, center_x = border_y//2, border_x//2

    
    stat_canvas = canvas.derwin(1, 1) 
    #shot = fire(canvas, center_y, center_x, obstacles)





    stars_signs = ['+', '*', '.', ':']
    start_row = start_column = 1
    
    min_number_of_stars = 10
    max_number_of_stars = 145


    async def update_current_year(start_time):
        while True:
            seconds_left = time.time() - start_time 
            years_left = math.floor(seconds_left/1.5)
            global year 
            year = 1951 + years_left
            await asyncio.sleep(0)

    coroutines.append(update_current_year(start_time))


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
                canvas.addstr(1, 6, '                           ')


            canvas.refresh()
            await asyncio.sleep(0)



    coroutines.append(show_current_year(stat_canvas))
    coroutines.append(show_phrases(stat_canvas))

    
    ship = animate_spaceship(canvas, center_y, center_x, rocket_frame_1, rocket_frame_2, coroutines, obstacles, obstacles_in_last_collisions, start_time)

    coroutines.append(ship)
    
    async def fill_orbit_with_garbage(canvas, garbage, start_column, border_x, obstacles, obstacles_in_last_collisions):
        while True:
            if year:
                garbage_delay = get_garbage_delay_tics(year)
                if garbage_delay:
                        coroutines.append(fly_garbage(canvas, randint(start_column, border_x), choice(garbage), obstacles, obstacles_in_last_collisions))
                        await sleep(garbage_delay)
        
            await asyncio.sleep(0)
           
    for i in range(randint(min_number_of_stars, max_number_of_stars)):
        coroutines.append(blink(canvas, randint(start_row, border_y), randint(start_column, border_x), choice(stars_signs)))


    coroutines.append(fill_orbit_with_garbage(canvas, garbage, start_column, border_x, obstacles, obstacles_in_last_collisions))
    coroutines.append(show_obstacles(canvas, obstacles))


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