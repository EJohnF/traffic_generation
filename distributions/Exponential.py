from distributions.Distribution import Distribution
import numpy


class Exponential(Distribution):
    def next(self):
        value = self.random.exponential(self.params["L"])
        if value <= 1:
            return 1
        else:
            return value
