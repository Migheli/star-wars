import asyncio
from curses_tools import draw_frame
from itertools import cycle
from curses_tools import read_controls, get_frame_size
from physics import update_speed
from animations.fire_animation import fire
from animations.game_messages import GameOverException
from animations.explosion import explode


async def animate_spaceship(canvas, coordinates, rocket_animation, coroutines, obstacles, obstacles_in_last_collision, is_gun_available):

    input_controls = []
    row_speed = column_speed = 0

    row, column = coordinates

    for frame in cycle(rocket_animation):

        for step in range(2):

            number_of_rows, number_of_columns = canvas.getmaxyx()
            ship_size_rows, ship_size_columns = get_frame_size(frame)
            ship_border_row = number_of_rows - ship_size_rows
            ship_border_column = number_of_columns - ship_size_columns

            row = min(row, ship_border_row)
            row = max(row, 0)
            column = min(column, ship_border_column)
            column = max(column, 0)

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
                    obstacles_in_last_collision.append(obstacle)
                    await explode(canvas, obstacle.row, obstacle.column)
                    await explode(canvas, row, column)
                    raise GameOverException
                    return

            gun_available = is_gun_available()

            if gun_available and is_shot_pressed:
                coroutines.append(fire(canvas, row, column, obstacles, obstacles_in_last_collision))
