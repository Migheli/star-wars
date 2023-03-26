import asyncio
from curses_tools import draw_frame, get_frame_size


class GameOverException(Exception):
    pass


async def show_game_over(canvas, coordinates, frame='frames/gameover.txt'):

    center_row, center_column = coordinates

    with open(frame, 'r') as gameover_frame:
        frame = gameover_frame.read()

    gameover_size_rows, gameover_size_columns = get_frame_size(frame)
    center_column -= gameover_size_columns*0.5
    center_row -= gameover_size_rows*0.5
    while True:
        draw_frame(canvas, center_row, center_column, frame, negative=False)
        await asyncio.sleep(0)
