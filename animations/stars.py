import asyncio
import curses
from random import randint

async def sleep(tics=1):
    for tic in range(tics):
        await asyncio.sleep(0)


async def blink(canvas, row, column, symbol, offset_tics):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(offset_tics)

        canvas.addstr(row, column, symbol)
        await sleep(offset_tics)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(offset_tics)
          
        canvas.addstr(row, column, symbol)
        await sleep(offset_tics)
