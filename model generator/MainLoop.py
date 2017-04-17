import getopt
import json
import sys
import utils
from threading import Thread
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, WebKit, Gdk

view = WebKit.WebView()

def main(argv):
    configFile = ''
    try:
        opts, args = getopt.getopt(argv, "hc:", ["config=", "configuration="])
    except getopt.GetoptError:
        print('MainLoop.py -c <configFile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('MainLoop.py -c <configFile>')
            sys.exit()
        elif opt in ("-c", "--config", "--configuration"):
            configFile = arg

    if configFile == '':
        configFile = 'configuration.json'

    print('Config file is ', configFile)

    f = open(configFile, 'r')
    config = json.load(f)

    th = Thread(target=utils.parser_site_list, args=(config['sites'], config,))
    Gdk.threads_init()
    sw = Gtk.ScrolledWindow()
    view.open("http://google.com")
    sw.connect("destroy", Gtk.main_quit)
    th.start()
    Gtk.main()

if __name__ == "__main__":
    main(sys.argv[1:])
