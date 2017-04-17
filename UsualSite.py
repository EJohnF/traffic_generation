from threading import Thread
import utils
import random
import time
from Opener import *
from Worker import Worker


class UsualSite(Worker):

    def __init__(self, site_scheme, config):
        super().__init__(site_scheme, config)

    def worker(self):
        scheme = utilsparse_scheme(self.site_scheme['scheme'], config)
        utils.go_round_site(self.site_scheme['link'], scheme)

    def start(self):
        self.stop = False
        thread = Thread(target=self.worker, args=())
        thread.start()
