from datetime import datetime as dt
import time
import subprocess as sb
from pathlib import Path

START_H, START_M = 1, 0
END_H, END_M = 7, 0

start_total_m = START_H * 60 + START_M
end_total_m = END_H * 60 + END_M

folderpath = Path("C:/Users/саске/AppData/Local/c0sSs1n-LLC")
folderpath.mkdir(parents=True, exist_ok=True)
logpath = folderpath / "log.txt"

logdata = f"\n|ON|{dt.now()}, Компьютер успешно включен."
with open(logpath, "a", encoding="utf-8") as f:
    f.write(logdata)

already_run_tonight = False

print("|LOG| Скрипт запущен и переходит в режим отслеживания.")

while True:
    now = dt.now()
    current_total_m = now.hour * 60 + now.minute


    is_inside_window = False
    if start_total_m < end_total_m:
        is_inside_window = start_total_m <= current_total_m < end_total_m
    else:
        is_inside_window = current_total_m >= start_total_m or current_total_m < end_total_m

    if is_inside_window:
        if not already_run_tonight:
            print(f"|LOG| [{dt.now()}] Время подходит. Запуск admpanel.py...")
            sb.run(["python", "admpanel.py"])
            already_run_tonight = True
    
        minutes_to_end = (end_total_m - current_total_m) % 1440
        seconds_to_sleep = (minutes_to_end * 60) - now.second
        
        if seconds_to_sleep > 0:
            print(f"|LOG| [{dt.now()}] Скрипт отработал внутри окна. Спим до конца окна {seconds_to_sleep} сек.")
            time.sleep(seconds_to_sleep)
        else:
            time.sleep(1)
        continue

    else:
        already_run_tonight = False
        
        waitfortotal = (start_total_m - current_total_m) % 1440
        seconds_to_sleep = (waitfortotal * 60) - now.second
        
        if seconds_to_sleep <= 0:
            seconds_to_sleep = 10
            
        print(f"|LOG| [{dt.now()}] Вне рабочего времени. Скрипт уходит в глубокий сон на {seconds_to_sleep} сек. до старта.")
        time.sleep(seconds_to_sleep)
