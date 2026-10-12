import time, os, asyncio, ctypes, sys
import msvcrt as ms
from pathlib import Path
from datetime import datetime as dt
password = ''
buffer = ''
timer = 0
oldlog = ''

folderpath = Path("C:/Users/саске/AppData/Local/c0sSs1n-LLC")
folderpath.mkdir(parents=True,exist_ok=True)
ogpath = folderpath / "info.txt"
logpath = folderpath / "log.txt"

with open(ogpath, "r",encoding='utf-8') as f:
    for i, line in enumerate(f):
        if (i == 0):password = line.strip()
        if (i == 1):timer = int(line.strip())

def make_console_unclosable():
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    hwnd = kernel32.GetConsoleWindow()
    if hwnd:
        hMenu = user32.GetSystemMenu(hwnd, False)
        if hMenu:
            user32.DeleteMenu(hMenu, 0xF060, 0x00000000)
            print("-=== Панель администрирования экранного времени ПК ===-")

def readchar():
    if ms.kbhit():
        return ms.getch()
    return None

async def set_timer(dur):
    global buffer, current_seconds
    for i in range(dur, -1, -1):
        current_seconds = i
        stars = "*" * len(buffer)
        print(f"\r\033[KОсталось: {i} секунд. Введите пароль: {stars}", end='', flush=True)
        await asyncio.sleep(1)
    print("\nПароль не введен в назначенное время.\nВыключение...")
    logdata = f"\n|OFF|{dt.now()}, Компьютер успешно выключен."
    with open(logpath,"a",encoding="utf-8") as f:
        f.write(logdata)
    os.system("shutdown /s /t 0")
    

async def get_input():
    loop = asyncio.get_running_loop()
    while True:
        ch = await loop.run_in_executor(None, readchar)
        if ch is not None:
            return ch
        await asyncio.sleep(0.05)

async def main():
    global buffer, current_seconds, timer
    current_seconds = timer
    timertask = asyncio.create_task(set_timer(timer))
    
    while True:
        inptask = asyncio.create_task(get_input())
        done, pending = await asyncio.wait(
            [timertask, inptask],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        if timertask in done:
            inptask.cancel()
            break
            
        if inptask in done:
            ch = inptask.result()
            if ch in (b'\r', b'\n'):
                if buffer == password:
                    timertask.cancel()
                    print("\n\nДоступ разрешен.")
                    break
                else:
                    buffer = ''
                    if not timertask.done():
                        print(f"\r\033[KОсталось: {current_seconds} секунд. Введите пароль: [НЕВЕРНО]", end='', flush=True)
                        await asyncio.sleep(1)
            elif ch == b'\x08':
                buffer = buffer[:-1]
            else:
                try:
                    buffer += ch.decode('utf-8')
                except UnicodeDecodeError:
                    pass
            
            if not timertask.done():
                stars = "*" * len(buffer)
                print(f"\r\033[KОсталось: {current_seconds} секунд. Введите пароль: {stars}", end='', flush=True)

    input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    make_console_unclosable()
    asyncio.run(main())
