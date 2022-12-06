#функция добавления постоянной составляющей сигнала
# вход: 1) buf - массив сигнала в комплексном виде
#
# выход: 1)rez - массив сигнала с добавленной постоянной сотавляющей в комплексном виде
#
#***************************************************************************

import numpy as np
    
def AddConst(buf = None): 
    #####################################################################
    #увеличение постоянной составляющей сигнала
    min_re = np.amin(buf.real)
    min_im = np.amin(buf.imag)
    rez = np.zeros((np.asarray(buf).size,1))
    const_min = complex(np.abs(min_re),np.abs(min_im))
    N_sample = np.asarray(buf).size
    for i in np.arange(1,N_sample+1).reshape(-1):
        rez[i] = buf[i] + const_min
    return rez
    
    #####################################################################