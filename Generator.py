import getopt
import json
import sys
import utils
from threading import Thread
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, WebKit, Gdk, GLib
from process_python_api import Logger, LError, LInfo
import argparse
import signal

view = WebKit.WebView()
Gdk.threads_init()
sw = Gtk.ScrolledWindow()
sw.add(view)
view.open("http://google.com")
sw.connect("destroy", Gtk.main_quit)
sw.connect("delete-event", Gtk.main_quit)
workers = []


th = ''

def start_generating(config):
    for site in config["sites"]:
        Logger.log(LInfo, "open new site scheme: " + str(site))
        workers.append(utils.parse_site_scheme(site, config))


def main(argv):
    parser = argparse.ArgumentParser(description='The script for starting threads for traffic generation')
    parser.add_argument("-c", help='a configuration for generating', metavar='configuration', dest='config',
                        default='config/configuration.json')
    parser.add_argument("-n", help='a name of this generator for using in logs', metavar='name', dest='name',
                        default='default')
    arguments = parser.parse_args(argv)

    Logger.init(arguments.name)
    Logger.log(LInfo, "configuration file is {}".format(arguments.config))

    f = open(arguments.config, 'r')
    config = json.load(f)
    global th
    th = Thread(target=start_generating, args=(config,))
    th.setDaemon(True)
    th.start()
    Gtk.main()
    Logger.log(LInfo, "generating finished")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main(sys.argv[1:])



