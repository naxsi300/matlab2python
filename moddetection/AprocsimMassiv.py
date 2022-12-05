#
# : 1) massiv -
#       2) kof -
# : 1)rez -
#
#***************************************************************************

import numpy as np
    
def AprocsimMassiv(massiv = None,kof = None): 
    rez = massiv
    mx = np.amax(rez)
    mx = mx * kof
    c = np.asarray(rez).size
    for i in np.arange(1,c+1).reshape(-1):
        if rez(i) < mx:
            rez[i] = 0
    
    return rez