###################################################################
#
#
#:
#   1)     () presition
#   2)   moment[]
#   3)   Tx[]
#   4)    r_max
#   5)   +/- direct
#   6)   M-
# :
#   1)    r (  0 -      )
#####################################################################




import numpy as np
    
def GetPositionModulateFSK(presition = None,moment = None,Tx = None,r_max = None,m_array = None): 
    t_real = np.zeros((r_max,1))
    #t_delta=zeros(r_max,1);
    moment_rang = presition
    shag = 2
    for i in np.arange(1,r_max - 1+1).reshape(-1):
        #   a=moment(moment_rang);
#    b=moment(moment_rang+1);
        #  moment(moment_rang)=0.0004;
# moment(moment_rang+1)=0.0066;
        #     a11= moment(moment_rang-shag);
# a22=m_array(i+1,moment_rang);
#a21=m_array(i+1,moment_rang-shag);
#a12=moment(moment_rang);
        t_real[i] = (moment(moment_rang - shag) * m_array(i + 1,moment_rang) + moment(moment_rang) * m_array(i + 1,moment_rang - shag)) / (moment(moment_rang) + m_array(i + 1,moment_rang))
        #   t_real(i)=(moment(moment_rang-shag)*m_array(i+1,moment_rang)+m_array(i,moment_rang)*m_array(i+1,moment_rang-shag))/(m_array(i,moment_rang)+m_array(i+1,moment_rang));
        #t_real(i)=(moment(moment_rang+1)*m_array(i,moment_rang+2)+moment(moment_rang+2)*m_array(i,moment_rang+1))/(moment(moment_rang+2)+m_array(i,moment_rang+2));
        t_delta[i] = np.abs(t_real(i) - Tx(i))
    
    x = 0
    for r in np.arange(1,np.asarray(Tx).size+1).reshape(-1):
        if (t_real(r) <= Tx(r)):
            if (x == 1 and (Tx(r) - t_real(r)) > delta_1):
                rez = r - 1
            else:
                rez = r
            break
        else:
            delta_1 = t_real(r) - Tx(r)
            delta_2 = (Tx(r) + Tx(r + 1)) / 2
            if (delta_1 < delta_2):
                x = 1
            else:
                x = 0
    
    #    delta=t_delta(1);
#   for i=1:r_max-1
#    if(delta>t_delta(i))
#     delta=t_delta(i);
#    r=i;
# end;
    
    # end;
    
    
    #r=2;
#if(direct>0)
    
    #   while  (moment (presition)< Tx(r) && r<r_max)
#      r=r+1;
# end;
#else
    
    #   while  (moment (presition)> Tx(r)&& r<r_max )
#      r=r+1;
# end;
#end;
    
    ############################################
    return rez
    
    return rez