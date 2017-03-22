import thread
import utils
import random
import time
import Opener


class Surfing:
    currentURL = ''
    links = []
    history = []
    stop = False

    def __init__(self, initURL, scheme):
        self.currentURL = initURL
        self.links = utils.get_URLs_from_page(initURL)
        self.history.append(initURL)
        self.scheme = scheme

    def worker(self):
        while not self.stop:
            self.currentURL = self.links[random.randint(0, len(self.links))]
            self.history.append(self.currentURL)
            self.links = utils.get_URLs_from_page(self.currentURL)
            resulted_list = []
            for link in self.links:
                if link not in self.history:
                    resulted_list.append(link)
            if len(resulted_list) > 0:
                self.links = resulted_list
            sleep_time = utils.distribution_to_value(self.scheme['time_between_page'])
            Opener.open_page(self.currentURL)
            time.sleep(sleep_time)

    def start(self):
        self.stop = False
        thread.start_new_thread(self.worker, ())

    def stop(self):
        self.stop = True
