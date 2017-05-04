import numpy
import time
from numpy import random


class Distribution:
    def __init__(self, params):
        random.seed(int(time.time()))
        self.params = params
        self.random = random

    def next(self):
        return 0