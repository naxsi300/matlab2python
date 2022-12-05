#
#:
#  buf_signal -
#     -8 |W(d)|-> disp=2.1876 ; abs_disp=0.0733
#:
#   :
# 0 -
# 1 - -
# 2 - -
# 3 - FSK, GFSK
# 4 - GMSK
#################################################################################################

import numpy as np
    
def GetTypeModulation(buf_signal = None,T1cum = None,T2cum = None): 
    # haar T1=2.1876;
#dmey
    T1 = 2.121
    #  haar T2=0.0733;
#dmey
    T2 = 0.071
    #  psk  2    2000   3
    minPSK = 504
    maxPSK = 6080
    #    2    2000   3
    maxQAM = 168
    minQAM = 5
    #  FSK  2    2000   3
    minFSK = 80
    #maxFSK=480;
    maxFSK = 2757
    #  GMSK  2    2000   3
    minGMSK = 82
    maxGMSK = 595
    type_ = 0
    ###############################################################################################55
    
    va1,vd1 = dwt(buf_signal,'dmey')
    
    histogramm_va,m_va,histogramm_va_num = hist_complex(va1,10)
    histogramm_vd,m_vd,histogramm_vd_num = hist_complex(vd1,10)
    #   2
#:
#  hist -
#  hist_num -
# alpha -
#:
# rez: - 0 -
#        1 -
#################################################################################################
    
    xi = CalcXi2(va1,histogramm_va_num,0.1)
    
    #histogramm_vd=AprocsimMassiv(histogramm_vd,0.1);
#histogramm_va=AprocsimMassiv(histogramm_va,0.1);
    
    #**************************************************************************
#  -
# : 1) hist -
#       2) size_mas -   hist
# : N_peak -
#**************************************************************************
    Num_peak_va = CalcNumPeakHist(histogramm_va,np.asarray(histogramm_va).size)
    Num_peak_vd = CalcNumPeakHist(histogramm_vd,np.asarray(histogramm_vd).size)
    #########################################################################
    
    #########################################################################
# :
# 1)
# 2)
# 3)
# :
    
    #########################################################################
    mu_n = CalcMoment(va1,histogramm_va,8)
    ##################################################################################################
    
    #:
#   mas -
    
    #:
#   disp2 -
#   abs_disp2 -
#################################################################################################
    
    #[var_1, var_abs,var_2, var_abs2]=haar_norm_var (buf_signal_orig);
    disp,abs_disp = haar_norm_var(buf_signal)
    #      PSK
    if (Num_peak_va == Num_peak_vd and Num_peak_va == 1):
        #  PSK
        if ((disp < T1 and abs_disp < T2) and (mu_n(2) < T2cum) and (xi > maxQAM)):
            #psk
            type_ = 2
        else:
            #KAM
            if (minQAM < xi and xi < maxQAM):
                type_ = 1
                return type_,xi
            #FSK
            if (minFSK < xi and xi < maxFSK):
                type_ = 3
                return type_,xi
        return type_,xi
    
    ############################################################
    
    
    if ((disp > T1 and abs_disp > T2) or (minQAM < xi and xi < maxQAM)):
        #KAM
        type_ = 1
        return type_,xi
    
    #  GFSK
#if ((Num_peak_vd>1 && Num_peak_va>1) && (disp<T1 && abs_disp>T2) && ( minFSK<xi && xi<maxFSK) )
    if ((Num_peak_va > 1) and (disp < T1 and abs_disp > T2) and (minFSK < xi and xi < maxFSK)):
        #if ((disp<T1 && abs_disp<T2)&&( minFSK<xi && xi<maxFSK) )
#  M-GFSK
        type_ = 3
        return type_,xi
    
    #  GMSK
    if ((mu_n(2) > T1cum) and (minGMSK < xi and xi < maxGMSK)):
        type_ = 4
        return type_,xi
    
    #PSK
#if (( Num_peak_vd==1 && disp <T1 && abs_disp<T2) &&  ( (mu_n(2)<T2cum) && (xi>minPSK)))
    if ((Num_peak_vd == 1 and disp < T1) or ((mu_n(2) < T2cum) and (xi > minPSK))):
        #psk
        type_ = 2
        return type_,xi
    
    return type_,xi
    return type_,xi
    
    return type,xi