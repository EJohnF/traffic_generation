import utils

class Worker:
    def __init__(self, site_object, config):
        self.config = config
        self.site_scheme = site_object
        self.stop = False
        self.scheme = utils.parse_scheme(self.site_scheme['scheme'], self.config)

    def start(self):
        Logger.log(LInfo, "start ".format(self.site_scheme))

    def stop(self):
        Logger.log(LInfo, "stop ".format(self.site_scheme))
        self.stop = True
