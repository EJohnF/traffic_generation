import random
from threading import Thread
import gi
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, WebKit, Gdk
import time
from process_python_api import Logger, LError, LInfo
from collections import deque



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


if __name__ != "__main__":
    from Generator import view, max_loading_time
    view.connect("load-finished", fin)
    view.connect("load-error", error)


def main_loop():
    global prevFinished
    global last
    global isError
    waiting = 0
    while True:
        if isError:
            time.sleep(5)
            isError = False
        if (prevFinished or waiting > max_loading_time) and len(pages) > 0:
            if last != '' and prevFinished:
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
    # if len(pages) > 2000:
    #     time.sleep(600)
    pages.append(link)
    times.append(wait)
    Logger.log(LInfo, "waiting_size " + str(len(pages)))

if __name__ == "__main__":
    view = WebKit.WebView()
    sw = Gtk.ScrolledWindow()
    sw.add(view)

    win = Gtk.Window()
    win.set_default_size(1200, 800)
    win.add(sw)
    win.show_all()

    if (len(sys.argv)>1):
        view.open(sys.argv[1])
    else:
        view.open("https://habrahabr.ru/")
    Gtk.main()
