#########################################################################
#
#########################################################################
# :
# 1)
# 2)
# 3)
# :
#
#########################################################################
import numpy as np


def CalcMu2(ca=None):
    stop = np.asarray(ca).size
    mu = 0
    mu2 = 0
    for i1 in np.arange(1, stop+1).reshape(-1):
        temp_r = (ca[i1].real) ** 2 + (ca[i1].imag) ** 2
        temp_i = 2 * (ca[i1].real) * (ca[i1].imag)
        temp = complex(temp_r, temp_i)
        mu2 = mu2 + (np.abs(temp) - (np.abs(ca[i1]) ** 2))
        mu = mu + ca[i1]

    mu2 = mu2 / stop
    mu = np.abs(complex((mu.real) / stop, (mu.imag) / stop))
    temp = np.abs(np.mean(ca[i1]))
    return mu, mu2
