class Worker:
    def __init__(self, site_object, config):
        self.config = config
        self.site_scheme = site_object
        self.stop = False

    def start(self):
        Logger.log(LInfo, "start working Specific Type Worker".format(last, waiting))

    def stop(self):
        Logger.log(LInfo, "stop working Specific Type Worker".format(last, waiting))
        self.stop = True
