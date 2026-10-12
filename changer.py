from pathlib import Path

folderpath = Path("C:/Users/саске/AppData/Local/c0sSs1n-LLC")
folderpath.mkdir(parents=True,exist_ok=True)
ogpath = folderpath / "info.txt"
password = timer = newpassword = 0

with open(ogpath, "r",encoding='utf-8') as f1:
    for i, line in enumerate(f1):
        if i == 0: password = line.strip()
        if i == 1: timer = line.strip()
        
while True:
    print("Для смены пароля введите старый:")
    answer = input(">> ")
    if answer != password:
        print("Пароль неверный.")
        continue
    elif answer == password:
        newpassword = input("Введите новый пароль:\n>> ")
        try:
            newtimer = int(input("При желании введите новое время отсчета(секунды('30' если нет)): "))
            break
        except ValueError:
            print("Ввод секунд только ЦЕЛЫМИ числами")
            continue
    

with open(ogpath, "w",encoding='utf-8') as f:
    f.write(f"{newpassword}\n{newtimer}")

