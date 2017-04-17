import random
from threading import Thread
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, WebKit, Gdk
import time
from process_python_api import Logger, LError, LInfo
import subprocess
from collections import deque
from MainLoop import view

view.connect("load-finished", lambda v, f: fin())
# Logger.init("Opener")

queue = deque()

prevFinished = True


def fin():
    global prevFinished
    prevFinished = True


def main_loop():
    time.sleep(3)

    global prevFinished
    waiting = 0
    while True:
        # print(prevFinished)
        print(prevFinished, waiting)
        # if waiting > 10:
        #     Gdk.threads_enter()
        #     view.stop_loading()
        #     Gdk.threads_leave()
        if prevFinished:
            waiting = 0
            prevFinished = False
            Gdk.threads_enter()
            current = queue.popleft()
            print("open: ", current)
            view.open(current)
            Gdk.threads_leave()
        waiting += 1
        time.sleep(1)


def open_page(link):
    print('put in deque: ' + link + "dec size: " + str(len(queue)))
    queue.append(link)
    if len(queue) == 1:
        main_loop()
    # subprocess.Popen('python3 open.py ' + link, shell=True)
