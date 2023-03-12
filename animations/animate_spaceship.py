import asyncio
from curses_tools import draw_frame
from itertools import cycle
from curses_tools import read_controls, get_frame_size

async def animate_spaceship(canvas, row, column, rocket_frame_1, rocket_frame_2):
   
    frames = [rocket_frame_1, rocket_frame_2]
    
    input_controls = []

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
        row_dir, col_dir, shot_btn = input_controls
        row += row_dir
        column += col_dir
          

