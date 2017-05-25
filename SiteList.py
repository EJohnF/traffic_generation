from openpyxl import load_workbook
from threading import Thread
import utils
import random
import time
from Opener import *
from Worker import Worker


def parse_xlsx_list(filename, worksheet, columnname):
    wb = load_workbook(filename)
    result = []
    for site in wb[worksheet][columnname]:
        result.append(site.value)
    return result


class SiteList(Worker):
    def __init__(self, site_object, config):
        super().__init__(site_object, config)
        self.th = ''
        self.index = -1
        self.sites = []
        self.scheme = utils.parse_scheme(self.site_scheme['scheme'], self.config)
        if site_object['file_type'] == 'xlsx':
            self.sites = parse_xlsx_list(site_object['file_name'], site_object['worksheet'], site_object['column'])

    def __iter__(self):
        return self

    def reset(self):
        self.index = -1

    def hasNext(self):
        return self.index < len(self.sites) - 1

    def next(self):
        self.index += 1
        if self.hasNext():
            return self.sites[self.index]
        else:
            raise StopIteration

    def get(self, index):
        if index < len(self.sites):
            return self.sites[index]
        else:
            return -1

    def worker(self):
        count_for_visit = self.site_scheme['count_for_visit']
        site_count = utils.create_distribution(self.scheme["page_number"])
        distr_time = utils.create_distribution(self.scheme["time_between_page"])
        while (self.site_scheme['count_for_visit'] == 0 or count_for_visit > 0) and self.hasNext():
            utils.go_round_site(self.next(), site_count, distr_time, self.scheme['page_generator'])
            count_for_visit -= 1
            if not self.hasNext():
                self.reset()

    def start(self):
        self.stop = False
        thread = Thread(target=self.worker, args=())
        thread.setDaemon(True)
        thread.start()
        self.th = thread
