import json
import random
import numpy
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

threadList = []


def open_page(link):
    print 'open_page', link
    # view.open("http://www."+link)
    view.open(link)
    thread = Thread(target=thread_open, args=( ))
    thread.setDaemon(True)
    thread.start()
    threadList.append(thread)

random.seed(10)


def distribution_to_value(description):
    dis_type = description["type"]
    if dis_type == "uniform":
        return random.randint(int(description["low_boundary"]), int(description["up_boundary"]))
    if dis_type == "log-normal":
        return numpy.exp(numpy.random.normal(description["M"], description["D"]))
    return 0


def generate_page_list(site_link, number_pages=10):
    result = []
    i = 0
    for url in google.search("site:" + site_link, num=number_pages):
        if i < number_pages:
            print 'generated page: ', url
            result.append(url)
            i += 1
        else:
            break
    print 'list generated'
    return result


def generator(sites):
    for site in sites:
        number_page = distribution_to_value(config['schemes']['default']['page_number'])
        print 'page_number ', number_page
        pages_list = generate_page_list(site, int(number_page))
        for page in pages_list:
            open_page(page)
            sleep_time = distribution_to_value(config['schemes']['default']['time_between_page'])
            print 'sleep time: ', sleep_time
            time.sleep(sleep_time)

f = open('configuration.json', 'r')
config = json.load(f)
generator(config['sites'])
