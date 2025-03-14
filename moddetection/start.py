import numpy as np
import pywt

# for PyQT
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFileInfo
#####
# self-made functions
from CaclT import CalcT
from CaclT_haar import CalcT_haar
from AddConst import AddConst
from GetTypeModulation import GetTypeModulation
from hist_complex import hist_complex
from AprocsimMassiv import AprocsimMassiv
from CalcNumPeakHist import CalcNumPeakHist
from CalcMoment import CalcMoment
from CalcMu2 import CalcMu2
from ComplextoReal import ComplextoReal
from GetPositionModulate import GetPositionModulate
from GetPositionModulateFSK import GetPositionModulateFSK
from GetPositionModulatePSK import GetPositionModulatePSK
#
##############################################################################
# переменные
##############################################################################

# выбор файла


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Modulation detector'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        work(self.openFileNameDialog())
        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options)
        return fileName


def work(NameFile):
    # Returns the name of the file, excluding the path.
    Name = QFileInfo(NameFile).fileName
    # статистика пиков
    stat_Num_peak_va = 0
    stat_Num_peak_vd = 0
    stat_Num_peak_vax = 0
    stat_Num_peak_vdx = 0
    # открытие файла на чтение
    file = open(NameFile, 'rb')
    # функция расчета пороговых значений для критерия принятия решения
    # вход: 1) Name_gmsk - имя файла со значениями моментов эталонов GMSK
    #       2) Name_fsk - шаблон имени файлов для значений моментов эталонов
    #       N-fsk+m (где N - позиционность fsk)
    #       3) Name_psk - имя файла со значениями моментов эталонов psk+m
    #       4) Name_qam - имя файла со значениями моментов эталонов qam+m
    # выход: 1)Расчет порога опредления GMSC или FSK (T1)
    #        2)Расчет порога опредления PSK или QAM (Т2)
    #        3)Расчет порогов опредления для М-FSK(Tfr)
    #        4)Расчет порогов опредления для М-QAM(Tqr)
    #        5)Расчет порогов опредления для М-PSK(Tpr)
    #        6)массив значений моментов эталонов M-QAM
    #        7)массив значений моментов эталонов M-PSK
    #        8)массив значений моментов эталонов M-FSK
    # **************************************************************************
    T1, T2, Tfr, Tqr, Tpr, mqam, mpsk, mfsk = CalcT(
        'gmsk+8.bin', 'fsk+8.bin', 'psk+8.bin', 'qam+8.bin')
    # функция расчета пороговых значений для критерия принятия решения ПО ХААРУ
    # вход: 1) Name_gmsk - имя файла со значениями моментов эталонов GMSK
    #       2) Name_fsk - шаблон имени файлов для значений моментов эталонов
    #       N-fsk+m (где N - позиционность fsk)
    #       3) Name_psk - имя файла со значениями моментов эталонов psk+m
    #       4) Name_qam - имя файла со значениями моментов эталонов qam+m
    # выход: 1)Расчет порога опредления GMSC или FSK (T1)
    #        2)Расчет порога опредления PSK или QAM (Т2)
    #        3)Расчет порогов опредления для М-FSK(Tfr)
    #        4)Расчет порогов опредления для М-QAM(Tqr)
    #        5)Расчет порогов опредления для М-PSK(Tpr)
    #        6)массив значений моментов эталонов M-QAM
    #        7)массив значений моментов эталонов M-PSK
    #        8)массив значений моментов эталонов M-FSK
    # **************************************************************************
    T1_h, T2_h, Tfr_h, Tqr_h, Tpr_h, mqam_h, mpsk_h, mfsk_h = CalcT_haar(
        'gmsk+8.bin', 'fsk-haar-+8.bin', 'psk-haar-+8.bin', 'qam+8.bin')
    # запись коэффициентов вейвлет преобразований

    filenamea = Name + '.wvl'
    fda = open(filenamea, 'wb')
    filenameb = Name + '.wvh'
    fdb = open(filenameb, 'wb')
    ############################################

    N_sample = 2000
    # число блоков сигнала для расчета
    Num_block = 50
    # массив расчета результатов моментов до 8 порядка
    mu_n = np.zeros((Num_block, 8))
    mu_n_haar = np.zeros((Num_block, 8))
    mu_n_dmey = np.zeros((Num_block, 8))
    mu_n_ctrl = np.zeros((Num_block, 8))
    mu_n_temp = np.zeros((Num_block, 8))
    # параметр номировки сигнала

    buf_signal_orig = np.zeros((N_sample, 1))
    # кол-во решений по определению сигналов fsk из выборки
    p_good_fsk = 0
    # кол-во решений по определению сигналов psk из выборки
    p_good_psk = 0
    # кол-во решений по определению сигналов gmsk из выборки
    p_good_gmsk = 0
    # кол-во решений по определению сигналов qam из выборки
    p_good_qam = 0
    # решения по позиционности КАМ
    N_pos_qam = 12

    # решения по позиционности PSK
    N_pos_psk = 7

    p_pos_qam = np.zeros((N_pos_qam, 1))
    # решения по позиционности FSK
    N_pos_fsk = 5
    # массив кол-ва решений по определению порзиционности сигналов psk из выборки
    p_pos_fsk = np.zeros((11, 1))
    # решения по позиционности КАМ
    p_pos_psk = np.zeros((11, 1))
    # точность прияния решения через номер порядка момента
    precition_moment = 2
    # времянка массив значений хи2
    xi2 = np.zeros((Num_block, 1))
    # начало обработки блоков
    for x in np.arange(1, Num_block+1).reshape(-1):
        # считывание очередного блока сигнала
        # [buf_signal_orig_real]=fread(filex,N_sample,'float32');
        for kadr in np.arange(1, N_sample+1).reshape(-1):
            # считывание очередного блока сигнала
            RS = np.fromfile(file, np.float32, 1)
            IM = np.fromfile(file, np.float32, 1)
            buf_signal_orig[kadr] = complex(RS, IM)
        # /////////////////////////////////////////////
        buf_signal_real = buf_signal_orig
        # добавление постоянной составляющей
        buf_signal_orig = AddConst(buf_signal_orig)
        # 55
    # функция определения типа модуляции
    # вход:
    #  buf_signal - массив комплексного сигнала
    #  T1 - пороговое значение из метода моментов
    #  T2 - пороговое значение из метода моментов
        # пороговые значения взяты для КАМ-8 |W(d)|-> disp=2.988 ; abs_disp=0.0733
    # выход:
    # тип модуляции :
    # 0 - неопределен
    # 1 - КАМ-М
    # 2 - ФМ-М
    # 3 - FSK, GFSK,
    # 4 - GMSK
    #################################################################################################
        type_mod, x2 = GetTypeModulation(buf_signal_orig, T1, T2)
        xi2[x] = x2
        # ////////////////////////////////////////////
    # вейвлет преобразования 'dmey'
    # комплексный сигнал
        va1, vd1 = pywt.dwt(buf_signal_orig, 'dmey')
        # /////////////////////////////////////////////////////////
        a = np.mean(va1)
        b = np.var(va1)
        histogramm_va, m_va, xi2_va = hist_complex(va1, 10)
        histogramm_vd, m_vd, xi2_vd = hist_complex(vd1, 10)
        histogramm_vd = AprocsimMassiv(histogramm_vd, 0.1)
        histogramm_va = AprocsimMassiv(histogramm_va, 0.1)
        ####################################################################
    # определение кол-ва пиков гистограмм
    ####################################################################
    # **************************************************************************
    # функция определение кол-ва пиков гистограмм
    # вход: 1) hist - массив гистограммы
    #       2) size_mas - размер массива hist
    # выход: N_peak -количество пиков
    # **************************************************************************
        Num_peak_va = CalcNumPeakHist(
            histogramm_va, np.asarray(histogramm_va).size)
        Num_peak_vd = CalcNumPeakHist(
            histogramm_vd, np.asarray(histogramm_vd).size)
        # функция определения вида распределения по критерию хи-квадрат
    # вход: 1) massiv - массив выборки
    # выход: 1)массив результатов проврки гипотез:
    #           строки:
    #           1: Вид распределения (0-нормальное, 1-экспоненциальное, 2-вейбула, 4 - гамма распределение)
    #           2: вероятность подтверждения
    #           3: размер выборки
        # ***************************************************************************
        # статистика пиков
        if Num_peak_va > 1:
            stat_Num_peak_va = stat_Num_peak_va + 1
        if Num_peak_vd > 1:
            stat_Num_peak_vd = stat_Num_peak_vd + 1
        #########################################################################
    # расчет статистических моментов выборки
    #########################################################################
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
        mu_n[x, :] = CalcMoment(va1, histogramm_va, 8)
        mu, mu2 = CalcMu2(va1)
        modulation = 'no identification'
        # определние позиционности
        if 1 == type_mod:
            modulation = 'M-QAM '
            p_good_qam = p_good_qam + 1
            ###################################################################
    # функция выбора позиционности модуляции по заданному критерию и номеру
    # момента
    # вход:
    #   1) номер момента для выбора (точность) presition
    #   2) массив моментов moment[]
    #   3) массив критериев Tx[]
    #   4) размер массива критериев r_max
    #   5) условие выбора +/- direct
    # выход:
    #   1) степень позиционности модуляции r (если возврат 0 - то позиционность модуляции не определена )
    #####################################################################
            m_pos = GetPositionModulate(
                8, mu_n[x, :], Tqr[6, :], N_pos_qam - 3, 1, mqam)
            m_pos = m_pos + 2
            modulation = 2 ** (m_pos) + '-QAM'
            p_pos_qam[m_pos, 1] = p_pos_qam[m_pos, 1] + 1
            ###########################################################################
            # PSK-M
        else:
            if 2 == type_mod:
                modulation = 'M-PSK'
                p_good_psk = p_good_psk + 1
                # подготовительные вычисления "индусы"
    # переход в вещественную область значений сигнала
                buf_signal_real = ComplextoReal(buf_signal_orig)
                for i in np.arange(1, np.asarray(buf_signal_real).size+1).reshape(-1):
                    buf_signal_real[i] = buf_signal_real[i] + 2
                # преобразования вейвлетом Хаара
                va1, vd1 = pywt.dwt(buf_signal_real, 'haar')
                histogramm_va = hist_complex(va1, 10)
                mu_n_haar[x, :] = CalcMoment(va1, histogramm_va, 8)
                ###################################################################
    # функция выбора позиционности модуляции по заданному критерию и номеру
    # момента
    # вход:
    #   1) номер момента для выбора (точность) presition
    #   2) массив моментов moment[]
    #   3) массив критериев Tx[]
    #   4) размер массива критериев r_max
    #   5) условие выбора +/- direct
    # выход:
    #   1) степень позиционности модуляции r (если возврат 0 - то позиционность модуляции не определена )
    #####################################################################
                m_pos = GetPositionModulatePSK(
                    8, mu_n_haar[x, :], Tpr_h[6, :], N_pos_psk - 2, mpsk_h)
                modulation = 2 ** (m_pos) + '-PSK'
                p_pos_psk[m_pos, 1] = p_pos_psk[m_pos, 1] + 1
                ###########################################################################
    ###########################################################################
                # тип M-FSK
            else:
                if 3 == type_mod:
                    # подготовительные вычисления "индусы"
                    # переход в вещественную область значений сигнала
                    buf_signal_real = ComplextoReal(buf_signal_orig)
                    for i in np.arange(1, np.asarray(buf_signal_real).size+1).reshape(-1):
                        buf_signal_real[i] = buf_signal_real[i] + 2
                    # преобразования вейвлетом Хаара
                    va1, vd1 = pywt.dwt(buf_signal_real, 'haar')
                    histogramm_va = hist_complex(va1, 10)
                    mu_n_haar[x, :] = CalcMoment(va1, histogramm_va, 8)
                    p_good_fsk = p_good_fsk + 1
                    ###################################################################
    # функция выбора позиционности модуляции по заданному критерию и номеру
    # момента
    # вход:
    #   1) номер момента для выбора (точность) presition
    #   2) массив моментов moment[]
    #   3) массив критериев Tx[]
    #   4) размер массива критериев r_max
    #   5) условие выбора +/- direct
                    # выход:
    #   1) степень позиционности модуляции r (если возврат 0 - то позиционность модуляции не определена )
    #####################################################################
                    m_pos = GetPositionModulateFSK(
                        8, mu_n_haar[x, :], Tfr_h[6, :], N_pos_fsk, mpsk)
                    modulation = 2 ** (m_pos) + '-FSK'
                    p_pos_fsk[m_pos, 1] = p_pos_fsk[m_pos, 1] + 1
                    #  end;
                else:
                    if 4 == type_mod:
                        # тип GMSK
                        modulation = 'GMSK'
                        p_good_gmsk = p_good_gmsk + 1
        #####################################################################################

    # конец обработки блоков
    fda.close
    fdb.close
    # вероятность определения позиционности сигналов qam из выборки
    p_pos_qam = p_pos_qam / p_good_qam
    # кол-во решений по определению сигналов fsk из выборки
    p_good_fsk = p_good_fsk / Num_block
    # кол-во решений по определению сигналов psk из выборки
    p_good_psk = p_good_psk / Num_block
    # кол-во решений по определению сигналов gmsk из выборки
    p_good_gmsk = p_good_gmsk / Num_block
    # кол-во решений по определению сигналов qam из выборки
    p_good_qam = p_good_qam / Num_block
    # **************************************************************************

    # закрытие файла пакетов
    file.close
    # file2.close()
    # 0001 конец времянка для графика  достоверности от размера выборки

    # запись моментов в файл с соответствующим именем
    # **************************************************************************
    # функция записи моментов в файл бинарный
    # вход: 1) Name - имя файла
    #       2) moment - массив вектор
    #       3) size_mas - размер массива moment
    # выход: нет
    # **************************************************************************

    # WriteMomentFileBin('gmsk',mu_n(1,:),numel (mu_n(1,:)));

    # статистика пиков
    stat_Num_peak_va = stat_Num_peak_va / Num_block
    stat_Num_peak_vd = stat_Num_peak_vd / Num_block
    # вывод результатов:
    print('размер выборки=')
    print(N_sample)
    print('количество обработанных блоков=')
    print(Num_block)
    if (p_good_fsk > 0):
        print('вероятность решения по определению сигналов fsk из выборки')
        print(p_good_fsk)
        print('позиционность сигнала fsk')
        print(p_pos_fsk)

    if (p_good_psk > 0):
        print('вероятность решения по определению сигналов psk из выборки')
        print(p_good_psk)
        print('позиционность сигнала psk')
        print(p_pos_psk)

    if (p_good_gmsk > 0):
        print('вероятность решения по определению сигналов gmsk из выборки')
        print(p_good_gmsk)
        print('позиционность сигнала gmsk')
        print(2)

    if (p_good_qam > 0):
        print('вероятность решения по определению сигналов qam из выборки')
        print(p_good_qam)
        print('позиционность сигнала qam')
        print(p_pos_qam)


# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
