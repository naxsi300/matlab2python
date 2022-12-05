import numpy as np
    
def fSpectrum(y = None,N = None,fs = None): 
    y = np.transpose(y)
    vf = (np.arange(0,N / 2+1)) * fs / N
    vf = (np.arange(0,int(np.floor(N / 2))+1)) * fs / N
    Sp = np.abs(np.fft.rfft(y)) ** 2 / (N * fs)
    Sp = Sp(np.arange(1,int(np.floor(N / 2)) + 1+1))
    return Sp,vf