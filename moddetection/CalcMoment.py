# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# расчет статистических моментов выборки
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# вход:
# 1) массив случайных величин
# 2) массив гистограммы случайного процесса
# 3) порядок расчитываемого момента
# выход:
# массив значений моментов по возрастанию
#########################################################################
import numpy as np
from ComplextoReal import ComplextoReal


def CalcMoment(va=None, histy=None, rang=None):
    mu = np.zeros((rang, 1))
    # rr=real(ca);
# ii=imag(ca);
# ra=mean(rr);
# ri=mean(ii);
# mi=mean(ca);
# means_i=abs(ri+i*mi);
# means_re=mean(ca);

    # ca_complex=ca;
    ca = ComplextoReal(va)
    # ca=real(va);
# ca=va;
    stop = np.asarray(ca).size
    ca_p = np.zeros((1, stop))

    ca = np.sort(ca)
    mu_0 = np.mean(ca)
    mu_1 = np.var(ca)
    stop2 = stop
    i = 1
    while (i < stop2):

        y = i
        while (ca[y] == ca[y + 1] and (y + 1) < stop2):

            y = y + 1
            ca_p[y] = 0

        z = y - i + 1
        ca_p[i] = z / stop2
        i = y + 1

    if (ca[y] != ca[stop2]):
        ca_p[stop2] = 1 / stop2
    else:
        z = z + 1
        ca_p[stop2 - z + 1] = z / stop2

    mu_n_1 = 0
    for n in np.arange(1, rang+1).reshape(-1):
        for i in np.arange(1, stop+1).reshape(-1):
            if (ca_p(i) != 0):
                mu[n] = mu[n] + ((ca[i] - mu_n_1) ** n) * (ca_p[i])
        mu_n_1 = mu[1]
        # mu(n)=abs(mu(n));

    # mu(1)= abs (mu(1))
# mu(2)=abs (mu(2));

    return mu
