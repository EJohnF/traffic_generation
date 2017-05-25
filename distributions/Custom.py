from distributions.Distribution import Distribution
import numpy as np


class Custom(Distribution):
    def __init__(self, params):
        super().__init__(params)
        self.length = len(params['array'])
        self.p = params['array']

    def next(self):
        return self.random.choice(a=self.length, p=self.p)
