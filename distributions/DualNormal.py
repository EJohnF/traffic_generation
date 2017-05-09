from distributions.Distribution import Distribution
import numpy as np


class DualNormal(Distribution):
    def __init__(self, params):
        super().__init__(params)
        m1 = params["M1"]
        d1 = params["D1"]
        m2 = params["M2"]
        d2 = params["D2"]
        self.p = []
        self.length = max(m1+d1*3, m2+d2*3)
        for i in range(self.length):
            self.p.append(
                0.5 * (
                    1.0 / (np.sqrt(2 * np.pi * d1)) * np.exp(- (i - m1) ** 2 / float(2 * d1))
                )
                +
                0.5 * (
                    1.0 / (np.sqrt(2 * np.pi * d2)) * np.exp(- (i - m2) ** 2 / float(2 * d2))
                )
            )
        print(self.p)
        print(sum(self.p))
        self.p[0] += 1-sum(self.p)

    def next(self):
        return self.random.choice(a=self.length, p=self.p)
