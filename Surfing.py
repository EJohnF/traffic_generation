from threading import Thread
import utils
import random
import time
from Opener import *
from Worker import Worker
from process_python_api import Logger, LError, LInfo


class Surfing(Worker):
    def __init__(self, initURL, scheme):
        super().__init__(initURL, scheme)
        self.currentURL = initURL
        self.th = ''
        links = utils.get_URLs_from_page(initURL)
        Logger.log(LInfo, "links_on_page {}".format(len(links)))
        self.links = set(links)
        self.history = set()
        self.scheme = scheme

    def worker(self):
        distr_time = utils.create_distribution(self.scheme['time_between_page'])
        while not self.stop and len(self.links) > 0:
            self.currentURL = self.links.pop()
            self.history.add(self.currentURL)
            links = utils.get_URLs_from_page(self.currentURL)
            Logger.log(LInfo, "links_on_page {}".format(len(links)))
            self.links.update(links)
            self.links -= self.history
            sleep_time = distr_time.next()
            open_page(self.currentURL)
            Logger.log(LInfo, "sleep {}".format(sleep_time))
            time.sleep(sleep_time)

    def start(self):
        self.stop = False
        thread = Thread(target=self.worker, args=())
        thread.setDaemon(True)
        thread.start()
        self.th = thread
