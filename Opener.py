import random
from threading import Thread
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, WebKit, Gdk
import time
from process_python_api import Logger, LError, LInfo
import subprocess
from collections import deque
from Generator import view

view.connect("load-finished", lambda v, f: fin())

queue = deque()
prevFinished = True
last = ''


def fin():
    global prevFinished
    prevFinished = True


def main_loop():
    global prevFinished
    global last
    waiting = 0
    while True:
        print("loop prev finished " + str(prevFinished))
        if (prevFinished or waiting > 50) and len(queue) > 0:
            if last != '':
                Logger.log(LInfo, "loading_time {} ".format(waiting))
            waiting = 0
            prevFinished = False
            current = queue.popleft()
            last = current
            Logger.log(LInfo, "open 0 {}".format(current))
            print('open next')
            Gdk.threads_enter()
            view.open(current)
            Gdk.threads_leave()
        waiting += 1
        time.sleep(1)


th = Thread(target=main_loop)
th.setDaemon(True)
th.start()


def open_page(link):
    global th
    if not th.isAlive():
        Logger.log(LInfo, "restart 0 main loop")
        th = Thread(target=main_loop)
        th.setDaemon(True)
        th.start()
    Logger.log(LInfo, "waiting_size " + str(len(queue)))
    queue.append(link)

