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


pages = deque()
times = deque()
prevFinished = True
last = ''
isError = False

def fin(v, param):
    global prevFinished
    prevFinished = True


def error(a,b,c,d):
    global isError
    isError = True
    Logger.log(LError, "error 0 {0} {1}".format(c, d))

view.connect("load-finished", fin)
view.connect("load-error", error)


def main_loop():
    global prevFinished
    global last
    global isError
    waiting = 0
    # if error occur - freeze flow for 1 min
    while True:
        if isError:
            time.sleep(60)
            isError = False
        if (prevFinished or waiting > 50) and len(pages) > 0:
            if last != '':
                Logger.log(LInfo, "loading_time {} ".format(waiting))
            waiting = 0
            prevFinished = False

            current = pages.popleft()
            time.sleep(times.popleft())
            last = current
            Logger.log(LInfo, "open 0 {}".format(current))
            # print('open next')

            Gdk.threads_enter()
            view.open(current)
            Gdk.threads_leave()
        waiting += 1
        time.sleep(1)


th = Thread(target=main_loop)
th.setDaemon(True)
th.start()


def open_page(link, wait):
    global th
    if not th.isAlive():
        Logger.log(LInfo, "restart 0 main loop")
        th = Thread(target=main_loop)
        th.setDaemon(True)
        th.start()
    if len(pages) > 200:
        time.sleep(600)
    pages.append(link)
    times.append(wait)
    Logger.log(LInfo, "waiting_size " + str(len(pages)))


