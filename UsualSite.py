from threading import Thread
import utils
import random
import time
from Opener import *
from Worker import Worker


class UsualSite(Worker):

    def __init__(self, site_scheme, config):
        super().__init__(site_scheme, config)
        self.th = Thread(target=self.worker, args=())

    def worker(self):
        scheme = utils.parse_scheme(self.site_scheme['scheme'], self.config)
        site_count = utils.create_distribution(scheme["page_number"])
        distr_time = utils.create_distribution(scheme["time_between_page"])
        utils.go_round_site(self.site_scheme['link'], site_count, distr_time, scheme['page_generator'])

    def start(self):
        self.stop = False
        thread = Thread(target=self.worker, args=())
        thread.setDaemon(True)
        thread.start()
        self.th = thread
