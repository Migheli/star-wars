from curses_tools import draw_frame
import asyncio
from animations.obstacles import Obstacle 
from curses_tools import get_frame_size

async def fly_garbage(canvas, column, garbage_frame, obstacles, obstacles_in_last_collisions, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)
    row = 0

    garbage_size_rows, garbage_size_columns = get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, garbage_size_rows, garbage_size_columns)
    obstacles.append(obstacle)

    try:
        while row < rows_number:
            if obstacle in obstacles_in_last_collisions:
                return

            draw_frame(canvas, row, column, garbage_frame)


            obstacle.row = row 

            await asyncio.sleep(0)
            draw_frame(canvas, row, column, garbage_frame, negative=True)
            row += speed

    except StopIteration:
        obstacles.remove(obstacle)
        if obstacle in obstacles_in_last_collisions:
            obstacles_in_last_collisions.remove(obstacle)

    finally:
        obstacles.remove(obstacle)
        if obstacle in obstacles_in_last_collisions:
            obstacles_in_last_collisions.remove(obstacle)