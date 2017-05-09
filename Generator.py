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
import time
view = WebKit.WebView()
workers = []
sites = []

stop = False
th = ''

def start_generating(config):
    global stop
    global workers
    global sites
    for site in config["sites"]:
        if stop:
            stop = False
            break
        Logger.log(LInfo, "site_scheme 0 " + str(site))
        workers.append(utils.parse_site_scheme(site, config))
        sites.append(site)


def restart(config):
    time.sleep(500)
    Logger.log(LInfo, "restart 0 ")
    Gdk.threads_enter()
    Gtk.main_quit()
    Gdk.threads_leave()

    global stop
    global view
    view = WebKit.WebView()
    stop = True
    time.sleep(10)
    th = Thread(target=start_generating, args=(config,))
    th.setDaemon(True)

    th1 = Thread(target=check, args=(config,))
    th1.start()

    Gdk.threads_init()
    sw = Gtk.ScrolledWindow()
    sw.add(view)
    view.open("http://google.com")

    win = Gtk.Window()
    win.add(sw)
    win.show_all()

    th.start()
    Gdk.threads_enter()
    Gtk.main()
    Gdk.threads_leave()

def check(config):
    global th
    while True:
        for counter, worker in enumerate(workers):
            if not worker.th.isAlive():
                Logger.log(LInfo, 'counter {0} sites {1} {2}'.format(counter, len(sites), sites))
                Logger.log(LInfo, "restart 0 " + str(sites[counter]))
                workers[counter] = utils.parse_site_scheme(sites[counter], config)
        time.sleep(5)



def main(argv):
    parser = argparse.ArgumentParser(description='The script for starting threads for traffic generation')
    parser.add_argument("-c", help='a configuration for generating', metavar='configuration', dest='config',
                        default='config/configuration.json')
    parser.add_argument("-n", help='a name of this generator for using in logs', metavar='name', dest='name',
                        default='default')
    arguments = parser.parse_args(argv)

    Logger.init(arguments.name)
    Logger.log(LInfo, "configuration 0 {}".format(arguments.config))

    f = open(arguments.config, 'r')
    config = json.load(f)
    global th
    th = Thread(target=start_generating, args=(config,))
    th.setDaemon(True)

    th1 = Thread(target=check, args=(config,))
    th1.start()


    Gdk.threads_init()
    sw = Gtk.ScrolledWindow()
    sw.add(view)
    view.open("http://google.com")

    th.start()
    Gtk.main()
    Logger.log(LInfo, "finish")

def print_something(signal, frame):
    print(str(signal))
    print('RESTORE')
    sys.exit(1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGSEGV, print_something)
    signal.signal(signal.SIGTRAP, print_something)
    main(sys.argv[1:])