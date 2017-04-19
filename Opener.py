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
from Statistics import *

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
        if prevFinished and len(queue) > 0:
            if last != '':
                load_page(last, waiting)
                Logger.log(LInfo, "loading time for {0} was: {1} seconds".format(last, waiting))
            waiting = 0
            prevFinished = False
            Gdk.threads_enter()
            current = queue.popleft()
            last = current
            Logger.log(LInfo, "open: {}".format(current))
            view.open(current)
            Gdk.threads_leave()
        waiting += 1
        time.sleep(1)


th = Thread(target=main_loop)
th.start()


def open_page(link):
    Logger.log(LInfo, 'put in deque: ' + link + "dec size: " + str(len(queue)))
    queue.append(link)
