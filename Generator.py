import getopt
import json
import sys
import utils
from threading import Thread
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, WebKit, Gdk
from process_python_api import Logger, LError, LInfo

view = WebKit.WebView()
help_string = "Generator.py -n <name> -c <configFile>"
workers = []

def start_generating(config):
    for site in config["sites"]:
        Logger.log(LInfo, "open new site scheme: " + str(site))
        workers.append(utils.parse_site_scheme(site, config))


def main(argv):
    config_file = ''
    name = ''
    try:
        opts, args = getopt.getopt(argv, "hn:c:", ["config=", "configuration=", "name="])
    except getopt.GetoptError:
        print('exception ' + help_string)
        sys.exit(2)
    for opt, arg in opts:
        print(opt, arg)
        if opt == '-h':
            print(help_string)
            sys.exit(1)
        if opt in ("-c", "--config", "--configuration"):
            config_file = arg
        if opt in ("-n", "--name"):
            name = arg

    if config_file == '':
        config_file = 'configuration.json'
        name = 'default'
    config_file = "config/"+config_file
    Logger.init(name)
    Logger.log(LInfo, "configuration file is {}".format(config_file))

    f = open(config_file, 'r')
    config = json.load(f)

    th = Thread(target=start_generating, args=(config,))
    Gdk.threads_init()
    sw = Gtk.ScrolledWindow()
    view.open("http://google.com")
    sw.connect("destroy", Gtk.main_quit)
    th.start()
    Gtk.main()
    Logger.log(LInfo, "generating finished")

if __name__ == "__main__":
    main(sys.argv[1:])
