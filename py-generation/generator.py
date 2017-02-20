import json
import random
import gtk
import webkit
import google
import time
from threading import Thread

view = webkit.WebView()
sw = gtk.ScrolledWindow()
sw.add(view)

# win = gtk.Window(gtk.WINDOW_TOPLEVEL)
# win.add(sw)
# win.show_all()


def thread_open():
    gtk.main()


def open_page(link):
    print 'open_page', link
    view.open("http://www."+link)
    thread = Thread(target=thread_open, args=( ))
    thread.start()

random.seed(10)


def distribution_to_value(description):
    dis_type = description["type"]
    if dis_type == "uniform":
        return random.randint(int(description["low_boundary"]), int(description["up_boundary"]))
    return 0


def generate_page_list(site_link, number_pages=10):
    result = []
    i = 0
    # for url in google.search("site:" + site_link):
    #     if i < number_pages:
    #         print 'generated page: ', url
    #         result.append(url)
    #         i += 1
    result.append(site_link)
    result.append(site_link)
    result.append(site_link)
    return result


def generator(sites):
    for site in sites:
        pages_list = generate_page_list(site)
        for page in pages_list:
            open_page(page)
            time.sleep(distribution_to_value(config['schemes']['default']['time_between_page']))

f = open('configuration.json', 'r')
config = json.load(f)
generator(config['sites'])
