from threading import Thread
import utils
import random
import time
from Opener import *
from Worker import Worker


class Surfing(Worker):
    def __init__(self, initURL, scheme):
        super().__init__(initURL, scheme)
        self.currentURL = initURL
        self.links = set(utils.get_URLs_from_page(initURL))
        self.history = set()
        self.scheme = scheme

    def worker(self):
        while not self.stop and len(self.links) > 0:
            self.currentURL = self.links.pop()
            self.history.add(self.currentURL)
            self.links.update(utils.get_URLs_from_page(self.currentURL))
            print(self.history)
            self.links -= self.history
            sleep_time = utils.distribution_to_value(self.scheme['time_between_page'])
            open_page(self.currentURL)
            time.sleep(sleep_time)

    def start(self):
        self.stop = False
        thread = Thread(target=self.worker, args=())
        thread.start()
