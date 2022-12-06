# функция определения типа модуляции
# вход:
#  buf_signal - массив комплексного сигнала
# пороговые значения взяты для КАМ-8 |W(d)|-> disp=2.1876 ; abs_disp=0.0733
# выход:
# тип модуляции :
# 0 - неопределен
# 1 - КАМ-М
# 2 - ФМ-М
# 3 - FSK, GFSK
# 4 - GMSK
#################################################################################################

import numpy as np
import pywt

from hist_complex import hist_complex
from CalcXi2 import CalcXi2
from CalcNumPeakHist import CalcNumPeakHist
from CalcMoment import CalcMoment
from haar_norm_var import haar_norm_var


def GetTypeModulation(buf_signal=None, T1cum=None, T2cum=None):
    # haar T1=2.1876;
    # dmey
    T1 = 2.121
    #  haar T2=0.0733;
# dmey
    T2 = 0.071
    # минимальный порог psk по хи2 для выборки в 2000 значений до 3 Дб
    minPSK = 504
    maxPSK = 6080
    # максимальный порог КАМ по хи2 для выборки в 2000 значений до 3 Дб
    maxQAM = 168
    minQAM = 5
    # максимальный порог FSK по хи2 для выборки в 2000 значений до 3 Дб
    minFSK = 80
    # maxFSK=480;
    maxFSK = 2757
    # максимальный порог GMSK по хи2 для выборки в 2000 значений до 3 Дб
    minGMSK = 82
    maxGMSK = 595
    type_ = 0
    # 55
    # проверка на КАМ по методу пиков гистограммы
    va1, vd1 = pywt.dwt(buf_signal, 'dmey')
    # построение гистограммы
    histogramm_va, m_va, histogramm_va_num = hist_complex(va1, 10)
    histogramm_vd, m_vd, histogramm_vd_num = hist_complex(vd1, 10)

    # функция вычисления значения хи2 и определения значения согласия
    # вход:
    #  hist - массив сигнала
    #  hist_num - массив значений попаданий в интервалы гистограммы
    # alpha - параметр значимости
    # выход:
    # rez: - 0 - согласуется с нормальным законом
    #        1 - не согласуется с нормальным законом
#################################################################################################

    xi = CalcXi2(va1, histogramm_va_num, 0.1)


# апроксимация гистограмм
#histogramm_vd = AprocsimMassiv(histogramm_vd, 0.1)
#histogramm_va = AprocsimMassiv(histogramm_va, 0.1)

# **************************************************************************
# функция определение кол-ва пиков гистограмм
# вход: 1) hist - массив гистограммы
#       2) size_mas - размер массива hist
# выход: N_peak - количество пиков
# **************************************************************************
    Num_peak_va = CalcNumPeakHist(
        histogramm_va, np.asarray(histogramm_va).size)
    Num_peak_vd = CalcNumPeakHist(
        histogramm_vd, np.asarray(histogramm_vd).size)

    #########################################################################
    # расчет статистических моментов выборки
    #########################################################################
# вход:
# 1) массив случайных величин
# 2) массив гистограммы случайного процесса
# 3) порядок расчитываемого момента
# выход:
#   массив значений моментов по возрастанию
    #########################################################################
    mu_n = CalcMoment(va1, histogramm_va, 8)

    ##################################################################################################
# функция расчета дисперсии вейвлета Хаара от вещественного сигнала и нормированного к его амплитуде
# вход:
#   mas - массив случайной комплексной величины
# выход:
#   disp2 - модуль дисперрсии вейвлета Хаара вещественного сигнала
#   abs_disp2 - модуль дисперрсии вейвлета Хаара нормированного сигнала
#################################################################################################

    #[var_1, var_abs,var_2, var_abs2]=haar_norm_var (buf_signal_orig);
    disp, abs_disp = haar_norm_var(buf_signal)
    # по методу гистограмм определяем КАМ или PSK
    if (Num_peak_va == Num_peak_vd and Num_peak_va == 1):
        # проверка на PSK
        if ((disp < T1 and abs_disp < T2) and (mu_n(2) < T2cum) and (xi > maxQAM)):
            # psk
            type_ = 2
        else:
            # KAM
            if (minQAM < xi and xi < maxQAM):
                type_ = 1
                return type_, xi
            # FSK
            if (minFSK < xi and xi < maxFSK):
                type_ = 3
                return type_, xi
        return type_, xi

    ############################################################
    # по анализу модуля дисперсии вейвлет преобразований сигнала
    # проверка на КАМ
    if ((disp > T1 and abs_disp > T2) or (minQAM < xi and xi < maxQAM)):
        # KAM
        type_ = 1
        return type_, xi

    # проверка на GFSK
# if ((Num_peak_vd>1 && Num_peak_va>1) && (disp<T1 && abs_disp>T2) && ( minFSK<xi && xi<maxFSK) )
    if ((Num_peak_va > 1) and (disp < T1 and abs_disp > T2) and (minFSK < xi and xi < maxFSK)):
        # if ((disp<T1 && abs_disp<T2)&&( minFSK<xi && xi<maxFSK) )
        # тип M-GFSK
        type_ = 3
        return type_, xi

    # проверка на GMSK
    if ((mu_n(2) > T1cum) and (minGMSK < xi and xi < maxGMSK)):
        type_ = 4
        return type_, xi

    # PSK
# if (( Num_peak_vd==1 && disp <T1 && abs_disp<T2) &&  ( (mu_n(2)<T2cum) && (xi>minPSK)))
    if ((Num_peak_vd == 1 and disp < T1) or ((mu_n(2) < T2cum) and (xi > minPSK))):
        # psk
        type_ = 2
        return type_, xi

    return type_, xi
