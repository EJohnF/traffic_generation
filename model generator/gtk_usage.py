import random
from threading import Thread
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, WebKit, GObject, Gdk
import time
from process_python_api import Logger, LError, LInfo
import subprocess

sites = ["https://vk.com", "https://habrahabr.com", "http://rzd.com", "https://youtube.com"]
view = WebKit.WebView()

def main_loop():
    time.sleep(3)
    number = 0
    global view
    while True:
        # Setting a random value for the fraction
        Gdk.threads_enter()
        view.open(sites[number])
        print(sites[number])
        Gdk.threads_leave()
        number = (number + 1) % 4
        # Releasing the gtk global mutex
        time.sleep(3)
th = Thread(target=main_loop)
th.start()


Gdk.threads_init()
sw = Gtk.ScrolledWindow()
sw.add(view)
view.open("https://vk.com")
sw.connect('destroy', Gtk.main_quit)
Gtk.main()