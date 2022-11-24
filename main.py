import threading
import win10toast
from prettytable import PrettyTable
import datetime
import time
from time import mktime
Notyftable = PrettyTable()
Notyf = win10toast.ToastNotifier()
Notyftable.field_names = ["Номер", "Название", "Описание", "Deadline"]
Notyftable.align["Название"], Notyftable.align["Описание"] = "l","l"




def weit_time(naz, opi, ttime, threads):
    time.sleep(mktime(datetime.datetime.timetuple(ttime)) - time.time())
    Notyf.show_toast(title=naz, msg=opi, icon_path="notyf.ico")
    del threads[naz]

def new_thread(threads,naz,opi,ttime):
    threads[naz] = threading.Thread(target=weit_time, args=(naz, opi, ttime, threads)).start()


def add_notif(numb, naz,opi,threads):
    global mytime
    stop = False
    # sec2000 = datetime.datetime.strptime("01-01-2000", "%d-%m-%Y")
    # print(sec2000)
    while not stop:
        tm = input("""Установить таймер - 1
Установить deadline - 2
Отменить действие - stop

1/2: """).lower()
        if tm == "1":
            stopt = False
            while not stopt:
                set_time = input("Введите колличество часов и минут (stop - отмена действия) (hh:mm): ").lower()
                if set_time == "stop":
                    break
                elif len(set_time) != 5 or set_time[2] != ":" or int(set_time[0:2]) > 23 or int(set_time[3:]) > 59:
                    print("Неверное значение!\n")
                    continue
                else:
                    mytime = datetime.datetime.strptime(set_time, "%H:%M")
                    ttime = datetime.datetime.now() + datetime.timedelta(hours=mytime.hour, minutes=mytime.minute)
                    itime = ttime.strftime("%H:%M:%S %d.%m.%Y'")
                    Notyftable.add_row([numb, naz, opi, itime])
                    print("Напоминание успешно добавлено!\n")
                    new_thread(threads,naz,opi, ttime)
                    stopt = True
                    stop = True

            #time.sleep(mktime(datetime.datetime.timetuple(ttime)) - time.time())
            #Notyf.show_toast(title=naz, msg=opi, duration=60, icon_path="notyf.ico")
        elif tm == "2":
            stopt = False
            while not stopt:
                set_time = input("Введите дату (stop - отмена действия) (dd.mm.yyyy hh:mm): ").lower()
                if set_time == "stop":
                    break
                elif len(set_time) != 16 or set_time[2] != "." or set_time[5] != "." or set_time[10] != " " \
                        or set_time[13] != ":" or int(set_time[0:2]) > 31 or int(set_time[3:5]) > 12 \
                        or int(set_time[11:13]) > 23 or int(set_time[14:]) > 59:
                    print("Неверное значение!\n")
                    continue

                mytime = datetime.datetime.strptime(set_time, "%d.%m.%Y %H:%M")
                if mytime < datetime.datetime.now():
                    print("Можно установить только предстоящие событие!")
                    continue
                else:
                    itime = mytime.strftime("%H:%M:%S %d.%m.%Y")
                    Notyftable.add_row([numb, naz, opi, itime])
                    print("Напоминание успешно добавлено!\n")
                    new_thread(threads, naz, opi, mytime)
                    stopt = True
                    stop = True
        elif tm == "stop":
            stop = True
        else:
            print("Неверное значение!\n")



def clear_nitif():
    Notyftable.clear()


def show():
    print(Notyftable)


numb = 0
threads = {}
stop = False
while not stop:
    comand = input("""\nНовое напоминание - new
Показать - show
Отчистить - clear
Закрыть программу - stop

Команда: """).lower()
    if comand == "new":
        numb += 1

        naz = input("Введите название: ")
        opi = input("Опишите событие:  ")
        add_notif(numb,naz, opi,threads)

    elif comand == "show":
        show()
    elif comand == "clear":
        clear_nitif()
        numb = 0
        Notyftable.field_names = ["Номер", "Название", "Описание", "Deadline"]
    elif comand == "stop":
        print("Спасибо за использование приложения!")
        stop = True
    else:
        print("Такой команды нет!")