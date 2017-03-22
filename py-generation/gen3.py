import json
import random
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,WebKit
import google
import time
from threading import Thread

view = WebKit.WebView()
sw = Gtk.ScrolledWindow()
sw.add(view)


def thread_open():
    Gtk.main()

threadList = []

def open_page(link):
    print('open_page', link)
    view.open("http://www."+link)
    #view.open(link)
    thread_open();
#    thread = Thread(target=thread_open, args=( ))
#   thread.setDaemon(True)
#    thread.start()
#    threadList.append(thread)

random.seed(10)

open_page("habrahabr.ru")
