#
# : 1) Name_gmsk -       GMSK
#       2) Name_fsk -
#       N-fsk+m ( N -  fsk)
#       3) Name_psk -       psk+m
#       4) Name_qam -       qam+m
# : 1)   GMSC  FSK (T1)
#        2)   PSK  QAM (2)
#        3)    -FSK(Tfr)
#        4)    -QAM(Tqr)
#        5)    -PSK(Tpr)
#        6)    M-QAM
#        7)    M-PSK
#        8)    M-FSK
#***************************************************************************

import numpy as np
    
def CalcT(Name_gmsk = None,Name_fsk = None,Name_psk = None,Name_qam = None): 
    #   ,  r_... -  2^r_...
    r_fsk = 7
    r_psk = 7
    r_qam = 11
    
    #     GMSK
    mu_gmsk = np.zeros((8,1))
    fid2 = open(Name_gmsk,'r')
    #for z=1:8
#    re=fread(fid2,1,'float32');
#    im=fread(fid2,1,'float32');
#    mu_gmsk(z)= complex(re,im);
#    end;
    mu_gmsk = fread(fid2,8,'double')
    fid2.close()
    mu_gmsk = np.abs(mu_gmsk)
    ###########################################################################
#     FSK
#n- -   2^n-FSK
    mu_fsk = np.zeros((r_fsk + 1,8))
    
    for r in np.arange(1,r_fsk+1).reshape(-1):
        strok = int2str(2 ** r)
        fid2 = open(strcat(strok,'-',Name_fsk),'r')
        #    for z=1:8
#    re=fread(fid2,1,'float32');
#    im=fread(fid2,1,'float32');
#    mu_fsk(r,z)= complex(re,im);
#    end;
        mu_fsk[r,:] = fread(fid2,8,'double')
        fid2.close()
    
    #mu_fsk=abs(mu_fsk);
#mu_fsk=mu_fsk';
##########################################################################
#   PSK
    mu_psk = np.zeros((r_psk + 1,8))
    
    for r in np.arange(1,r_psk+1).reshape(-1):
        strok = int2str(2 ** r)
        fid2 = open(strcat(strok,'-',Name_psk),'r')
        # for z=1:8
# re=fread(fid2,1,'float32');
# im=fread(fid2,1,'float32');
# mu_psk(r,z)= complex(re,im);
# end;
        mu_psk[r,:] = fread(fid2,8,'double')
        fid2.close()
    
    #mu_psk=abs(mu_psk);
#temp=mu_psk;
#mu_psk=mu_psk';
#   QAM
    mu_qam = np.zeros((r_qam + 1,8))
    
    for r in np.arange(3,r_qam+1).reshape(-1):
        strok = int2str(2 ** (r))
        fid2 = open(strcat(strok,'-',Name_qam),'r')
        # if(r==12)
#    r=12;
#end;
# for z=1:8
#   re=fread(fid2,1,'float32');
#   im=fread(fid2,1,'float32');
#    mu_qam(r,z)= complex(re,im);
#   end;
        mu_qam[r - 2,:] = fread(fid2,8,'double')
        fid2.close()
    
    #mu_qam=mu_qam';
#    FSK
#mu_qam=abs(mu_qam);
    
    # 1
    moment_rang = 4
    moment_m = 2
    T1 = (mu_gmsk(moment_m) * mu_fsk(1,moment_rang) + mu_fsk(1,moment_m) * mu_gmsk(moment_rang)) / (mu_gmsk(moment_rang) + mu_fsk(1,moment_rang))
    #T1=mu_gmsk(2);
    
    #n- -   2^n-FSK
    Tfr = np.zeros((r_fsk + 1,8))
    # fr(fsk)
    moment_rang = 8
    for r in np.arange(2,2+1).reshape(-1):
        #for r=1:1
        for n in np.arange(1,r_fsk+1).reshape(-1):
            #   Tfr(n,r)=(mu_fsk(1,r)*mu_fsk(2,r+1)+mu_fsk(1,r+1)*mu_fsk(2,r))/(mu_fsk(2,r+1)+mu_fsk(2,r+1));
#Tfr(r,n)=abs( (mu_fsk(n,r+moment_rang)*mu_fsk(n+1,r+moment_rang+1)+mu_fsk(n,r+moment_rang+1)*mu_fsk(n+1,r+moment_rang))/(mu_fsk(n,r+moment_rang+1)+mu_fsk(n,r+moment_rang+1)) );
#Tqr(r,n)=(mu_qam(n,r+moment_rang)*mu_qam(n+1,r+moment_rang+1)+mu_qam(n,r+moment_rang+1)*mu_qam(n+1,r+moment_rang))/(mu_qam(n,r+moment_rang+1)+mu_qam(n+1,r+moment_rang+1));
            m11 = mu_fsk(n,r)
            mn22 = mu_fsk(n + 1,moment_rang)
            m21 = mu_fsk(n + 1,r)
            mn12 = mu_fsk(n,moment_rang)
            #Tfr(r,n)= (mu_fsk(n,r)*mu_fsk(n+1,moment_rang)+mu_fsk(n,moment_rang)*mu_fsk(n+1,r))/(mu_fsk(n,moment_rang)+mu_fsk(n+1,moment_rang)) ;
            Tfr[r,n] = (mu_fsk(n,r) * mu_fsk(n + 1,moment_rang) + mu_fsk(n,moment_rang) * mu_fsk(n + 1,r)) / (mu_fsk(n,moment_rang) + mu_fsk(n + 1,moment_rang))
    
    #n- -   2^(n+2)-QAM
    Tqr = np.zeros((8,r_qam))
    # qr(qam)
    moment_rang = 8
    for r in np.arange(6,6+1).reshape(-1):
        #for r=1:1
        for n in np.arange(1,r_qam - 2+1).reshape(-1):
            a11 = mu_qam(n,r)
            a22 = mu_qam(n + 1,moment_rang)
            a21 = mu_qam(n + 1,r)
            a12 = mu_qam(n,moment_rang)
            #  Tqr(r,n)=(mu_qam(n,r)*mu_qam(n+1,moment_rang)+mu_qam(n,moment_rang)*mu_qam(n+1,r))/(mu_qam(n,moment_rang)+mu_qam(n+1,moment_rang));
            Tqr[r,n] = (mu_qam(n,r) * mu_qam(n + 1,moment_rang) + mu_qam(n,moment_rang) * mu_qam(n + 1,r)) / (mu_qam(n,moment_rang) + mu_qam(n + 1,moment_rang))
    
    # 2
    moment_rang = 2
    
    #T2=(mu_psk(1,1)*mu_qam(1,moment_rang)+mu_qam(1,1)*mu_psk(1,moment_rang))/(mu_psk(1,moment_rang)+mu_qam(1,moment_rang));
    
    T2 = mu_qam(1,2)
    #T2=(mu_qam(1,1)*mu_psk(1,moment_rang)+mu_qam(1,moment_rang)*mu_psk(1,1))/(mu_qam(1,moment_rang)+mu_psk(1,moment_rang));
    
    #n- -   2^n-PSK
    Tpr = np.zeros((8,r_psk))
    moment_rang = 4
    for r in np.arange(2,2+1).reshape(-1):
        #for r=1:1
        for n in np.arange(1,r_psk - 1+1).reshape(-1):
            a11 = mu_psk(n,r)
            a22 = mu_psk(n + 1,moment_rang)
            a21 = mu_psk(n + 1,r)
            a12 = mu_psk(n,moment_rang)
            #  Tqr(r,n)=(mu_qam(n,r)*mu_qam(n+1,moment_rang)+mu_qam(n,moment_rang)*mu_qam(n+1,r))/(mu_qam(n,moment_rang)+mu_qam(n+1,moment_rang));
            Tpr[r,n] = (mu_psk(n,r) * mu_psk(n + 1,moment_rang) + mu_psk(n,moment_rang) * mu_psk(n + 1,r)) / (mu_psk(n,moment_rang) + mu_psk(n + 1,moment_rang))
    
    #T1=abs(T1);
#T2=real(T2);
#Tfr=abs(Tfr);
#Tqr=abs(Tqr);
#Tpr=real(Tpr);
    
    return T1,T2,Tfr,Tqr,Tpr,mu_qam,mu_psk,mu_fsk
    
    return T1,T2,Tfr,Tqr,Tpr,mu_qam,mu_psk,mu_fsk