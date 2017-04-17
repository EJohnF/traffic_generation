import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, WebKit
import sys
import time
from threading import Thread


def close_gtk():
    time.sleep(5)
    Gtk.main_quit()

thread = Thread(target=close_gtk, args=())
thread.setDaemon(True)
thread.start()

view = WebKit.WebView()
# view.connect("load-finished", lambda v, f: Gtk.main_quit())

# settings = WebKit.WebSettings()
# settings.set_property("user-agent", 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0')

sw = Gtk.ScrolledWindow()
sw.add(view)
view.open(str(sys.argv[1]))
Gtk.main()


