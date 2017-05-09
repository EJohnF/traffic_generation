from distributions.Distribution import Distribution
import numpy


class NormalPositive(Distribution):
    def next(self):
        value = self.random.normal(self.params["M"], numpy.sqrt(self.params["D"]))
        if value <= 1:
            return 1
        else:
            return value
