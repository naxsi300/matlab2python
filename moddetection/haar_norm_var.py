#
#:
#   mas -

#:
#   disp2 -
#   abs_disp2 -
#################################################################################################
#function [disp, abs_disp,disp2,abs_disp2]=haar_norm_var (mas)
import numpy as np
import pywt
from ComplextoReal import ComplextoReal


def haar_norm_var(mas=None):

    real_s = ComplextoReal(mas)

    D = np.amax(np.abs(real_s))

    real_abs = real_s / D

    a, d = pywt.dwt(real_s, 'dmey')

    an, dn = pywt.dwt(real_abs, 'dmey')

    disp = np.var(np.abs(a))
    disp2 = np.var(np.abs(d))

    abs_disp = np.var(np.abs(an))
    abs_disp2 = np.var(np.abs(dn))
    return disp2, abs_disp2
