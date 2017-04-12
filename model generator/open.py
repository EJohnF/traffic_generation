import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, WebKit
import sys
import time
from threading import Thread


def close_gtk():
    time.sleep(10)
    Gtk.main_quit()

thread = Thread(target=close_gtk, args=())
thread.setDaemon(True)
thread.start()

view = WebKit.WebView()
sw = Gtk.ScrolledWindow()
sw.add(view)
view.open(str(sys.argv[1]))
Gtk.main()


