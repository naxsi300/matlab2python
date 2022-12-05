#
# : 1) buf -
#
# : 1)rez -
#
#***************************************************************************

import numpy as np
    
def AddConst(buf = None): 
    #####################################################################
    
    min_re = np.amin(real(buf))
    min_im = np.amin(imag(buf))
    rez = np.zeros((np.asarray(buf).size,1))
    const_min = complex(np.abs(min_re),np.abs(min_im))
    N_sample = np.asarray(buf).size
    for i in np.arange(1,N_sample+1).reshape(-1):
        rez[i] = buf(i) + const_min
    
    return rez
    
    #####################################################################
    return rez