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
    
def CalcMu2(ca = None): 
    stop = np.asarray(ca).size
    mu = 0
    mu2 = 0
    for i1 in np.arange(1,stop+1).reshape(-1):
        temp_r = real(ca(i1)) ** 2 + imag(ca(i1)) ** 2
        temp_i = 2 * real(ca(i1)) * imag(ca(i1))
        temp = complex(temp_r,temp_i)
        mu2 = mu2 + (np.abs(temp) - (np.abs(ca(i1)) ** 2))
        mu = mu + ca(i1)
    
    mu2 = mu2 / stop
    mu = np.abs(complex(real(mu) / stop,imag(mu) / stop))
    temp = np.abs(mean(ca(i1)))
    return mu,mu2
    
    return mu,mu2