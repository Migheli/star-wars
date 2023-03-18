import asyncio
from curses_tools import draw_frame
from itertools import cycle
from curses_tools import read_controls, get_frame_size
from physics import update_speed
from animations.fire_animation import fire
from animations.stars import sleep


async def game_over(canvas, center_row, center_column, gameover_frame):
    gameover_size_rows, gameover_size_columns = get_frame_size(gameover_frame)
    center_column -= gameover_size_columns*0.5
    center_row-= gameover_size_rows*0.5
    while True:
        draw_frame(canvas, center_row, center_column, gameover_frame, negative=False)
        await asyncio.sleep(0)
                    

async def animate_spaceship(canvas, row, column, rocket_frame_1, rocket_frame_2, coroutines, obstacles, obstacles_in_last_collision):
   
    frames = [rocket_frame_1, rocket_frame_2]
    
    input_controls = []
    
    row_speed = column_speed = 0

    center_row = row
    center_column = column 

    with open("gameover.txt", "r") as gameover_file:    
            gameover_frame = gameover_file.read()


    game_over_async = game_over(canvas, center_row, center_column, gameover_frame)

    for frame in cycle(frames):

        


        number_of_rows, number_of_columns = canvas.getmaxyx()
        ship_size_rows, ship_size_columns = get_frame_size(frame)
        
        ship_border_row = number_of_rows - ship_size_rows
        ship_border_column = number_of_columns - ship_size_columns
        if row > ship_border_row:
            row = ship_border_row
        if column > ship_border_column:
            column = ship_border_column
        if row < 0:
            row = 0
        if column < 0:
            column = 0
        
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        
        draw_frame(canvas, row, column, frame, negative=True)
        input_controls = read_controls(canvas)
        row_direction, column_direction, is_shot_pressed = input_controls
        
        row_speed, column_speed = update_speed(row_speed, column_speed, row_direction, column_direction)


        row += row_speed
        column += column_speed


        for obstacle in obstacles:
            if obstacle.has_collision(row, column, ship_size_rows, ship_size_columns):
                coroutines.append(game_over_async)
                return

        if is_shot_pressed:
            coroutines.append(fire(canvas, row, column, obstacles, obstacles_in_last_collision))



