import asyncio
import curses

async def sleep(tics=1):
    for tic in range(tics):
        await asyncio.sleep(0)


async def blink(canvas, row, column, symbol, offset_tics):
    await sleep(offset_tics)
    while True:
        
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(20)
       
        canvas.addstr(row, column, symbol)
        await sleep(3)
    
        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(5)
        
        canvas.addstr(row, column, symbol)
        await sleep(3)
        