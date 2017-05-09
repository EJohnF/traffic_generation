from threading import Thread
import utils
import random
import time
from Opener import *
from Worker import Worker
import google


class GoogleQuery(Worker):

    def __init__(self, site_scheme, config):
        super().__init__(site_scheme, config)
        self.th = Thread(target=self.worker, args=())
        self.th.setDaemon(True)

    def worker(self):
        site_count = utils.create_distribution(self.site_scheme["site_number"])
        page_count = utils.create_distribution(self.scheme["page_number"])
        distr_time = utils.create_distribution(self.scheme["time_between_page"])
        for query in self.site_scheme["queries"]:
            Logger.log(LInfo, "query 0 {}".format(query))
            count = site_count.next()
            Logger.log(LInfo, "number_site {} ".format(count))
            sites = google.search(query, num=count, stop=count, pause=3.0)
            for site in sites:
                Logger.log(LInfo, "open_site 0 {}".format(site))
                utils.go_round_site(site, page_count, distr_time, self.scheme['page_generator'])

    def start(self):
        self.stop = False
        self.th.start()
