from distributions.Distribution import Distribution


class Fix(Distribution):
    def next(self):
        return self.params["value"]
