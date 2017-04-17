class Worker:
    config = ''
    site_scheme = ''
    stop = False

    def __init__(self, site_object, config):
        self.config = config
        self.site_scheme = site_object

    def start(self):
        Logger.log(LInfo, "start working Specific Type Worker".format(last, waiting))

    def stop(self):
        Logger.log(LInfo, "stop working Specific Type Worker".format(last, waiting))
        self.stop = True
