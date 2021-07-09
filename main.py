# coding=utf-8
# создано сотрудниками АО "НИИЧаспром"
# Данная программа предназначена для анализа надежности радиоэлектронных модулей и системы в целом
# !pip install brewer2mpl
import numpy
import numpy as np
import pandas as pd
# import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter
from mpl_toolkits import mplot3d

# % matplotlib
warnings.filterwarnings(action='once')

from matplotlib import rc  # для вывода русских букв

font = {'family': 'Verdana',  # для вывода русских букв
        'weight': 'normal'}
rc('font', **font)

''' Описание некоторых переменных и логики работы 
В Части 1 программы введены коэффициенты из справочника по надежности 2006 года
Сначала приводится массив коэффициентов для температуры эксплуатации 25, 30, 35, 40, 45, 50, 55, 60, 65, 70
Затем идут базовые значения. Эту часть предстоит расширить при появлении новых компонентов. 

Во Части 2 все коэффициенты умножаются и для каждого элемента получается 10 значения лямбда параметра для каждой 
температуры.

В Части 3 формируется состав модуля, всего в данной программе их два - МШВ без мажорирования и с мажорированием.

В Части 4 вычисляется ВБР для каждого из четырех случаев (на выходе для каждого случая получается двуменый массив
где по одной оси зависимость ВБР от времени, по другой от температуры ) 
- без мажорирования
- с мажорированием
- дублирование без мажорирования
- дублирование с мажорированием

Часть 5 построение различного вида графиков'''
###########################
# Часть 1
##########################
KV = [0.56, 0.91, 1.46, 2.31, 3.58, 5.49, 8.31, 12.43, 18.36, 26.82] # t =10 градусов, соотношение токов 0.5
V1 = 0.00103E-6     # 2  Вилка СНП59-64/94х11В-23-1-В	НЩ0.364.061ТУ
V2 = 0.0157E-6      # 2  Гнездо Г1,6 чер."5" В	ТУ6315.00207593842  (не нашел гамму в справочнике, взял типовую)
V3 = 0.00074E-6     # 1  Розетка РП15-9 ГВФ-В "5"	НКЦС.434410.509ТУ

#   устройства полупроводниковые,
#   для температуры [25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
# Коэфициент из српавочника, взяты для соотношения токов 0,6
KD = [0.1930, 0.2111, 0.2317, 0.2553, 0.2829, 0.3156, 0.3552, 0.40422, 0.4662, 0.5467]

D1 = 0.17E-6  # 2  Диод 2Д212Б /СО 	АЕЯР.432120.177ТУ
D2 = 0.078E-6  # 2  Диод 2Д222АС 	аА0.339.327ТУ
D3 = 0.032E-6  # 2  Диод 2Д522Б	ДР3.362.029-01ТУ/02	38
D4 = 0.01E-6  # 1  Стабилитрон 2С147В 	СМ3.362.839ТУ
T1 = 0.036E-6  # 5  Транзистор 2Т208А (3л)	ЮФ3.365.035ТУ

# индикаторы для температуры [25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
KI = [0.033, 0.048, 0.068, 0.096, 0.135, 0.187, 0.257, 0.349, 0.47, 0.628] # Коэфициент соотношения токов 0,3

I1 = 0.18E-6  # 1  индикатор ИПД148В-Л	аА0.339.189ТУ
I2 = 0.21E-6  # 1  Индикатор ИПВ72А1-4/5х7К (красный)	АЕЯР.432220.232ТУ

# конденсаторы
# для температуры [25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
KC = [0.033, 0.048, 0.068, 0.096, 0.135, 0.187, 0.257, 0.349, 0.47, 0.628]

C1 = 0.033E-6  # 8  Конд. К10-17а-М47-22 пФ±10%-В	ОЖ0.460.107ТУ
C2 = 0.033E-6  # 2  Конд. К10-17а-М47-330 пФ±10%-В	ОЖ0.460.107ТУ
C3 = 0.033E-6  # 1  Конд. К10-17а-МП0-50 В-47 пФ±10%-1-В	ОЖ0.460.107ТУ
C4 = 0.033E-6  # 30 Конд. К10-17а-Н90-0,033 мкФ-В	ОЖ0.460.107ТУ
C5 = 0.155E-6  # 2  Конд. К53-18-20В-22 мкФ±10%-В	ОЖ0.464.136ТУ
C6 = 0.155E-6  # 2  Конд. К53-18-20В-47 мкФ±10%-В	ОЖ0.464.136ТУ
C7 = 0.155E-6  # 3  Конд. К53-18-20В-100 мкФ±10%-В	ОЖ0.464.136ТУ

# микросхемы
# для температуры [25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
# KM1 = [0.66, 0.67, 0.74, 0.82, 0.91, 1.01, 0.257, 1.12, 1.24, 1.38]  # меньше 10 эл
KM1 = [1.0, 1.11, 1.23, 1.37, 1.52, 1.68, 1.87, 2.07, 2.3, 2.55]  # меньше 386 бит ЗУ, от 100 до 1000 эл

M1 = 0.0291E-6  # 1 (взял типовую) Микросборка 852ИН2П	АЕЯР.431230.419ТУ
M2 = 0.0485E-6  # 2 (типовая 386 бит ЗУ) Микросхема 1533АП6*5	бК0.347.364-55ТУ
M3 = 0.0485E-6  # 2  Микросхема 1533ИД7*5	бК0.347.364-08ТУ
M4 = 0.0485E-6  # 2  Микросхема 1533ИР24*5	бКЩ.347.364-38ТУ
M5 = 0.0485E-6  # 1  Микросхема 1533КП7*5	бК0.347.364-12ТУ
M6 = 0.0485E-6  # 3  Микросхема 1533ЛА3*5	бК0.347.364-01ТУ
M7 = 0.0485E-6  # 2  Микросхема 1533ЛЕ1*5	бК0.347.364-05ТУ
M8 = 0.0485E-6  # 1  Микросхема 1533ЛИ1*5	бК0.347.364-13ТУ
M9 = 0.0485E-6  # 1_0  Микросхема 1533ЛП3*5	бК0.347.364-15ТУ (элемент "или")
M10 = 0.0485E-6  # 1  Микросхема 1533ТМ9*5	бК0.347.364-24ТУ
M11 = 0.0485E-6  # 4  Микросхема 1533ТМ2*5	бК0.347.364-02ТУ
M12 = 0.0388E-6  # 1  (взял типовую 78 бит ЗУ)Микросхема 533ЛЕ4	бК0.347.141ТУ46/02
M13 = 0.0388E-6  # 1  Микросхема 533ЛЛ1	бК0.347.141ТУ7/02
M14 = 0.0388E-6  # 2  Микросхема 533ТЛ2	бК0.347.141ТУ16/02
M15 = 0.0872E-6  # 1  (типовая 4684 бит ЗУ) Микросхема 588ВГ7 бК0.347.367-12ТУ

KM2 = [1.7, 1.89, 2.09, 2.32, 2.58, 2.86, 3.17, 3.52, 3.91, 4.34]  # от 4000 до 16000 бит

M16 = 0.4362E-6  # 4_1  (типовая для макс. знач. ЗУ) Микросхема РIС17С44-33 I/P(40)

# резисторы

KR = [0.58, 0.59, 0.62, 0.64, 0.67, 0.7, 0.74, 0.79, 0.84, 0.91] # при нагрузке 0,5
R1 = 0.015E-6  # 1  Блок (резистор.) Б19К-2-10кОм±10%	ОЖ0.206.018ТУ
R2 = 0.063E-6  # 4_1  Резист. С2-33Н-0,125-100 Ом ±5% А-Д-В 	ОЖ0.467.093ТУ
R3 = 0.063E-6  # 1  Резист. С2-33Н-0,125-220 Ом ±5% А-Д-В 	ОЖ0.467.093ТУ
R4 = 0.063E-6  # 7  Резист. С2-33Н-0,125-470 Ом ±5% А-Д-В	ОЖ0.467.093ТУ
R5 = 0.063E-6  # 1  Резист. С2-33Н-0,125-510 Ом ±5% А-Д-В	ОЖ0.467.093ТУ
R6 = 0.06E-6  # 22_16  Резист. С2-33Н-0,125-1 кОм ±5% А-Д-В 	ОЖ0.467.093ТУ
R7 = 0.063E-6  # 2  Резист. С2-33Н-0,125-22 кОм ±5% А-Д-В 	ОЖ0.467.093ТУ
R8 = 0.063E-6  # 1  Резист. С2-33Н-0,125-51 кОм ±5% А-Д-В	ОЖ0.467.093ТУ
R9 = 0.063E-6  # 1  Резист. С2-33Н-0,5-390 Ом±5% А-Д-В 	ОЖ0.467.093ТУ
RZ1 = 0.013E-6  # 1  Резонатор РК386М-4АК-5000 кГц	ТУ6321-004-07614320-96
RZ2 = 0.013E-6  # 1  Резонатор РК386ММ-4АК-12000 К-В	ТУ6321-004-07614320-96
RZ3 = 0.013E-6  # 4_1  Резонатор РК386ММ-4АК-33000 кГц	ТУ6321-004-07614320-96

# Трансформатор
KTR = [1, 1.01, 1.04, 1.08, 1.13, 1.20, 1.29, 1.41, 1.57, 1.79]  # для класса Б - до 105 градусов
TR = 0.0019E-6  # 1  Трансформатор ТИЛ3В "5"	АГ0.472.105ТУ

VBR = []  # ВБР модуля без дублирования и мажорирования
VBR_D = []  # ВБР модуля с дублированием без мажорирования
D_MCHV = [] # временная переменная, содержит ВБР для определенной температуры
VBR_MAZH = []  # ВБР модуля с мажорированием без дублирования
VBR_D_MAZH = []  # ВБР модуля с дублированием и мажорированием
P_MCHV = [] # временная переменная, содержит ВБР для определенной температуры
MAZ = np.array([], float) # ВБР части мажоритароного узла, где элементы соеденены последовательно
P_MAZ =[] # ВБР голосование 2 из 3
T = []  # время наработки в часах
i = 0 # переменная для формаирования масиивов ВБР
MCHV = np.array([], float)
MCHV_MAMZ = np.array([], float)

###########################
# Часть 2
##########################

for t in range(1, 90000, 1000):     # время до 90000 ч
                                                                                                                    # шт с мажориров _шт без маж
    P_R1 = [np.exp(-R1*KR[0]*t), np.exp(-R1*KR[1]*t), np.exp(-R1*KR[2]*t), np.exp(-R1*KR[3]*t), np.exp(-R1*KR[4]*t),
            np.exp(-R1*KR[5]*t), np.exp(-R1*KR[6]*t), np.exp(-R1*KR[7]*t), np.exp(-R1*KR[8]*t), np.exp(-R1*KR[9]*t)]
    P_V1 = [np.exp(-V1*KV[0]*t), np.exp(-V1*KV[1]*t), np.exp(-V1*KV[2]*t), np.exp(-V1*KV[3]*t), np.exp(-V1*KV[4]*t),
            np.exp(-V1*KV[5]*t), np.exp(-V1*KV[6]*t), np.exp(-V1*KV[7]*t), np.exp(-V1*KV[8]*t), np.exp(-V1*KV[9]*t)]  # 2 шт
    P_V2 = [np.exp(-V2*KV[0]*t), np.exp(-V2*KV[1]*t), np.exp(-V2*KV[2]*t), np.exp(-V2*KV[3]*t), np.exp(-V2*KV[4]*t),
            np.exp(-V2*KV[5]*t), np.exp(-V2*KV[6]*t), np.exp(-V2*KV[7]*t), np.exp(-V2*KV[8]*t), np.exp(-V2*KV[9]*t)]  # 2 шт
    P_D1 = [np.exp(-D1*KD[0]*t), np.exp(-D1*KD[1]*t), np.exp(-D1*KD[2]*t), np.exp(-D1*KD[3]*t), np.exp(-D1*KD[4]*t),
            np.exp(-D1*KD[5]*t), np.exp(-D1*KD[6]*t), np.exp(-D1*KD[7]*t), np.exp(-D1*KD[8]*t), np.exp(-D1*KD[9]*t)]  # 2 шт
    P_D2 = [np.exp(-D2*KD[0]*t), np.exp(-D2*KD[1]*t), np.exp(-D2*KD[2]*t), np.exp(-D2*KD[3]*t), np.exp(-D2*KD[4]*t),
            np.exp(-D2*KD[5]*t), np.exp(-D2*KD[6]*t), np.exp(-D2*KD[7]*t), np.exp(-D2*KD[8]*t), np.exp(-D2*KD[9]*t)]  # 2 шт
    P_D3 = [np.exp(-D3*KD[0]*t), np.exp(-D3*KD[1]*t), np.exp(-D3*KD[2]*t), np.exp(-D3*KD[3]*t), np.exp(-D3*KD[4]*t),
            np.exp(-D3*KD[5]*t), np.exp(-D3*KD[6]*t), np.exp(-D3*KD[7]*t), np.exp(-D3*KD[8]*t), np.exp(-D3*KD[9]*t)]   # 2 шт
    P_I1 = [np.exp(-I1*KI[0]*t), np.exp(-I1*KI[1]*t), np.exp(-I1*KI[2]*t), np.exp(-I1*KI[3]*t), np.exp(-I1*KI[4]*t),
            np.exp(-I1*KI[5]*t), np.exp(-I1*KI[6]*t), np.exp(-I1*KI[7]*t). np.exp(-I1*KI[8]*t), np.exp(-I1*KI[9]*t)]
    P_I2 = [np.exp(-I2*KI[0]*t), np.exp(-I2*KI[1]*t), np.exp(-I2*KI[2]*t), np.exp(-I2*KI[3]*t), np.exp(-I2*KI[4]*t),
            np.exp(-I2*KI[5]*t), np.exp(-I2*KI[6]*t), np.exp(-I2*KI[7]*t). np.exp(-I2*KI[8]*t), np.exp(-I2*KI[9]*t)]
    P_C1 = [np.exp(-C1*KC[0]*t), np.exp(-C1*KC[1]*t), np.exp(-C1*KC[2]*t), np.exp(-C1*KC[3]*t), np.exp(-C1*KC[4]*t),
            np.exp(-C1*KC[5]*t), np.exp(-C1*KC[6]*t), np.exp(-C1*KC[7]*t), np.exp(-C1*KC[8]*t), np.exp(-C1*KC[9]*t)]  # 8 шт
    P_C2 = [np.exp(-C2*KC[0]*t), np.exp(-C2*KC[1]*t), np.exp(-C2*KC[2]*t), np.exp(-C2*KC[3]*t), np.exp(-C2*KC[4]*t),
            np.exp(-C2*KC[5]*t), np.exp(-C2*KC[6]*t), np.exp(-C2*KC[7]*t), np.exp(-C2*KC[8]*t), np.exp(-C2*KC[9]*t)]
    P_C3 = [np.exp(-C3*KC[0]*t), np.exp(-C3*KC[1]*t), np.exp(-C3*KC[2]*t), np.exp(-C3*KC[3]*t), np.exp(-C3*KC[4]*t),
            np.exp(-C3*KC[5]*t), np.exp(-C3*KC[6]*t), np.exp(-C3*KC[7]*t), np.exp(-C3*KC[8]*t), np.exp(-C3*KC[9]*t)]
    P_C4 = [np.exp(-C4*KC[0]*t), np.exp(-C4*KC[1]*t), np.exp(-C4*KC[2]*t), np.exp(-C4*KC[3]*t), np.exp(-C4*KC[4]*t),
            np.exp(-C4*KC[5]*t), np.exp(-C4*KC[6]*t), np.exp(-C4*KC[7]*t), np.exp(-C4*KC[8]*t), np.exp(-C4*KC[9]*t)]  # 30 шт
    P_C5 = [np.exp(-C5*KC[0]*t), np.exp(-C5*KC[1]*t), np.exp(-C5*KC[2]*t), np.exp(-C5*KC[3]*t), np.exp(-C5*KC[4]*t),
            np.exp(-C5*KC[5]*t), np.exp(-C5*KC[6]*t), np.exp(-C5*KC[7]*t), np.exp(-C5*KC[8]*t), np.exp(-C5*KC[9]*t)]  # 2 шт
    P_C6 = [np.exp(-C6*KC[0]*t), np.exp(-C6*KC[1]*t), np.exp(-C6*KC[2]*t), np.exp(-C6*KC[3]*t), np.exp(-C6*KC[4]*t),
            np.exp(-C6*KC[5]*t), np.exp(-C6*KC[6]*t), np.exp(-C6*KC[7]*t), np.exp(-C6*KC[8]*t), np.exp(-C6*KC[9]*t)]   # 2 шт
    P_C7 = [np.exp(-C7*KC[0]*t), np.exp(-C7*KC[1]*t), np.exp(-C7*KC[2]*t), np.exp(-C7*KC[3]*t), np.exp(-C7*KC[4]*t),
            np.exp(-C7*KC[5]*t), np.exp(-C7*KC[6]*t), np.exp(-C7*KC[7]*t), np.exp(-C7*KC[8]*t), np.exp(-C7*KC[9]*t)]   # 3 шт
    P_M1 = [np.exp(-M1*KM1[0]*t), np.exp(-M1*KM1[1]*t), np.exp(-M1*KM1[2]*t), np.exp(-M1*KM1[3]*t), np.exp(-M1*KM1[4]*t),
            np.exp(-M1*KM1[5]*t), np.exp(-M1*KM1[6]*t), np.exp(-M1*KM1[7]*t), np.exp(-M1*KM1[8]*t), np.exp(-M1*KM1[9]*t)]
    P_M2 = [np.exp(-M2*KM1[0]*t), np.exp(-M2*KM1[1]*t), np.exp(-M2*KM1[2]*t), np.exp(-M2*KM1[3]*t), np.exp(-M2*KM1[4]*t),
            np.exp(-M2*KM1[5]*t), np.exp(-M2*KM1[6]*t), np.exp(-M2*KM1[7]*t), np.exp(-M2*KM1[8]*t), np.exp(-M2*KM1[9]*t)]  # 2 шт
    P_M3 = [np.exp(-M3*KM1[0]*t), np.exp(-M3*KM1[1]*t), np.exp(-M3*KM1[2]*t), np.exp(-M3*KM1[3]*t), np.exp(-M3*KM1[4]*t),
            np.exp(-M3*KM1[5]*t), np.exp(-M3*KM1[6]*t), np.exp(-M3*KM1[7]*t), np.exp(-M3*KM1[8]*t), np.exp(-M3*KM1[9]*t)]  # 2 шт
    P_M4 = [np.exp(-M4*KM1[0]*t), np.exp(-M4*KM1[1]*t), np.exp(-M4*KM1[2]*t), np.exp(-M4*KM1[3]*t), np.exp(-M4*KM1[4]*t),
            np.exp(-M4*KM1[5]*t), np.exp(-M4*KM1[6]*t), np.exp(-M4*KM1[7]*t), np.exp(-M4*KM1[8]*t), np.exp(-M4*KM1[9]*t)]  # 2 шт
    P_M5 = [np.exp(-M5*KM1[0]*t), np.exp(-M5*KM1[1]*t), np.exp(-M5*KM1[2]*t), np.exp(-M5*KM1[3]*t), np.exp(-M5*KM1[4]*t),
            np.exp(-M5*KM1[5]*t), np.exp(-M5*KM1[6]*t), np.exp(-M5*KM1[7]*t), np.exp(-M5*KM1[8]*t), np.exp(-M5*KM1[9]*t)]
    P_M6 = [np.exp(-M6*KM1[0]*t), np.exp(-M6*KM1[1]*t), np.exp(-M6*KM1[2]*t), np.exp(-M6*KM1[3]*t), np.exp(-M6*KM1[4]*t),
            np.exp(-M6*KM1[5]*t), np.exp(-M6*KM1[6]*t), np.exp(-M6*KM1[7]*t), np.exp(-M6*KM1[8]*t), np.exp(-M6*KM1[9]*t)] # 3 шт
    P_M7 = [np.exp(-M7*KM1[0]*t), np.exp(-M7*KM1[1]*t), np.exp(-M7*KM1[2]*t), np.exp(-M7*KM1[3]*t), np.exp(-M7*KM1[4]*t),
            np.exp(-M7*KM1[5]*t), np.exp(-M7*KM1[6]*t), np.exp(-M7*KM1[7]*t), np.exp(-M7*KM1[8]*t), np.exp(-M7*KM1[9]*t)]  # 2 шт
    P_M8 = [np.exp(-M8*KM1[0]*t), np.exp(-M8*KM1[1]*t), np.exp(-M8*KM1[2]*t), np.exp(-M8*KM1[3]*t), np.exp(-M8*KM1[4]*t),
            np.exp(-M8*KM1[5]*t), np.exp(-M8*KM1[6]*t), np.exp(-M8*KM1[7]*t), np.exp(-M8*KM1[8]*t), np.exp(-M8*KM1[9]*t)]
    P_M9 = [np.exp(-M9*KM1[0]*t), np.exp(-M9*KM1[1]*t), np.exp(-M9*KM1[2]*t), np.exp(-M9*KM1[3]*t), np.exp(-M9*KM1[4]*t),
            np.exp(-M9*KM1[5]*t), np.exp(-M9*KM1[6]*t), np.exp(-M9*KM1[7]*t), np.exp(-M9*KM1[8]*t), np.exp(-M9*KM1[9]*t)]  # (это элемент "или" в мажоритарном узел)
    P_M10 = [np.exp(-M10*KM1[0]*t), np.exp(-M10*KM1[1]*t), np.exp(-M10*KM1[2]*t), np.exp(-M10*KM1[3]*t), np.exp(-M10*KM1[4]*t),
             np.exp(-M10*KM1[5]*t), np.exp(-M10*KM1[6]*t), np.exp(-M10*KM1[7]*t), np.exp(-M10*KM1[8]*t), np.exp(-M10*KM1[9]*t)]  # 4 шт
    P_M11 = [np.exp(-M11*KM1[0]*t), np.exp(-M11*KM1[1]*t), np.exp(-M11*KM1[2]*t), np.exp(-M11*KM1[3]*t), np.exp(-M11*KM1[4]*t),
             np.exp(-M11*KM1[5]*t), np.exp(-M11*KM1[6]*t), np.exp(-M11*KM1[7]*t), np.exp(-M11*KM1[8]*t), np.exp(-M11*KM1[9]*t)]
    P_M12 = [np.exp(-M12*KM1[0]*t), np.exp(-M12*KM1[1]*t), np.exp(-M12*KM1[2]*t), np.exp(-M12*KM1[3]*t), np.exp(-M12*KM1[4]*t),
             np.exp(-M12*KM1[5]*t), np.exp(-M12*KM1[6]*t), np.exp(-M12*KM1[7]*t), np.exp(-M12*KM1[8]*t), np.exp(-M12*KM1[9]*t)]
    P_M13 = [np.exp(-M13*KM1[0]*t), np.exp(-M13*KM1[1]*t), np.exp(-M13*KM1[2]*t), np.exp(-M13*KM1[3]*t), np.exp(-M13*KM1[4]*t),
             np.exp(-M13*KM1[5]*t), np.exp(-M13*KM1[6]*t), np.exp(-M13*KM1[7]*t), np.exp(-M13*KM1[8]*t), np.exp(-M13*KM1[9]*t)]
    P_M14 = [np.exp(-M14*KM1[0]*t), np.exp(-M14*KM1[1]*t), np.exp(-M14*KM1[2]*t), np.exp(-M14*KM1[3]*t), np.exp(-M14*KM1[4]*t),
             np.exp(-M14*KM1[5]*t), np.exp(-M14*KM1[6]*t), np.exp(-M14*KM1[7]*t), np.exp(-M14*KM1[8]*t), np.exp(-M14*KM1[9]*t)]  # 2
    P_M15 = [np.exp(-M15*KM1[0]*t), np.exp(-M15*KM1[1]*t), np.exp(-M15*KM1[2]*t), np.exp(-M15*KM1[3]*t), np.exp(-M15*KM1[4]*t),
             np.exp(-M15*KM1[5]*t), np.exp(-M15*KM1[6]*t), np.exp(-M15*KM1[7]*t), np.exp(-M15*KM1[8]*t), np.exp(-M15*KM1[9]*t)]
    P_M16 = [np.exp(-M16*KM2[0]*t), np.exp(-M16*KM2[1]*t), np.exp(-M16*KM2[2]*t), np.exp(-M16*KM2[3]*t), np.exp(-M16*KM2[4]*t),
             np.exp(-M16*KM2[5]*t), np.exp(-M16*KM2[6]*t), np.exp(-M16*KM2[7]*t), np.exp(-M16*KM2[8]*t), np.exp(-M16*KM2[9]*t)]  # 4_1 шт
    P_R2 = [np.exp(-R2*KR[0]*t), np.exp(-R2*KR[1]*t), np.exp(-R2*KR[2]*t), np.exp(-R2*KR[3]*t), np.exp(-R2*KR[4]*t),
            np.exp(-R2*KR[5]*t), np.exp(-R2*KR[6]*t), np.exp(-R2*KR[7]*t), np.exp(-R2*KR[8]*t), np.exp(-R2*KR[9]*t)]  # 4_1 шт
    P_R3 = [np.exp(-R3*KR[0]*t), np.exp(-R3*KR[1]*t), np.exp(-R3*KR[2]*t), np.exp(-R3*KR[3]*t), np.exp(-R3*KR[4]*t),
            np.exp(-R3*KR[5]*t), np.exp(-R3*KR[6]*t), np.exp(-R3*KR[7]*t), np.exp(-R3*KR[8]*t), np.exp(-R3*KR[9]*t)]
    P_R4 = [np.exp(-R4*KR[0]*t), np.exp(-R4*KR[1]*t), np.exp(-R4*KR[2]*t), np.exp(-R4*KR[3]*t), np.exp(-R4*KR[4]*t),
            np.exp(-R4*KR[5]*t), np.exp(-R4*KR[6]*t), np.exp(-R4*KR[7]*t), np.exp(-R4*KR[8]*t), np.exp(-R4*KR[9]*t)]  # 7 шт
    P_R5 = [np.exp(-R5*KR[0]*t), np.exp(-R5*KR[1]*t), np.exp(-R5*KR[2]*t), np.exp(-R5*KR[3]*t), np.exp(-R5*KR[4]*t),
            np.exp(-R5*KR[5]*t), np.exp(-R5*KR[6]*t), np.exp(-R5*KR[7]*t), np.exp(-R5*KR[8]*t), np.exp(-R5*KR[9]*t)]
    P_R6 = [np.exp(-R6*KR[0]*t), np.exp(-R6*KR[1]*t), np.exp(-R6*KR[2]*t), np.exp(-R6*KR[3]*t), np.exp(-R6*KR[4]*t),
            np.exp(-R6*KR[5]*t), np.exp(-R6*KR[6]*t), np.exp(-R6*KR[7]*t), np.exp(-R6*KR[8]*t), np.exp(-R6*KR[9]*t)]  # 22_16 шт
    P_R7 = [np.exp(-R7*KR[0]*t), np.exp(-R7*KR[1]*t), np.exp(-R7*KR[2]*t), np.exp(-R7*KR[3]*t), np.exp(-R7*KR[4]*t),
            np.exp(-R7*KR[5]*t), np.exp(-R7*KR[6]*t), np.exp(-R7*KR[7]*t), np.exp(-R7*KR[8]*t), np.exp(-R7*KR[9]*t)]  # 2 шт
    P_R8 = [np.exp(-R8*KR[0]*t), np.exp(-R8*KR[1]*t), np.exp(-R8*KR[2]*t), np.exp(-R8*KR[3]*t), np.exp(-R8*KR[4]*t),
            np.exp(-R8*KR[5]*t), np.exp(-R8*KR[6]*t), np.exp(-R8*KR[7]*t), np.exp(-R8*KR[8]*t), np.exp(-R8*KR[9]*t)]
    P_R9 = [np.exp(-R9*KR[0]*t), np.exp(-R9*KR[1]*t), np.exp(-R9*KR[2]*t), np.exp(-R9*KR[3]*t), np.exp(-R9*KR[4]*t),
            np.exp(-R9*KR[5]*t), np.exp(-R9*KR[6]*t), np.exp(-R9*KR[7]*t), np.exp(-R9*KR[8]*t), np.exp(-R9*KR[9]*t)]
    P_RZ1 = [np.exp(-RZ1*KR[0]*t), np.exp(-RZ1*KR[1]*t), np.exp(-RZ1*KR[2]*t), np.exp(-RZ1*KR[3]*t), np.exp(-RZ1*KR[4]*t),
            np.exp(-RZ1*KR[5]*t), np.exp(-RZ1*KR[6]*t), np.exp(-RZ1*KR[7]*t), np.exp(-RZ1*KR[8]*t), np.exp(-RZ1*KR[9]*t)]
    P_RZ2 = [np.exp(-RZ2*KR[0]*t), np.exp(-RZ2*KR[1]*t), np.exp(-RZ2*KR[2]*t), np.exp(-RZ2*KR[3]*t), np.exp(-RZ2*KR[4]*t),
            np.exp(-RZ2*KR[5]*t), np.exp(-RZ2*KR[6]*t), np.exp(-RZ2*KR[7]*t), np.exp(-RZ2*KR[8]*t), np.exp(-RZ2*KR[9]*t)]
    P_RZ3 = [np.exp(-RZ3*KR[0]*t), np.exp(-RZ3*KR[1]*t), np.exp(-RZ3*KR[2]*t), np.exp(-RZ3*KR[3]*t), np.exp(-RZ3*KR[4]*t),
            np.exp(-RZ2*KR[5]*t), np.exp(-RZ2*KR[6]*t), np.exp(-RZ2*KR[7]*t), np.exp(-RZ2*KR[8]*t), np.exp(-RZ3*KR[9]*t)]  # 4_1 шт
    P_V3 = [np.exp(-V3*KV[0]*t), np.exp(-V3*KV[1]*t), np.exp(-V3*KV[2]*t), np.exp(-V3*KV[3]*t), np.exp(-V3*KV[4]*t),
            np.exp(-V3*KV[5]*t), np.exp(-V3*KV[6]*t), np.exp(-V3*KV[7]*t), np.exp(-V3*KV[8]*t), np.exp(-V3*KV[9]*t)]
    P_D4 = [np.exp(-D4*KD[0]*t), np.exp(-D4*KD[1]*t), np.exp(-D4*KD[2]*t), np.exp(-D4*KD[3]*t), np.exp(-D4*KD[4]*t),
            np.exp(-D4*KD[5]*t), np.exp(-D4*KD[6]*t), np.exp(-D4*KD[7]*t), np.exp(-D4*KD[8]*t), np.exp(-D4*KD[9]*t)]
    P_T1 = [np.exp(-T1*KD[0]*t), np.exp(-T1*KD[1]*t), np.exp(-T1*KD[2]*t), np.exp(-T1*KD[3]*t), np.exp(-T1*KD[4]*t),
            np.exp(-T1*KD[5]*t), np.exp(-T1*KD[6]*t), np.exp(-T1*KD[7]*t), np.exp(-T1*KD[8]*t), np.exp(-T1*KD[9]*t)]  # 5 шт
    P_TR = [np.exp(-TR*KTR[0]*t), np.exp(-TR*KTR[1]*t), np.exp(-TR*KTR[2]*t), np.exp(-TR*KTR[3]*t), np.exp(-TR*KTR[4]*t),
            np.exp(-TR*KTR[5]*t), np.exp(-TR*KTR[6]*t), np.exp(-TR*KTR[7]*t), np.exp(-TR*KTR[8]*t), np.exp(-TR*KTR[9]*t)]
    ###########################
    # Часть 3
    ##########################
    for x in range(len(P_TR)):
        MCHV[i] = P_R1,# Состав МШВ без мажорирования (матрица MC_HV для проверки состава)
               P_V1, P_V1,
               P_V2, P_V2,
               P_D1, P_D1,
               P_D2, P_D2,
               P_D3, P_D3,
               P_I1,
               P_I2,
               P_C1, P_C1, P_C1, P_C1, P_C1, P_C1, P_C1, P_C1,
               P_C2,
               P_C3,
               P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4,
               P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4,
               P_C5, P_C5,
               P_C6, P_C6,
               P_C7, P_C7, P_C7,
               P_M1,
               P_M2, P_M2,
               P_M3, P_M3,
               P_M4, P_M4,
               P_M5,
               P_M6, P_M6, P_M6,
               P_M7,
               P_M8,
               P_M10, P_M10, P_M10, P_M10,
               P_M11,
               P_M12,
               P_M13,
               P_M14, P_M14,
               P_M15,
               P_M16,
               P_R2,
               P_R3,
               P_R4, P_R4, P_R4, P_R4, P_R4, P_R4, P_R4,
               P_R5,
               P_R6, P_R6, P_R6, P_R6, P_R6, P_R6, P_R6, P_R6, P_R6, P_R6, P_R6,
               P_R6, P_R6, P_R6, P_R6,
               P_R7, P_R7,
               P_R8,
               P_R9,
               P_RZ1,
               P_RZ2,
               P_RZ3,
               P_V3,
               P_D4,
               P_T1, P_T1, P_T1, P_T1, P_T1,
               P_TR})
    for x in range(len(MCHV)):
            MAZ[x] = P_M16[x] * P_R2[x] * P_R6[x] * P_R6[x] * P_RZ3[x]  # ВБР элементов мажоритарного узла* соединнных последовательно
            P_MAZ[x] = P_M9[x] * (3 * (MAZ[x] ** 2) - 2 * (MAZ[x] ** 3)) # голосование 2 из 3
    MCHV_MAMZ[i] = np.array({P_MAZ,
                             P_R1,
                             P_V1, P_V1,
                             P_V2, P_V2,
                             P_D1, P_D1,
                             P_D2, P_D2,
                             P_D3, P_D3,
                             P_I1,
                             P_I2,
                             P_C1, P_C1, P_C1, P_C1, P_C1, P_C1, P_C1, P_C1,
                             P_C2,
                             P_C3,
                             P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4,
                             P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4, P_C4,
                             P_C5, P_C5,
                             P_C6, P_C6,
                             P_C7, P_C7, P_C7,
                             P_M1,
                             P_M2, P_M2,
                             P_M3, P_M3,
                             P_M4, P_M4,
                             P_M5,
                             P_M6, P_M6, P_M6,
                             P_M7,
                             P_M8,
                             P_M10, P_M10, P_M10, P_M10,
                             P_M11,
                             P_M12,
                             P_M13,
                             P_M14, P_M14,
                             P_M15,
                             P_R3,
                             P_R4, P_R4, P_R4, P_R4, P_R4, P_R4, P_R4,
                             P_R5,
                             P_R6, P_R6, P_R6, P_R6, P_R6, P_R6, P_R6, P_R6, P_R6, P_R6, P_R6,
                             P_R6, P_R6, P_R6, P_R6, P_R6,
                             P_R7, P_R7,
                             P_R8,
                             P_R9,
                             P_RZ1,
                             P_RZ2,
                             P_RZ3,
                             P_V3,
                             P_D4,
                             P_T1, P_T1, P_T1, P_T1, P_T1,
                             P_TR})
    ###########################
    # Часть 3
    ##########################
    VBR[i]=1
    for x in range(len(MCHV)):# Дублирование
        VBR[i]*=MCHV[x]
         D_MCHV[i] = P_MCHV * MCHV[x]
    VBR_D.append(D_MCHV)
    VBR.append(MCHV)
    # Состав МШВ с мажорированием
    D_MCHV_MAZH = 1 - (1 - MCHV_MAMZ) ** 2
    VBR_D_MAZH.append(D_MCHV_MAZH)
    VBR_MAZH.append(MCHV_MAMZ)
    T.append(t)
i+=1

'''Часть 5'''
fig = plt.figure(figsize=(9, 8))
ax = fig.add_subplot(1, 1, 1, aspect=T[-1] + 100000)


def minor_tick(x, pos):
    if not x % 1.0:
        return ""
    return "%.2f" % x


ax.xaxis.set_major_locator(MultipleLocator(10000.000))
ax.xaxis.set_minor_locator(AutoMinorLocator(9))
ax.yaxis.set_major_locator(MultipleLocator(0.05))
# ax.yaxis.set_minor_locator(AutoMinorLocator(2))
# ax.xaxis.set_minor_formatter(FuncFormatter(minor_tick))

ax.set_xlim(0, T[-1] + 1000)
ax.set_ylim(0.55, 1.01)

# ax.tick_params(which='major', width=1.0)
# ax.tick_params(which='major', length=1.0)
# ax.tick_params(which='minor', width=1.0, labelsize=1.0)
# ax.tick_params(which='minor', length=5, labelsize=10, labelcolor='0.25')

ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)

ax.plot(T, VBR[5], lw=2,
        label=u"без мажорирования")  # ax.plot(T, vbr, c=(0.25, 0.25, 1.00), lw=2, label="Blue signal", zorder=10)
ax.plot(T, VBR_MAZH[5], lw=2,
        label=u"мажорирование без дублирования")  # ax.plot(T, vbr1, c=(1.00, 0.25, 0.25), lw=2, label="Red signal")
ax.plot(T, VBR_D[5], lw=2, label=u"дублирование без мажорирования")
ax.plot(T, VBR_D_MAZH[5], lw=2, label=u"дублирование и мажорирование")

# ax.plot(X, Y3, linewidth=0,
#        marker='o', markerfacecolor='w', markeredgecolor='k')

# ax.set_title(u"Вероятность безотказной работы", fontsize=20, verticalalignment='bottom')
ax.set_xlabel(u"Время работы (ч)")
ax.set_ylabel(u"Вероятность")

ax.legend()


def circle(x, y, radius=0.15):
    from matplotlib.patches import Circle
    from matplotlib.patheffects import withStroke
    circle = Circle((x, y), radius, clip_on=False, zorder=10, linewidth=1,
                    edgecolor='black', facecolor=(0, 0, 0, .0125),
                    path_effects=[withStroke(linewidth=5, foreground='w')])
    ax.add_artist(circle)


def text(x, y, text):
    ax.text(x, y, text, backgroundcolor="white",
            ha='center', va='top', weight='bold', color='blue')


'''
тут всякие кружочки
# Minor tick
# circle(0.50, -0.10)
# text(0.50, -0.32, "Minor tick label")

# Major tick
circle(-0.03, 4.00)
text(0.03, 3.80, "Major tick")

# Minor tick
circle(0.00, 3.50)
text(0.00, 3.30, "Minor tick")

# Major tick label
circle(-0.15, 3.00)
text(-0.15, 2.80, "Major tick label")

# X Label
circle(1.80, -0.27)
text(1.80, -0.45, "X axis label")

# Y Label
circle(-0.27, 1.80)
text(-0.27, 1.6, "Y axis label")

# Title
circle(1.60, 4.13)
text(1.60, 3.93, "Title")

# Blue plot
circle(1.75, 2.80)
text(1.75, 2.60, "Line\n(line plot)")

# Red plot
circle(1.20, 0.60)
text(1.20, 0.40, "Line\n(line plot)")

# Scatter plot
circle(3.20, 1.75)
text(3.20, 1.55, "Markers\n(scatter plot)")

# Grid
circle(3.00, 3.00)
text(3.00, 2.80, "Grid")

# Legend
circle(3.70, 3.80)
text(3.70, 3.60, "Legend")

# Axes
circle(0.5, 0.5)
text(0.5, 0.3, "Axes")

# Figure
circle(-0.3, 0.65)
text(-0.3, 0.45, "Figure")

'''

# стрелки с подписью про надежность
color = 'blue'
rel = str(round(MCHV[5], 3))
rel_mazh = str(round(MCHV_MAMZ[5], 3))
rel_d = str(round(D_MCHV[5], 3))
rel_mazh_d = str(round(D_MCHV_MAZH[5], 3))

ax.annotate(rel, xy=(T[-1] - 100, MCHV[5]), xycoords='data',
            xytext=(T[-1] - 15000, 0.56), textcoords='data',
            weight='bold', color=color,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3",
                            color=color))

ax.annotate(rel_mazh, xy=(T[-1] - 100, MCHV_MAMZ), xycoords='data',
            xytext=(T[-1] - 15000, 0.65), textcoords='data',
            weight='bold', color=color,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3",
                            color=color))

ax.annotate(rel_d, xy=(T[-1] - 100, D_MCHV), xycoords='data',
            xytext=(T[-1] - 10000, 0.77), textcoords='data',
            weight='bold', color=color,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3",
                            color=color))
ax.annotate(rel_mazh_d, xy=(T[-1] - 100, D_MCHV_MAZH), xycoords='data',
            xytext=(T[-1] - 10000, 0.87), textcoords='data',
            weight='bold', color=color,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3",
                            color=color))

# ax.annotate(rel_mazh, xy=(T[-1]-100, MCHV_MAMZ*2), xycoords='data',
#            xytext=(T[-1]-10000, 0.7), textcoords='data',
#            weight='bold', color=color,
#            arrowprops=dict(arrowstyle='->',
#                            connectionstyle="arc3",
#                            color=color))

ax.text(4.0, -0.4, "(JSC) Scientific Research Institute For Watch Industry",
        fontsize=10, ha="right", color='.5')

plt.show()

# отображение отказа
