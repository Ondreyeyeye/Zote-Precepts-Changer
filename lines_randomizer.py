import tkinter as tk
import asyncio
import requests
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Label
import pyautogui as pg
import pymsgbox
from async_tkinter_loop import async_handler, async_mainloop


file_output_name = ''
max_random_number = 0
previous_numbers = []


def get_random_number():
    url = f'https://www.random.org/integers/?num=1&min=0&max={max_random_number}&base=10&format=plain&col=5'
    number = int(requests.get(url).text)
    while True:
        if (number in previous_numbers):
            number = int(requests.get(url).text)
        else:
            break

    previous_numbers.append(number)
    if (len(previous_numbers) > 10):
        del previous_numbers[0:1]

    return number


def source_lines_input():
    global input_lines, max_random_number

    name = filedialog.askopenfilename() 

    # проверка выбран ли файл
    if (name == ''):
        messagebox.showerror('Ну ты совсем чтоли?', 'Ошибка: Файл забыла выбрать........')
        return
    # проверка на расширение файла
    if (Path(name).suffix != '.txt'):
        messagebox.showerror('Ну ты совсем чтоли?', 'Ошибка: Полюш, ну txt файлы же надо(')
        return
    
    file = open(name, 'r', encoding='utf8')

    input_lines = file.readlines()
    max_random_number = len(input_lines) - 1

    file.close()


def get_output_file_name():
    global file_output_name
    name = filedialog.askopenfilename()
    
    # проверка выбран ли файл
    if (name == ''):
        messagebox.showerror('Ну ты совсем чтоли?', 'Ошибка: Файл забыла выбрать........')
        return
    # проверка на расширение файла
    if (Path(name).suffix != '.txt'):
        messagebox.showerror('Ну ты совсем чтоли?', 'Ошибка: Полюш, ну txt файлы же надо(')
        return
    
    file_output_name = name


async def write_loop():
    global input_lines
    while True:
        file = open(file_output_name, 'w', encoding='utf8')

        file.write(input_lines[get_random_number()])

        file.close()

        await asyncio.sleep(time_of_delay)


root = tk.Tk()
root.geometry('400x300')
root.title('Zote Precepts Changer')
root.resizable(0, 0)
root.iconbitmap('_internal/book_copy.ico')
root.configure(bg = '#fefafa')
root.eval('tk::PlaceWindow . center')

pymsgbox.rootWindowPosition = '+960+540'
time_of_delay = int(pg.prompt('Input delay time in seconds', 'Data Input', '1'))

label = Label(root)
label.pack()


tk.Button(bd = 0, width = 15, height = 1, bg='#f6d2d6', text = 'Input File', command = source_lines_input).pack(pady = 10)
tk.Button(bd = 0, width = 15, height = 1, bg='#f6d2d6', text = 'Output File', command = get_output_file_name).pack(pady = 10)
tk.Button(root, bd = 0, width = 15, height = 1, bg='#f6d2d6', text = "Start", command = async_handler(write_loop)).pack(pady = 10)


async_mainloop(root)