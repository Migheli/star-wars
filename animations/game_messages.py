import asyncio
from curses_tools import draw_frame, get_frame_size


async def show_game_over(canvas, center_row, center_column, gameover_frame):
    gameover_size_rows, gameover_size_columns = get_frame_size(gameover_frame)
    center_column -= gameover_size_columns*0.5
    center_row -= gameover_size_rows*0.5
    while True:
        draw_frame(canvas, center_row, center_column, gameover_frame, negative=False)
        await asyncio.sleep(0)
