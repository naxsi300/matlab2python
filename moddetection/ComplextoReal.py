#########################################################################
# переход от комплексной к вещественной форме сигнала
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# вход:
# 1) массив комплексной случайной величины
# выход:
# массив вещественных значений сигнала
#########################################################################
import numpy as np


def ComplextoReal(ca=None):
    # re=real(ca);
    # im=image(ca);
    stop = np.asarray(ca).size
    ca_real = np.zeros((stop * 2, 1))
    ca_image = np.zeros((stop * 2, 1))
    n = 1
    for i in np.arange(1, stop+1).reshape(-1):
        ca_real[n] = ca[i].real * np.cos((n - 1) * np.pi / 2)
        ca_real[n + 1] = 0
        ca_image[n] = 0
        ca_image[n + 1] = ca[i].imag * (- np.sin((n) * np.pi / 2))
        n = n + 2

    ca_real = ca_real + ca_image
    return ca_real
