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
max_loading_time = 10
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
    global max_loading_time
    max_loading_time = config["max_loading_time"]
    th = Thread(target=start_generating, args=(config,))
    th.setDaemon(True)

    th1 = Thread(target=check, args=(config,))
    th1.start()


    Gdk.threads_init()
    sw = Gtk.ScrolledWindow()
    sw.add(view)


    settings = WebKit.WebSettings()
    settings.set_property("user-agent", config["user_agent"])
    view.set_settings(settings)
    view.open("http://google.com")
    th.start()
    Gtk.main()
    Logger.log(LInfo, "finish")


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main(sys.argv[1:])