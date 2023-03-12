import asyncio
import curses
from random import randint

async def blink(canvas, row, column, symbol):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for i in range(randint(3,20)):
            await asyncio.sleep(0)
                                 
        canvas.addstr(row, column, symbol)
        for i in range(randint(3,20)):
            await asyncio.sleep(0)
           
        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for i in range(randint(3,20)):
            await asyncio.sleep(0)
          
          
        canvas.addstr(row, column, symbol)
        for i in range(randint(3,20)):
            await asyncio.sleep(0)
    