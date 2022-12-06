###################################################################
# функция выбора позиционности модуляции по заданному критерию и номеру
# момента
# вход:
#   1) номер момента для выбора(точность) presition
# 2) массив моментов moment[]
# 3) массив критериев Tx[]
# 4) размер массива критериев r_max
# 5) условие выбора + /- direct
# 6) массив моментов M-модуляций
# выход:
# 1) степень позиционности модуляции r(если возврат 0 - то позиционность модуляции не определена)
#####################################################################


import numpy as np


def GetPositionModulateFSK(presition=None, moment=None, Tx=None, r_max=None, m_array=None):
    t_real = t_delta = np.zeros((r_max, 1))
    # t_delta=zeros(r_max,1);
    moment_rang = presition
    shag = 2
    for i in np.arange(1, r_max - 1+1).reshape(-1):
        # показателя для сравнения
        #   a=moment(moment_rang);
        #    b=moment(moment_rang+1);
        #  moment(moment_rang)=0.0004;
        # moment(moment_rang+1)=0.0066;
        #     a11= moment(moment_rang-shag);
        # a22=m_array(i+1,moment_rang);
        # a21=m_array(i+1,moment_rang-shag);
        # a12=moment(moment_rang);
        t_real[i] = (moment[moment_rang - shag] * m_array[i + 1, moment_rang] + moment[moment_rang]
                     * m_array[i + 1, moment_rang - shag]) / (moment[moment_rang] + m_array[i + 1, moment_rang])
        #   t_real(i)=(moment(moment_rang-shag)*m_array(i+1,moment_rang)+m_array(i,moment_rang)*m_array(i+1,moment_rang-shag))/(m_array(i,moment_rang)+m_array(i+1,moment_rang));
        # t_real(i)=(moment(moment_rang+1)*m_array(i,moment_rang+2)+moment(moment_rang+2)*m_array(i,moment_rang+1))/(moment(moment_rang+2)+m_array(i,moment_rang+2));
        t_delta[i] = np.abs(t_real[i] - Tx[i])

    x = 0
    for r in np.arange(1, np.asarray(Tx).size+1).reshape(-1):
        if (t_real[r] <= Tx[r]):
            if (x == 1 and (Tx[r] - t_real[r]) > delta_1):
                rez = r - 1
            else:
                rez = r
            break
        else:
            delta_1 = t_real[r] - Tx[r]
            delta_2 = (Tx[r] + Tx[r + 1]) / 2
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

  # начало старого участка
# r=2;
# if(direct>0)
    # условие выбора по возрастанию момента
 #   while  (moment (presition)< Tx(r) && r<r_max)
  #      r=r+1;
   # end;
# else
    # условие выбора по убыванию момента
 #   while  (moment (presition)> Tx(r)&& r<r_max )
  #      r=r+1;
   # end;
# end;
# конец старого участка
    ############################################
    return rez
