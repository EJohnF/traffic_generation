#draw graph for distribution on python 2.7
import numpy
import numpy as np
import time
from numpy import random
from platform import python_version
if float(python_version()[0:3]) < 3:
    import matplotlib.pyplot as plt


def dual_normal(m1, d1, m2, d2):
    # m1 = params['m1']//["M1"]
    # d1 = params.d1//["D1"]
    # m2 = params.m2//["M2"]
    # d2 = params.d2//["D2"]
    p = []
    for i in range(100):
        p.append(
            0.5*(
                1.0 / (np.sqrt(2 * np.pi*d1)) * np.exp(- (i - m1) ** 2 / float(2 * d1))
                )
            +
            0.5*(
                1.0 / (np.sqrt(2 * np.pi * d2)) * np.exp(- (i - m2) ** 2 / float(2 * d2))
                )
        )
    return p


def exponential(l):
    arr = np.random.exponential(l, 1000)
    p = np.zeros(100)
    for a in arr:
        if a < 100:
            p[a] += 1
    for count, per in enumerate(p):
        p[count] /= 1000
    return p

# p = dual_normal(10, 40, 70, 500)
p = exponential(5)
# print(p)
if float(python_version()[0:3]) < 3:
    plt.plot(p)
    plt.show()

