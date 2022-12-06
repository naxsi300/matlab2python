# функция расчета пороговых значений для критерия принятия решения
# вход: 1) Name_gmsk - имя файла со значениями моментов эталонов GMSK
# 2) Name_fsk - шаблон имени файлов для значений моментов эталонов
# N-fsk+m(где N - позиционность fsk)
# 3) Name_psk - имя файла со значениями моментов эталонов psk+m
# 4) Name_qam - имя файла со значениями моментов эталонов qam+m
# выход: 1)Расчет порога опредления GMSC или FSK(T1)
# 2)Расчет порога опредления PSK или QAM(Т2)
# 3)Расчет порогов опредления для М-FSK(Tfr)
# 4)Расчет порогов опредления для М-QAM(Tqr)
# 5)Расчет порогов опредления для М-PSK(Tpr)
# 6)массив значений моментов эталонов M-QAM
# 7)массив значений моментов эталонов M-PSK
# 8)массив значений моментов эталонов M-FSK
# ***************************************************************************

import numpy as np


def CalcT_haar(Name_gmsk=None, Name_fsk=None, Name_psk=None, Name_qam=None):
    # диапозон определения позиционности сигналов, где r_... - позиционность 2^r_...
    r_fsk = 4
    r_psk = 5
    r_qam = 11

    # считывание моментов эталонов сигнала GMSK
    mu_gmsk = np.zeros((8, 1))
    fid2 = open(Name_gmsk, 'rb')
    # for z=1:8
#    re=fread(fid2,1,'float32');
#    im=fread(fid2,1,'float32');
#    mu_gmsk(z)= complex(re,im);
#    end;
    mu_gmsk = np.fromfile(fid2, np.double, 8)
    fid2.close()
    mu_gmsk = np.abs(mu_gmsk)
    ###########################################################################
# считывание моментов эталонов сигнала FSK
# n-я строка- моменты для 2^n-FSK
    mu_fsk = np.zeros((r_fsk + 1, 8))  # r=4

    for r in np.arange(1, r_fsk+1).reshape(-1):
        strok = 2 ** r
        fid2 = open(str(strok) + '-' + Name_fsk, 'rb')
        #    for z=1:8
#    re=fread(fid2,1,'float32');
#    im=fread(fid2,1,'float32');
#    mu_fsk(r,z)= complex(re,im);
#    end;
        mu_fsk[r, :] = np.fromfile(fid2, np.double, 8)
        fid2.close()

    # mu_fsk=abs(mu_fsk);
# mu_fsk=mu_fsk';
##########################################################################
#   PSK
    mu_psk = np.zeros((r_psk + 1, 8))

    for r in np.arange(1, r_psk+1).reshape(-1):
        strok = 2 ** r
        fid2 = open(str(strok) + '-' + Name_psk + 'rb')
        # for z=1:8
# re=fread(fid2,1,'float32');
# im=fread(fid2,1,'float32');
# mu_psk(r,z)= complex(re,im);
# end;
        mu_psk[r, :] = np.fromfile(fid2, np.double, 8)
        fid2.close()

    # mu_psk=abs(mu_psk);
# temp=mu_psk;
# mu_psk=mu_psk';
# моменты эталонов сигнала QAM
    mu_qam = np.zeros((r_qam + 1, 8))

    for r in np.arange(3, r_qam+1).reshape(-1):
        strok = 2 ** (r)
        fid2 = open(str(strok) + '-' + Name_qam + 'rb')
        # if(r==12)
#    r=12;
# end;
# for z=1:8
#   re=fread(fid2,1,'float32');
#   im=fread(fid2,1,'float32');
#    mu_qam(r,z)= complex(re,im);
#   end;
        mu_qam[r - 2, :] = np.fromfile(fid2, np.double, 8)
        fid2.close()

    # mu_qam=mu_qam';
# пороги для определения позиционности FSK
# mu_qam=abs(mu_qam);

    # Расчет Т1
    moment_rang = 4
    moment_m = 2
    T1 = (mu_gmsk[moment_m] * mu_fsk[1, moment_rang] + mu_fsk[1, moment_m] *
          mu_gmsk[moment_rang]) / (mu_gmsk(moment_rang) + mu_fsk[1, moment_rang])
    # T1=mu_gmsk(2);

    # n-я строка- пороги для 2^n-FSK
    Tfr = np.zeros((r_fsk + 1, 8))
    # Расчет Тfr(fsk)
    moment_rang = 8
    for r in np.arange(6, 6+1).reshape(-1):
        # for r=1:1
        for n in np.arange(1, r_fsk+1).reshape(-1):
            #   Tfr(n,r)=(mu_fsk(1,r)*mu_fsk(2,r+1)+mu_fsk(1,r+1)*mu_fsk(2,r))/(mu_fsk(2,r+1)+mu_fsk(2,r+1));
            # Tfr(r,n)=abs( (mu_fsk(n,r+moment_rang)*mu_fsk(n+1,r+moment_rang+1)+mu_fsk(n,r+moment_rang+1)*mu_fsk(n+1,r+moment_rang))/(mu_fsk(n,r+moment_rang+1)+mu_fsk(n,r+moment_rang+1)) );
            # Tqr(r,n)=(mu_qam(n,r+moment_rang)*mu_qam(n+1,r+moment_rang+1)+mu_qam(n,r+moment_rang+1)*mu_qam(n+1,r+moment_rang))/(mu_qam(n,r+moment_rang+1)+mu_qam(n+1,r+moment_rang+1));
            m11 = mu_fsk(n, r)
            mn22 = mu_fsk(n + 1, moment_rang)
            m21 = mu_fsk(n + 1, r)
            mn12 = mu_fsk(n, moment_rang)
            # Tfr(r,n)= (mu_fsk(n,r)*mu_fsk(n+1,moment_rang)+mu_fsk(n,moment_rang)*mu_fsk(n+1,r))/(mu_fsk(n,moment_rang)+mu_fsk(n+1,moment_rang)) ;
            Tfr[r, n] = (mu_fsk[n, r] * mu_fsk[n + 1, moment_rang] + mu_fsk[n, moment_rang]
                         * mu_fsk[n + 1, r]) / (mu_fsk[n, moment_rang] + mu_fsk[n + 1, moment_rang])

    # n-я строка- пороги для 2^(n+2)-QAM
    Tqr = np.zeros((8, r_qam))
    # qr(qam)
    moment_rang = 8
    for r in np.arange(6, 6+1).reshape(-1):
        # for r=1:1
        for n in np.arange(1, r_qam - 2+1).reshape(-1):
            # a11 = mu_qam(n, r)
            # a22 = mu_qam(n + 1, moment_rang)
            # a21 = mu_qam(n + 1, r)
            # a12 = mu_qam(n, moment_rang)
            #  Tqr(r,n)=(mu_qam(n,r)*mu_qam(n+1,moment_rang)+mu_qam(n,moment_rang)*mu_qam(n+1,r))/(mu_qam(n,moment_rang)+mu_qam(n+1,moment_rang));
            Tqr[r, n] = (mu_qam[n, r] * mu_qam[n + 1, moment_rang] + mu_qam[n, moment_rang]
                         * mu_qam[n + 1, r]) / (mu_qam[n, moment_rang] + mu_qam[n + 1, moment_rang])

    # Расчет Т2
    moment_rang = 2
    # сравнение сигналов с одинаковой позиционностью М
    # T2=(mu_psk(1,1)*mu_qam(1,moment_rang)+mu_qam(1,1)*mu_psk(1,moment_rang))/(mu_psk(1,moment_rang)+mu_qam(1,moment_rang));

    T2 = mu_qam[1, 2]
    # T2=(mu_qam(1,1)*mu_psk(1,moment_rang)+mu_qam(1,moment_rang)*mu_psk(1,1))/(mu_qam(1,moment_rang)+mu_psk(1,moment_rang));

    # n-я строка- пороги для 2^n-PSK
    Tpr = np.zeros((8, r_psk))
    moment_rang = 8
    for r in np.arange(6, 6+1).reshape(-1):
        # for r=1:1
        for n in np.arange(1, r_psk - 1+1).reshape(-1):
            # a11 = mu_psk(n, r)
            # a22 = mu_psk(n + 1, moment_rang)
            # a21 = mu_psk(n + 1, r)
            # a12 = mu_psk(n, moment_rang)
            #  Tqr(r,n)=(mu_qam(n,r)*mu_qam(n+1,moment_rang)+mu_qam(n,moment_rang)*mu_qam(n+1,r))/(mu_qam(n,moment_rang)+mu_qam(n+1,moment_rang));
            Tpr[r, n] = (mu_psk[n, r] * mu_psk[n + 1, moment_rang] + mu_psk[n, moment_rang]
                         * mu_psk[n + 1, r]) / (mu_psk[n, moment_rang] + mu_psk[n + 1, moment_rang])

    # T1=abs(T1);
# T2=real(T2);
# Tfr=abs(Tfr);
# Tqr=abs(Tqr);
# Tpr=real(Tpr);

    return T1, T2, Tfr, Tqr, Tpr, mu_qam, mu_psk, mu_fsk
