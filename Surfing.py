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
        links = utils.get_URLs_from_page(initURL)
        Logger.log(LInfo, "number of links on page {0} is {1}".format(initURL, len(links)))
        self.links = set(links)
        self.history = set()
        self.scheme = scheme

    def worker(self):
        while not self.stop and len(self.links) > 0:
            self.currentURL = self.links.pop()
            self.history.add(self.currentURL)
            links = utils.get_URLs_from_page(self.currentURL)
            Logger.log(LInfo, "number of links on page {0} is {1}".format(self.currentURL, len(links)))
            self.links.update(links)
            self.links -= self.history
            sleep_time = utils.distribution_to_value(self.scheme['time_between_page'])
            open_page(self.currentURL)
            Logger.log(LInfo, "sleep {}".format(sleep_time))
            time.sleep(sleep_time)

    def start(self):
        self.stop = False
        thread = Thread(target=self.worker, args=())
        thread.start()
