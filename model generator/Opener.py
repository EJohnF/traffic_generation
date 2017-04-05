import random
from threading import Thread
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, WebKit
import time
from process_python_api import Logger, LError, LInfo
Logger.init("Opener")


view = WebKit.WebView()
sw = Gtk.ScrolledWindow()
sw.add(view)

def thread_open(link):
    view.open(link)
    Gtk.main()

threadList = []

def open_page(link):
    #print('open link', link)
    Logger.log(LInfo, "open page {}".format(link));
    thread = Thread(target=thread_open, args=(link,))
    thread.setDaemon(True)
    thread.start()
    threadList.append(thread)

random.seed(10)
