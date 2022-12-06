# функция вычисления значения хи2 и определения значения согласия
# вход:
#  hist - массив гистограммы
#  hist_num - массив значений попаданий в интервалы гистограммы
# alpha - параметр значимости
# выход:
# rez: - 0 - согласуется с нормальным законом
#        1 - не согласуется с нормальным законом
#################################################################################################

import numpy as np
import math


def CalcXi2(histogra=None, hist_num=None, alpha=None):
    rez = 0
# расчет критерия хи2
# xia = 1-2*
#xi2_board = 0.5*((sqrt(2*m-1)+0.18) ^ 2)
    num_hist = np.asarray(hist_num).size
    #histogra = normrnd(3,1,1,numel(histogra));
#histogra = rand(1,numel(histogra));
# hist_num=hist(histogra,num_hist);

    re_max = np.amax(histogra.real)
    re_min = np.amin(histogra.real)
    # if(re_max<re_min)re_max=re_min;end;
    step = np.abs(re_max - re_min) / num_hist
    # histogra=abs(histogra)./re_max;
    var_norm = np.var(histogra)
    mean_norm = np.mean(histogra.real)
    # var_norm=1;
# mean_norm=3;

    # re=zeros(num,1);
# re=real(mas);
# общее кол-во попаданий в интервалы
    num = 0
    for i in np.arange(1, num_hist+1).reshape(-1):
        num = num + hist_num(i)

    # num=num*2;
    xi2 = np.zeros((num_hist, 1))
    p_i = np.zeros((num_hist, 1))
    x1 = re_min
    x2 = re_min + step
    for i in np.arange(1, num_hist+1).reshape(-1):
        a = (x2 - mean_norm) / np.sqrt(2 * var_norm)
        b = (x1 - mean_norm) / np.sqrt(2 * var_norm)
        r2 = math.erf(a)
        r1 = math.erf(b)
        p_i[i] = 0.5 * (math.erf(a) - math.erf(b))
        x1 = x2
        x2 = x2 + step
        # (1/sqrt(2*pi*1))*exp(-(hist_num(i)^2)/2);

    # hist_num=hist(histogra,10)./num;
# hist_num=hist_num./num;

    # расчет значения ХИ2
    xi_2 = 0
    xi_2_alt = 0
    # double a=0;
    # массив вероятности
    xi2_alt = np.zeros((num_hist, 1))
    for i in np.arange(1, num_hist+1).reshape(-1):
        # p_i(i)=(1/sqrt(2*pi*var_norm))*exp(-0.5*(((mean_norm-i/num_hist)^2)/(var_norm)));
        #  p_i(i)=0.5*(erf(((i)-mean_norm)/sqrt(2*var_norm))-erf(((i-1)-mean_norm)/sqrt(2*var_norm))  );
        #  2
        if (hist_num(i) != 0):
            # a=hist(i);
            #  a=num*a;
            #   c=hist_num(i);
            #    a=c-a;
            # a=a^2;
            #  b=num*hist(i);
            xi2[i] = ((hist_num[i] - p_i[i] * num) ** 2) / (p_i[i] * num)
            # xi2_alt(i)=(hist_num(i)^2)/(hist(i)*num)-hist_num(i)*2+hist(i)*num;
            xi2_alt[i] = (hist_num[i] ** 2) / (p_i[i] * num)
        else:
            xi2[i] = 0
            xi2_alt[i] = 0
        xi_2 = xi_2 + xi2[i]
        xi_2_alt = xi_2_alt + xi2_alt[i]

    xi_2_alt = xi_2_alt - num
    # subplot(325); stem(xi2);
#subplot(326); stem(hist_num);
    rez = xi_2
    return rez
