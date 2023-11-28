import getpass
import os
import subprocess

import pyautogui as pag
import time
import pytesseract
from PIL import Image
import tkinter as tk
import threading


global data
data = []


file_path = r'C:\MUVIETSS2\MUVIETSS2.exe'


def check_account_connected():
    if len(data) <= 3:
        subprocess.Popen(file_path)
        time.sleep(5)


def background_task():
    findWindow()
    # turnOnAuto()


def add_data(number, name, server, status):
    global data
    data.append([
        number,
        name,
        server,
        status
    ])
    # Notify the tkinter thread about the data change
    root.event_generate("<<DataChange>>")



def getTextFromImage(imageUrl):
    image = Image.open(imageUrl)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(image)
    global data
    add_data(1, text, "Davias", "CONNECTED")
    print(text)
    return text


def on_data_change(event):
    listbox.delete(0, tk.END)
    check_account_connected()
    for row in range(len(data)):
        listbox.insert(row, f"{row} - {data[row][1]} - {data[row][2]} - {data[row][3]}")
    listbox.insert(0, "Number - Character - Server - Status")


root = tk.Tk()
root.title("Auto MU")

# Thêm widget listbox vào root
listbox = tk.Listbox(root, width=50, height=20)
listbox.pack()
# Tắt tính năng tự điều chỉnh kích thước của listbox
listbox.pack_propagate(False)
button = tk.Button(root, text="Start Background Task", command=background_task)
button.pack(side=tk.TOP)



def click(x, y):
    pag.moveTo(x, y)
    pag.mouseDown()
    pag.click()
    time.sleep(0.5)
    pag.mouseUp()


def keyPress(keyName):
    pag.keyDown(keyName)
    time.sleep(0.5)
    pag.keyUp(keyName)

def getName(window):
    time.sleep(1)
    window.activate()
    time.sleep(3)
    keyPress("c")
    time.sleep(1)
    screen = pag.screenshot(region=(1180, 262, 150, 22))
    time.sleep(1)
    screen.save('pic1.png')
    keyPress("c")
    print('imaged')
    return getTextFromImage('pic1.png')

def findWindow():
    windows = pag.getWindowsWithTitle('MU VIET SEASON 2.0')
    print(windows)
    if windows:
        for i in range(len(windows)):
            getName(windows[i])

def turnOnAuto():
    pag.hotkey('home')


def main():
    root.bind("<<DataChange>>", on_data_change)
    thread = threading.Thread(target=background_task)
    thread.start()
    root.mainloop()


if __name__ == '__main__':
    main()