# coding=utf-8
# создано сотрудниками АО "НИИЧаспром"
# Данная программа предназначена для анализа надежности радиоэлектронных модулей, выполн
# !pip install brewer2mpl
#

import math

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from math import e

# % matplotlib
# from typing import List, Union

warnings.filterwarnings(action='once')

from matplotlib import rc  # для вывода русских букв

font = {'family': 'Verdana',  # для вывода русских букв
        'weight': 'normal'}
rc('font', **font)

''' Описание некоторых переменных и логики работы 
В Части 1 программы введены коэффициенты из справочника по надежности 2006 года
Сначала приводится массив коэффициентов для температуры эксплуатации 25, 30, 35, 40, 45, 50, 55, 60, 65, 70
Затем идут базовые значения.
Конечнаый блок - блок вычисления потоков отказов для каждго элемента. Эти данные нужны для вычисления потока отказов 
всего модуля при расчете запасов ЗИП

Эту часть предстоит расширить при появлении новых компонентов. 

Во Части 2 все коэффициенты умножаются и для каждого элемента получается 10 значений ВБР (для 10 коэфициентов) 
для каждой температуры.

В Части 3 формируются составы модуле, всего в данной программе их два - МШВ без мажорирования и с мажорированием.

В Части 4 вычисляется ВБР для каждого из четырех случаев (на выходе для каждого случая получается двуменый массив
где по одной оси зависимость ВБР от времени, по другой от температуры ) 
- без мажорирования
- с мажорированием
- дублирование без мажорирования
- дублирование с мажорированием

Часть 5 Вычисление необходимого ЗИП
Вычиления делаются в соотвесвти с ГОСТ РВ 27.3.03-2005 по формуле 9.3 для разного времени пополнения ЗИП 

Часть 6 построение различного вида графиков'''
###########################
# Часть 1
###########################

Z = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70]  # Температура для которой расчитывается коэффициент
time = 131  # вермя, тыс. часов
VBR = np.ones(len(Z))  # ВБР модуля без дублирования и мажорирования
VBR_D = np.ones(len(Z))  # ВБР модуля с дублированием без мажорирования
VBR_MAZH = np.ones(len(Z))  # ВБР модуля с мажорированием без дублирования
VBR_D_MAZH = np.ones(len(Z))  # ВБР модуля с дублированием и мажорированием
P_MCHV = np.zeros(len(Z))  # временная переменная, содержит ВБР для определенной температуры
MAZ = np.zeros(len(Z))  # ВБР части мажоритароного узла, где элементы соеденены последовательно
P_MAZ = np.zeros(len(Z))  # ВБР голосование 2 из 3
T = []  # время наработки в часах
MCHV = np.zeros(len(Z))  # для одного значения времени (ВБР(t=25), ... , ВБР(t=70)) МШВ без мажорировани
MCHV_MAZH = np.zeros(len(Z))  # для одного значения времени (ВБР(t=25), ... , ВБР(t=70)) МШВ с мажорированием
D_MCHV = np.zeros(len(Z))  # для одного значения времени (ВБР(t=25), ... , ВБР(t=70)) МШВ дублирование без мажорировани
D_MCHV_MAZH = np.zeros(
len(Z))  # для одного значения времени (ВБР(t=25), ... , ВБР(t=70)) МШВ дублирование с мажорированием
GM_MAZ = np.zeros(len(Z))  # временная переменная для вычисления интенсивности отказов
G_MAZ = np.zeros(len(Z))  # интенсивность отказов мажоритарного узла
G_MAZH = np.zeros(len(Z))  # интенсивность отказов всего МШВ
a = np.zeros(len(Z))  # среднее число поступающих в комплект ЗИП заявок на запасные части
R = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # временная переменная для вычисления количества модулей в ЗИП
zip = np.zeros(len(Z))
# D_MCHV_ZIP_TEM = np.ones(len(Z))
COUNT_ZIP = np.zeros(len(Z))
DZIP = np.zeros(len(Z))
k = 1 # неснижаемый запас
# D_MCHV_ZIP = [np.zeros(Z)]
#######################
# данные из справочника
#######################

KV = [0.56, 0.91, 1.46, 2.31, 3.58, 5.49, 8.31, 12.43, 18.36, 26.82]  # t =10 градусов, соотношение токов 0.5
V1 = 0.00103E-6  # 2  Вилка СНП59-64/94х11В-23-1-В	НЩ0.364.061ТУ
V2 = 0.0157E-6  # 2  Гнездо Г1,6 чер."5" В	ТУ6315.00207593842  (не нашел гамму в справочнике, взял типовую)
V3 = 0.00074E-6  # 1  Розетка РП15-9 ГВФ-В "5"	НКЦС.434410.509ТУ

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
KI = [0.033, 0.048, 0.068, 0.096, 0.135, 0.187, 0.257, 0.349, 0.47, 0.628]  # Коэфициент соотношения токов 0,3

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
# KM = [0.66, 0.67, 0.74, 0.82, 0.91, 1.01, 0.257, 1.12, 1.24, 1.38]  # меньше 10 эл
KM = [1.0, 1.11, 1.23, 1.37, 1.52, 1.68, 1.87, 2.07, 2.3, 2.55]  # меньше 386 бит ЗУ, от 100 до 1000 эл

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

KR = [0.58, 0.59, 0.62, 0.64, 0.67, 0.7, 0.74, 0.79, 0.84, 0.91]  # при нагрузке 0,5
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

###########################
# Часть 2
##########################
# потоки отказов для элементов в зависимости от температуры.
# Для этого умножаем общий поток отказов на температурный коэфициент

G_R1 = [R1 * KR[0], R1 * KR[1], R1 * KR[2], R1 * KR[3], R1 * KR[4], R1 * KR[5], R1 * KR[6], R1 * KR[7], R1 * KR[8],
        R1 * KR[9]]
G_V1 = [V1 * KV[0], V1 * KV[1], V1 * KV[2], V1 * KV[3], V1 * KV[4], V1 * KV[5], V1 * KV[6], V1 * KV[7], V1 * KV[8],
        V1 * KV[9]]
G_V2 = [V2 * KV[0], V2 * KV[1], V2 * KV[2], V2 * KV[3], V2 * KV[4], V2 * KV[5], V2 * KV[6], V2 * KV[7], V2 * KV[8],
        V2 * KV[9]]
G_V3 = [V3 * KV[0], V3 * KV[1], V3 * KV[2], V3 * KV[3], V3 * KV[4], V3 * KV[5], V3 * KV[6], V3 * KV[7], V3 * KV[8],
        V3 * KV[9]]
G_D1 = [D1 * KD[0], D1 * KD[1], D1 * KD[2], D1 * KD[3], D1 * KD[4], D1 * KD[5], D1 * KD[6], D1 * KD[7], D1 * KD[8],
        D1 * KD[9]]
G_D2 = [D2 * KD[0], D2 * KD[1], D2 * KD[2], D2 * KD[3], D2 * KD[4], D2 * KD[5], D2 * KD[6], D2 * KD[7], D2 * KD[8],
        D2 * KD[9]]
G_D3 = [D3 * KD[0], D3 * KD[1], D3 * KD[2], D3 * KD[3], D3 * KD[4], D3 * KD[5], D3 * KD[6], D3 * KD[7], D3 * KD[8],
        D3 * KD[9]]
G_I1 = [I1 * KI[0], I1 * KI[1], I1 * KI[2], I1 * KI[3], I1 * KI[4], I1 * KI[5], I1 * KI[6], I1 * KI[7], I1 * KI[8],
        I1 * KI[9]]
G_I2 = [I2 * KI[0], I2 * KI[1], I2 * KI[2], I2 * KI[3], I2 * KI[4], I2 * KI[5], I2 * KI[6], I2 * KI[7], I2 * KI[8],
        I2 * KI[9]]
G_C1 = [C1 * KC[0], C1 * KC[1], C1 * KC[2], C1 * KC[3], C1 * KC[4], C1 * KC[5], C1 * KC[6], C1 * KC[7], C1 * KC[8],
        C1 * KC[9]]
G_C2 = [C2 * KC[0], C2 * KC[1], C2 * KC[2], C2 * KC[3], C2 * KC[4], C2 * KC[5], C2 * KC[6], C2 * KC[7], C2 * KC[8],
        C2 * KC[9]]
G_C3 = [C3 * KC[0], C3 * KC[1], C3 * KC[2], C3 * KC[3], C3 * KC[4], C3 * KC[5], C3 * KC[6], C3 * KC[7], C3 * KC[8],
        C3 * KC[9]]
G_C4 = [C4 * KC[0], C4 * KC[1], C4 * KC[2], C4 * KC[3], C4 * KC[4], C4 * KC[5], C4 * KC[6], C4 * KC[7], C4 * KC[8],
        C4 * KC[9]]
G_C5 = [C5 * KC[0], C5 * KC[1], C5 * KC[2], C5 * KC[3], C5 * KC[4], C5 * KC[5], C5 * KC[6], C5 * KC[7], C5 * KC[8],
        C5 * KC[9]]
G_C6 = [C6 * KC[0], C6 * KC[1], C6 * KC[2], C6 * KC[3], C6 * KC[4], C6 * KC[5], C6 * KC[6], C6 * KC[7], C6 * KC[8],
        C6 * KC[9]]
G_C7 = [C7 * KC[0], C7 * KC[1], C7 * KC[2], C7 * KC[3], C7 * KC[4], C7 * KC[5], C7 * KC[6], C7 * KC[7], C7 * KC[8],
        C7 * KC[9]]
G_M1 = [M1 * KM[0], M1 * KM[1], M1 * KM[2], M1 * KM[3], M1 * KM[4], M1 * KM[5], M1 * KM[6], M1 * KM[7], M1 * KM[8],
        M1 * KM[9]]
G_M2 = [M2 * KM[0], M2 * KM[1], M2 * KM[2], M2 * KM[3], M2 * KM[4], M2 * KM[5], M2 * KM[6], M2 * KM[7], M2 * KM[8],
        M2 * KM[9]]
G_M3 = [M3 * KM[0], M3 * KM[1], M3 * KM[2], M3 * KM[3], M3 * KM[4], M3 * KM[5], M3 * KM[6], M3 * KM[7], M3 * KM[8],
        M3 * KM[9]]
G_M4 = [M4 * KM[0], M4 * KM[1], M4 * KM[2], M4 * KM[3], M4 * KM[4], M4 * KM[5], M4 * KM[6], M4 * KM[7], M4 * KM[8],
        M4 * KM[9]]
G_M5 = [M5 * KM[0], M5 * KM[1], M5 * KM[2], M5 * KM[3], M5 * KM[4], M5 * KM[5], M5 * KM[6], M5 * KM[7], M5 * KM[8],
        M5 * KM[9]]
G_M6 = [M6 * KM[0], M6 * KM[1], M6 * KM[2], M6 * KM[3], M6 * KM[4], M6 * KM[5], M6 * KM[6], M6 * KM[7], M6 * KM[8],
        M6 * KM[9]]
G_M7 = [M7 * KM[0], M7 * KM[1], M7 * KM[2], M7 * KM[3], M7 * KM[4], M7 * KM[5], M7 * KM[6], M7 * KM[7], M7 * KM[8],
        M7 * KM[9]]
G_M8 = [M8 * KM[0], M8 * KM[1], M8 * KM[2], M8 * KM[3], M8 * KM[4], M8 * KM[5], M8 * KM[6], M8 * KM[7], M8 * KM[8],
        M8 * KM[9]]
G_M9 = [M9 * KM[0], M9 * KM[1], M9 * KM[2], M9 * KM[3], M9 * KM[4], M9 * KM[5], M9 * KM[6], M9 * KM[7], M9 * KM[8],
        M9 * KM[9]]
G_M10 = [M10 * KM[0], M10 * KM[1], M10 * KM[2], M10 * KM[3], M10 * KM[4], M10 * KM[5], M10 * KM[6], M10 * KM[7],
         M10 * KM[8], M10 * KM[9]]
G_M11 = [M11 * KM[0], M11 * KM[1], M11 * KM[2], M11 * KM[3], M11 * KM[4], M11 * KM[5], M11 * KM[6], M11 * KM[7],
         M11 * KM[8], M11 * KM[9]]
G_M12 = [M12 * KM[0], M12 * KM[1], M12 * KM[2], M12 * KM[3], M12 * KM[4], M12 * KM[5], M12 * KM[6], M12 * KM[7],
         M12 * KM[8], M12 * KM[9]]
G_M13 = [M13 * KM[0], M13 * KM[1], M13 * KM[2], M13 * KM[3], M13 * KM[4], M13 * KM[5], M13 * KM[6], M13 * KM[7],
         M13 * KM[8], M13 * KM[9]]
G_M14 = [M14 * KM[0], M14 * KM[1], M14 * KM[2], M14 * KM[3], M14 * KM[4], M14 * KM[5], M14 * KM[6], M14 * KM[7],
         M14 * KM[8], M14 * KM[9]]
G_M15 = [M15 * KM[0], M15 * KM[1], M15 * KM[2], M15 * KM[3], M15 * KM[4], M15 * KM[5], M15 * KM[6], M15 * KM[7],
         M15 * KM[8], M15 * KM[9]]
G_M16 = [M16 * KM2[0], M16 * KM2[1], M16 * KM2[2], M16 * KM2[3], M16 * KM2[4], M16 * KM2[5], M16 * KM2[6], M16 * KM2[7],
         M16 * KM2[8], M16 * KM2[9]]
G_R2 = [R2 * KR[0], R2 * KR[1], R2 * KR[2], R2 * KR[3], R2 * KR[4], R2 * KR[5], R2 * KR[6], R2 * KR[7], R2 * KR[8],
        R2 * KR[9]]
G_R3 = [R3 * KR[0], R3 * KR[1], R3 * KR[2], R3 * KR[3], R3 * KR[4], R3 * KR[5], R3 * KR[6], R3 * KR[7], R3 * KR[8],
        R3 * KR[9]]
G_R4 = [R4 * KR[0], R4 * KR[1], R4 * KR[2], R4 * KR[3], R4 * KR[4], R4 * KR[5], R4 * KR[6], R4 * KR[7], R4 * KR[8],
        R4 * KR[9]]
G_R5 = [R5 * KR[0], R5 * KR[1], R5 * KR[2], R5 * KR[3], R5 * KR[4], R5 * KR[5], R5 * KR[6], R5 * KR[7], R5 * KR[8],
        R5 * KR[9]]
G_R6 = [R6 * KR[0], R6 * KR[1], R6 * KR[2], R6 * KR[3], R6 * KR[4], R6 * KR[5], R6 * KR[6], R6 * KR[7], R6 * KR[8],
        R6 * KR[9]]
G_R7 = [R7 * KR[0], R7 * KR[1], R7 * KR[2], R7 * KR[3], R7 * KR[4], R7 * KR[5], R7 * KR[6], R7 * KR[7], R7 * KR[8],
        R7 * KR[9]]
G_R8 = [R8 * KR[0], R8 * KR[1], R8 * KR[2], R8 * KR[3], R8 * KR[4], R8 * KR[5], R8 * KR[6], R8 * KR[7], R8 * KR[8],
        R8 * KR[9]]
G_R9 = [R9 * KR[0], R9 * KR[1], R9 * KR[2], R9 * KR[3], R9 * KR[4], R9 * KR[5], R9 * KR[6], R9 * KR[7], R9 * KR[8],
        R9 * KR[9]]
G_RZ1 = [RZ1 * KR[0], RZ1 * KR[1], RZ1 * KR[2], RZ1 * KR[3], RZ1 * KR[4], RZ1 * KR[5], RZ1 * KR[6], RZ1 * KR[7],
         RZ1 * KR[8], RZ1 * KR[9]]
G_RZ2 = [RZ2 * KR[0], RZ2 * KR[1], RZ2 * KR[2], RZ2 * KR[3], RZ2 * KR[4], RZ2 * KR[5], RZ2 * KR[6], RZ2 * KR[7],
         RZ2 * KR[8], RZ2 * KR[9]]
G_RZ3 = [RZ3 * KR[0], RZ3 * KR[1], RZ3 * KR[2], RZ3 * KR[3], RZ3 * KR[4], RZ2 * KR[5], RZ2 * KR[6], RZ2 * KR[7],
         RZ2 * KR[8], RZ3 * KR[9]]
G_D4 = [D4 * KD[0], D4 * KD[1], D4 * KD[2], D4 * KD[3], D4 * KD[4], D4 * KD[5], D4 * KD[6], D4 * KD[7], D4 * KD[8],
        D4 * KD[9]]
G_T1 = [T1 * KD[0], T1 * KD[1], T1 * KD[2], T1 * KD[3], T1 * KD[4], T1 * KD[5], T1 * KD[6], T1 * KD[7], T1 * KD[8],
        T1 * KD[9]]
G_TR = [TR * KTR[0], TR * KTR[1], TR * KTR[2], TR * KTR[3], TR * KTR[4], TR * KTR[5], TR * KTR[6], TR * KTR[7],
        TR * KTR[8], TR * KTR[9]]

# Вычисляем ВБР для всех входящих элементов
# Поток отказов для мажарированной дублированной
# 1 Для начал вычислим поток отказов мажоритарного узла
for x in range(len(G_RZ2)):
    GM_MAZ[x] = G_M16[x] + G_R2[x] + G_R6[x] + G_R6[x] + G_RZ3[x]
    # голосование 2 из 3
    G_MAZ[x] = G_M9[x] + (3 * (GM_MAZ[x] * 2) - 2 * (GM_MAZ[x] * 3))
    # 2 Теперь переменожим все интенсивности отказов и получим массив с 10 значениями для каждой температуры
    G_MAZH[x] = G_MAZ[x] + \
                G_R1[x] + \
                G_V1[x] + G_V1[x] + \
                G_V2[x] * G_V2[x] + \
                G_D1[x] + G_D1[x] + \
                G_D2[x] + G_D2[x] + \
                G_D3[x] + G_D3[x] + \
                G_I1[x] + \
                G_I2[x] + \
                G_C1[x] + G_C1[x] + G_C1[x] + G_C1[x] + G_C1[x] + G_C1[x] + G_C1[x] + G_C1[x] + \
                G_C2[x] + \
                G_C3[x] + \
                G_C4[x] + G_C4[x] + G_C4[x] + G_C4[x] + G_C4[x] + G_C4[x] + G_C4[x] + G_C4[x] + G_C4[x] + \
                G_C4[x] + \
                G_C4[x] + G_C4[x] + G_C4[x] + G_C4[x] + G_C4[x] + G_C4[x] + G_C4[x] + G_C4[x] + G_C4[x] + \
                G_C4[x] + \
                G_C5[x] + G_C5[x] + \
                G_C6[x] + G_C6[x] + \
                G_C7[x] + G_C7[x] + G_C7[x] + \
                G_M1[x] + \
                G_M2[x] + G_M2[x] + \
                G_M3[x] + G_M3[x] + \
                G_M4[x] + G_M4[x] + \
                G_M5[x] + \
                G_M6[x] + G_M6[x] + G_M6[x] + \
                G_M7[x] + \
                G_M8[x] + \
                G_M10[x] + G_M10[x] + G_M10[x] + G_M10[x] + \
                G_M11[x] + \
                G_M12[x] + \
                G_M13[x] + \
                G_M14[x] + G_M14[x] + \
                G_M15[x] + \
                G_R3[x] + \
                G_R4[x] + G_R4[x] + G_R4[x] + G_R4[x] + G_R4[x] + G_R4[x] + G_R4[x] + \
                G_R5[x] + \
                G_R6[x] + G_R6[x] + G_R6[x] + G_R6[x] + G_R6[x] + G_R6[x] + G_R6[x] + G_R6[x] + G_R6[x] + \
                G_R6[x] + G_R6[x] + \
                G_R6[x] + G_R6[x] + G_R6[x] + G_R6[x] + G_R6[x] + \
                G_R7[x] + G_R7[x] + \
                G_R8[x] + \
                G_R9[x] + \
                G_RZ1[x] + \
                G_RZ2[x] + \
                G_RZ3[x] + \
                G_V3[x] + \
                G_D4[x] + \
                G_T1[x] + G_T1[x] + G_T1[x] + G_T1[x] + G_T1[x] + \
                G_TR[x]
for y in range(len(R)):
    a[y] = G_MAZH[y] * 5000
    n = 2  # начнем 0
    while R[y] >= 10E-7:
        R[y] = -math.log(1 - a[y] ** (k + 2) / (a[y] ** (k + 2) + (n - k) * (1 + a[y]) ** (k + 1)))
        zip[y] = n
        n = n + 1
print ('R = '), R
print ('ZIP ='), zip
    # 3 теперь найдем а= m * гамма * Т ,  m = 2, T =5000

# 4 теперь будем подбирать R (сложная формула ГОСТ РВ 27.3.03-2005 c. 13, ф.9.3),
# n (количество модулей в ЗИП) должно давать R = 0,01
# n = 0
#R = 0

# a = 2 * G_MAZH[9] * 10000



for i in range(0, time):  # время до 90000 ч
    t = (i + 1) * 1000  # шт с мажориров _шт без маж
    P_R1 = [np.exp(-G_R1[0] * t), np.exp(-G_R1[1] * t), np.exp(-G_R1[2] * t), np.exp(-G_R1[3] * t),
            np.exp(-G_R1[4] * t),
            np.exp(-G_R1[5] * t), np.exp(-G_R1[6] * t), np.exp(-G_R1[7] * t), np.exp(-G_R1[8] * t),
            np.exp(-G_R1[9] * t)]
    P_V1 = [np.exp(-G_V1[0] * t), np.exp(-G_V1[1] * t), np.exp(-G_V1[2] * t), np.exp(-G_V1[3] * t),
            np.exp(-G_V1[4] * t),
            np.exp(-G_V1[5] * t), np.exp(-G_V1[6] * t), np.exp(-G_V1[7] * t), np.exp(-G_V1[8] * t),
            np.exp(-G_V1[9] * t)]  # 2 шт
    P_V2 = [np.exp(-G_V2[0] * t), np.exp(-G_V2[1] * t), np.exp(-G_V2[2] * t), np.exp(-G_V2[3] * t),
            np.exp(-G_V2[4] * t),
            np.exp(-G_V2[5] * t), np.exp(-G_V2[6] * t), np.exp(-G_V2[7] * t), np.exp(-G_V2[8] * t),
            np.exp(-G_V2[9] * t)]  # 2 шт
    P_D1 = [np.exp(-G_D1[0] * t), np.exp(-G_D1[1] * t), np.exp(-G_D1[2] * t), np.exp(-G_D1[3] * t),
            np.exp(-G_D1[4] * t),
            np.exp(-G_D1[5] * t), np.exp(-G_D1[6] * t), np.exp(-G_D1[7] * t), np.exp(-G_D1[8] * t),
            np.exp(-G_D1[9] * t)]  # 2 шт
    P_D2 = [np.exp(-G_D2[0] * t), np.exp(-G_D2[1] * t), np.exp(-G_D2[2] * t), np.exp(-G_D2[3] * t),
            np.exp(-G_D2[4] * t),
            np.exp(-G_D2[5] * t), np.exp(-G_D2[6] * t), np.exp(-G_D2[7] * t), np.exp(-G_D2[8] * t),
            np.exp(-G_D2[9] * t)]  # 2 шт
    P_D3 = [np.exp(-G_D3[0] * t), np.exp(-G_D3[1] * t), np.exp(-G_D3[2] * t), np.exp(-G_D3[3] * t),
            np.exp(-G_D3[4] * t),
            np.exp(-G_D3[5] * t), np.exp(-G_D3[6] * t), np.exp(-G_D3[7] * t), np.exp(-G_D3[8] * t),
            np.exp(-G_D3[9] * t)]  # 2 шт
    P_I1 = [np.exp(-G_I1[0] * t), np.exp(-G_I1[1] * t), np.exp(-G_I1[2] * t), np.exp(-G_I1[3] * t),
            np.exp(-G_I1[4] * t),
            np.exp(-G_I1[5] * t), np.exp(-G_I1[6] * t), np.exp(-G_I1[7] * t), np.exp(-G_I1[8] * t),
            np.exp(-G_I1[9] * t)]
    P_I2 = [np.exp(-G_I2[0] * t), np.exp(-G_I2[1] * t), np.exp(-G_I2[2] * t), np.exp(-G_I2[3] * t),
            np.exp(-G_I2[4] * t),
            np.exp(-G_I2[5] * t), np.exp(-G_I2[6] * t), np.exp(-G_I2[7] * t), np.exp(-G_I2[8] * t),
            np.exp(-G_I2[9] * t)]
    P_C1 = [np.exp(-G_C1[0] * t), np.exp(-G_C1[1] * t), np.exp(-G_C1[2] * t), np.exp(-G_C1[3] * t),
            np.exp(-G_C1[4] * t),
            np.exp(-G_C1[5] * t), np.exp(-G_C1[6] * t), np.exp(-G_C1[7] * t), np.exp(-G_C1[8] * t),
            np.exp(-G_C1[9] * t)]  # 8 шт
    P_C2 = [np.exp(-G_C2[0] * t), np.exp(-G_C2[1] * t), np.exp(-G_C2[2] * t), np.exp(-G_C2[3] * t),
            np.exp(-G_C2[4] * t),
            np.exp(-G_C2[5] * t), np.exp(-G_C2[6] * t), np.exp(-G_C2[7] * t), np.exp(-G_C2[8] * t),
            np.exp(-G_C2[9] * t)]
    P_C3 = [np.exp(-G_C3[0] * t), np.exp(-G_C3[1] * t), np.exp(-G_C3[2] * t), np.exp(-G_C3[3] * t),
            np.exp(-G_C3[4] * t),
            np.exp(-G_C3[5] * t), np.exp(-G_C3[6] * t), np.exp(-G_C3[7] * t), np.exp(-G_C3[8] * t),
            np.exp(-G_C3[9] * t)]
    P_C4 = [np.exp(-G_C4[0] * t), np.exp(-G_C4[1] * t), np.exp(-G_C4[2] * t), np.exp(-G_C4[3] * t),
            np.exp(-G_C4[4] * t),
            np.exp(-G_C4[5] * t), np.exp(-G_C4[6] * t), np.exp(-G_C4[7] * t), np.exp(-G_C4[8] * t),
            np.exp(-G_C4[9] * t)]  # 30 шт
    P_C5 = [np.exp(-G_C5[0] * t), np.exp(-G_C5[1] * t), np.exp(-G_C5[2] * t), np.exp(-G_C5[3] * t),
            np.exp(-G_C5[4] * t),
            np.exp(-G_C5[5] * t), np.exp(-G_C5[6] * t), np.exp(-G_C5[7] * t), np.exp(-G_C5[8] * t),
            np.exp(-G_C5[9] * t)]  # 2 шт
    P_C6 = [np.exp(-G_C6[0] * t), np.exp(-G_C6[1] * t), np.exp(-G_C6[2] * t), np.exp(-G_C6[3] * t),
            np.exp(-G_C6[4] * t),
            np.exp(-G_C6[5] * t), np.exp(-G_C6[6] * t), np.exp(-G_C6[7] * t), np.exp(-G_C6[8] * t),
            np.exp(-G_C6[9] * t)]  # 2 шт
    P_C7 = [np.exp(-G_C7[0] * t), np.exp(-G_C7[1] * t), np.exp(-G_C7[2] * t), np.exp(-G_C7[3] * t),
            np.exp(-G_C7[4] * t),
            np.exp(-G_C7[5] * t), np.exp(-G_C7[6] * t), np.exp(-G_C7[7] * t), np.exp(-G_C7[8] * t),
            np.exp(-G_C7[9] * t)]  # 3 шт
    P_M1 = [np.exp(-G_M1[0] * t), np.exp(-G_M1[1] * t), np.exp(-G_M1[2] * t), np.exp(-G_M1[3] * t),
            np.exp(-G_M1[4] * t),
            np.exp(-G_M1[5] * t), np.exp(-G_M1[6] * t), np.exp(-G_M1[7] * t), np.exp(-G_M1[8] * t),
            np.exp(-G_M1[9] * t)]
    P_M2 = [np.exp(-G_M2[0] * t), np.exp(-G_M2[1] * t), np.exp(-G_M2[2] * t), np.exp(-G_M2[3] * t),
            np.exp(-G_M2[4] * t),
            np.exp(-G_M2[5] * t), np.exp(-G_M2[6] * t), np.exp(-G_M2[7] * t), np.exp(-G_M2[8] * t),
            np.exp(-G_M2[9] * t)]  # 2 шт
    P_M3 = [np.exp(-G_M3[0] * t), np.exp(-G_M3[1] * t), np.exp(-G_M3[2] * t), np.exp(-G_M3[3] * t),
            np.exp(-G_M3[4] * t),
            np.exp(-G_M3[5] * t), np.exp(-G_M3[6] * t), np.exp(-G_M3[7] * t), np.exp(-G_M3[8] * t),
            np.exp(-G_M3[9] * t)]  # 2 шт
    P_M4 = [np.exp(-G_M4[0] * t), np.exp(-G_M4[1] * t), np.exp(-G_M4[2] * t), np.exp(-G_M4[3] * t),
            np.exp(-G_M4[4] * t),
            np.exp(-G_M4[5] * t), np.exp(-G_M4[6] * t), np.exp(-G_M4[7] * t), np.exp(-G_M4[8] * t),
            np.exp(-G_M4[9] * t)]  # 2 шт
    P_M5 = [np.exp(-G_M5[0] * t), np.exp(-G_M5[1] * t), np.exp(-G_M5[2] * t), np.exp(-G_M5[3] * t),
            np.exp(-G_M5[4] * t),
            np.exp(-G_M5[5] * t), np.exp(-G_M5[6] * t), np.exp(-G_M5[7] * t), np.exp(-G_M5[8] * t),
            np.exp(-G_M5[9] * t)]
    P_M6 = [np.exp(-G_M6[0] * t), np.exp(-G_M6[1] * t), np.exp(-G_M6[2] * t), np.exp(-G_M6[3] * t),
            np.exp(-G_M6[4] * t),
            np.exp(-G_M6[5] * t), np.exp(-G_M6[6] * t), np.exp(-G_M6[7] * t), np.exp(-G_M6[8] * t),
            np.exp(-G_M6[9] * t)]  # 3 шт
    P_M7 = [np.exp(-G_M7[0] * t), np.exp(-G_M7[1] * t), np.exp(-G_M7[2] * t), np.exp(-G_M7[3] * t),
            np.exp(-G_M7[4] * t),
            np.exp(-G_M7[5] * t), np.exp(-G_M7[6] * t), np.exp(-G_M7[7] * t), np.exp(-G_M7[8] * t),
            np.exp(-G_M7[9] * t)]  # 2 шт
    P_M8 = [np.exp(-G_M8[0] * t), np.exp(-G_M8[1] * t), np.exp(-G_M8[2] * t), np.exp(-G_M8[3] * t),
            np.exp(-G_M8[4] * t),
            np.exp(-G_M8[5] * t), np.exp(-G_M8[6] * t), np.exp(-G_M8[7] * t), np.exp(-G_M8[8] * t),
            np.exp(-G_M8[9] * t)]
    P_M9 = [np.exp(-G_M9[0] * t), np.exp(-G_M9[1] * t), np.exp(-G_M9[2] * t), np.exp(-G_M9[3] * t),
            np.exp(-G_M9[4] * t),
            np.exp(-G_M9[5] * t), np.exp(-G_M9[6] * t), np.exp(-G_M9[7] * t), np.exp(-G_M9[8] * t),
            np.exp(-G_M9[9] * t)]  # (это элемент "или" в мажоритарном узел)
    P_M10 = [np.exp(-G_M10[0] * t), np.exp(-G_M10[1] * t), np.exp(-G_M10[2] * t), np.exp(-G_M10[3] * t),
             np.exp(-G_M10[4] * t),
             np.exp(-G_M10[5] * t), np.exp(-G_M10[6] * t), np.exp(-G_M10[7] * t), np.exp(-G_M10[8] * t),
             np.exp(-G_M10[9] * t)]  # 4 шт
    P_M11 = [np.exp(-G_M11[0] * t), np.exp(-G_M11[1] * t), np.exp(-G_M11[2] * t), np.exp(-G_M11[3] * t),
             np.exp(-G_M11[4] * t),
             np.exp(-G_M11[5] * t), np.exp(-G_M11[6] * t), np.exp(-G_M11[7] * t), np.exp(-G_M11[8] * t),
             np.exp(-G_M11[9] * t)]
    P_M12 = [np.exp(-G_M12[0] * t), np.exp(-G_M12[1] * t), np.exp(-G_M12[2] * t), np.exp(-G_M12[3] * t),
             np.exp(-G_M12[4] * t),
             np.exp(-G_M12[5] * t), np.exp(-G_M12[6] * t), np.exp(-G_M12[7] * t), np.exp(-G_M12[8] * t),
             np.exp(-G_M12[9] * t)]
    P_M13 = [np.exp(-G_M13[0] * t), np.exp(-G_M13[1] * t), np.exp(-G_M13[2] * t), np.exp(-G_M13[3] * t),
             np.exp(-G_M13[4] * t),
             np.exp(-G_M13[5] * t), np.exp(-G_M13[6] * t), np.exp(-G_M13[7] * t), np.exp(-G_M13[8] * t),
             np.exp(-G_M13[9] * t)]
    P_M14 = [np.exp(-G_M14[0] * t), np.exp(-G_M14[1] * t), np.exp(-G_M14[2] * t), np.exp(-G_M14[3] * t),
             np.exp(-G_M14[4] * t),
             np.exp(-G_M14[5] * t), np.exp(-G_M14[6] * t), np.exp(-G_M14[7] * t), np.exp(-G_M14[8] * t),
             np.exp(-G_M14[9] * t)]  # 2
    P_M15 = [np.exp(-G_M15[0] * t), np.exp(-G_M15[1] * t), np.exp(-G_M15[2] * t), np.exp(-G_M15[3] * t),
             np.exp(-G_M15[4] * t),
             np.exp(-G_M15[5] * t), np.exp(-G_M15[6] * t), np.exp(-G_M15[7] * t), np.exp(-G_M15[8] * t),
             np.exp(-G_M15[9] * t)]
    P_M16 = [np.exp(-G_M16[0] * t), np.exp(-G_M16[1] * t), np.exp(-G_M16[2] * t), np.exp(-G_M16[3] * t),
             np.exp(-G_M16[4] * t),
             np.exp(-G_M16[5] * t), np.exp(-G_M16[6] * t), np.exp(-G_M16[7] * t), np.exp(-G_M16[8] * t),
             np.exp(-G_M16[9] * t)]  # 4_1 шт
    P_R2 = [np.exp(-G_R2[0] * t), np.exp(-G_R2[1] * t), np.exp(-G_R2[2] * t), np.exp(-G_R2[3] * t),
            np.exp(-G_R2[4] * t),
            np.exp(-G_R2[5] * t), np.exp(-G_R2[6] * t), np.exp(-G_R2[7] * t), np.exp(-G_R2[8] * t),
            np.exp(-G_R2[9] * t)]  # 4_1 шт
    P_R3 = [np.exp(-G_R3[0] * t), np.exp(-G_R3[1] * t), np.exp(-G_R3[2] * t), np.exp(-G_R3[3] * t),
            np.exp(-G_R3[4] * t),
            np.exp(-G_R3[5] * t), np.exp(-G_R3[6] * t), np.exp(-G_R3[7] * t), np.exp(-G_R3[8] * t),
            np.exp(-G_R3[9] * t)]
    P_R4 = [np.exp(-G_R4[0] * t), np.exp(-G_R4[1] * t), np.exp(-G_R4[2] * t), np.exp(-G_R4[3] * t),
            np.exp(-G_R4[4] * t),
            np.exp(-G_R4[5] * t), np.exp(-G_R4[6] * t), np.exp(-G_R4[7] * t), np.exp(-G_R4[8] * t),
            np.exp(-G_R4[9] * t)]  # 7 шт
    P_R5 = [np.exp(-G_R5[0] * t), np.exp(-G_R5[1] * t), np.exp(-G_R5[2] * t), np.exp(-G_R5[3] * t),
            np.exp(-G_R5[4] * t),
            np.exp(-G_R5[5] * t), np.exp(-G_R5[6] * t), np.exp(-G_R5[7] * t), np.exp(-G_R5[8] * t),
            np.exp(-G_R5[9] * t)]
    P_R6 = [np.exp(-G_R6[0] * t), np.exp(-G_R6[1] * t), np.exp(-G_R6[2] * t), np.exp(-G_R6[3] * t),
            np.exp(-G_R6[4] * t),
            np.exp(-G_R6[5] * t), np.exp(-G_R6[6] * t), np.exp(-G_R6[7] * t), np.exp(-G_R6[8] * t),
            np.exp(-G_R6[9] * t)]  # 22_16 шт
    P_R7 = [np.exp(-G_R7[0] * t), np.exp(-G_R7[1] * t), np.exp(-G_R7[2] * t), np.exp(-G_R7[3] * t),
            np.exp(-G_R7[4] * t),
            np.exp(-G_R7[5] * t), np.exp(-G_R7[6] * t), np.exp(-G_R7[7] * t), np.exp(-G_R7[8] * t),
            np.exp(-G_R7[9] * t)]  # 2 шт
    P_R8 = [np.exp(-G_R8[0] * t), np.exp(-G_R8[1] * t), np.exp(-G_R8[2] * t), np.exp(-G_R8[3] * t),
            np.exp(-G_R8[4] * t),
            np.exp(-G_R8[5] * t), np.exp(-G_R8[6] * t), np.exp(-G_R8[7] * t), np.exp(-G_R8[8] * t),
            np.exp(-G_R8[9] * t)]
    P_R9 = [np.exp(-G_R9[0] * t), np.exp(-G_R9[1] * t), np.exp(-G_R9[2] * t), np.exp(-G_R9[3] * t),
            np.exp(-G_R9[4] * t),
            np.exp(-G_R9[5] * t), np.exp(-G_R9[6] * t), np.exp(-G_R9[7] * t), np.exp(-G_R9[8] * t),
            np.exp(-G_R9[9] * t)]
    P_RZ1 = [np.exp(-G_RZ1[0] * t), np.exp(-G_RZ1[1] * t), np.exp(-G_RZ1[2] * t), np.exp(-G_RZ1[3] * t),
             np.exp(-G_RZ1[4] * t),
             np.exp(-G_RZ1[5] * t), np.exp(-G_RZ1[6] * t), np.exp(-G_RZ1[7] * t), np.exp(-G_RZ1[8] * t),
             np.exp(-G_RZ1[9] * t)]
    P_RZ2 = [np.exp(-G_RZ2[0] * t), np.exp(-G_RZ2[1] * t), np.exp(-G_RZ2[2] * t), np.exp(-G_RZ2[3] * t),
             np.exp(-G_RZ2[4] * t),
             np.exp(-G_RZ2[5] * t), np.exp(-G_RZ2[6] * t), np.exp(-G_RZ2[7] * t), np.exp(-G_RZ2[8] * t),
             np.exp(-G_RZ2[9] * t)]
    P_RZ3 = [np.exp(-G_RZ3[0] * t), np.exp(-G_RZ3[1] * t), np.exp(-G_RZ3[2] * t), np.exp(-G_RZ3[3] * t),
             np.exp(-G_RZ3[4] * t),
             np.exp(-G_RZ2[5] * t), np.exp(-G_RZ2[6] * t), np.exp(-G_RZ2[7] * t), np.exp(-G_RZ2[8] * t),
             np.exp(-G_RZ3[9] * t)]  # 4_1 шт
    P_V3 = [np.exp(-G_V3[0] * t), np.exp(-G_V3[1] * t), np.exp(-G_V3[2] * t), np.exp(-G_V3[3] * t),
            np.exp(-G_V3[4] * t),
            np.exp(-G_V3[5] * t), np.exp(-G_V3[6] * t), np.exp(-G_V3[7] * t), np.exp(-G_V3[8] * t),
            np.exp(-G_V3[9] * t)]
    P_D4 = [np.exp(-G_D4[0] * t), np.exp(-G_D4[1] * t), np.exp(-G_D4[2] * t), np.exp(-G_D4[3] * t),
            np.exp(-G_D4[4] * t),
            np.exp(-G_D4[5] * t), np.exp(-G_D4[6] * t), np.exp(-G_D4[7] * t), np.exp(-G_D4[8] * t),
            np.exp(-G_D4[9] * t)]
    P_T1 = [np.exp(-G_T1[0] * t), np.exp(-G_T1[1] * t), np.exp(-G_T1[2] * t), np.exp(-G_T1[3] * t),
            np.exp(-G_T1[4] * t),
            np.exp(-G_T1[5] * t), np.exp(-G_T1[6] * t), np.exp(-G_T1[7] * t), np.exp(-G_T1[8] * t),
            np.exp(-G_T1[9] * t)]  # 5 шт
    P_TR = [np.exp(-G_TR[0] * t), np.exp(-G_TR[1] * t), np.exp(-G_TR[2] * t), np.exp(-G_TR[3] * t),
            np.exp(-G_TR[4] * t),
            np.exp(-G_TR[5] * t), np.exp(-G_TR[6] * t), np.exp(-G_TR[7] * t), np.exp(-G_TR[8] * t),
            np.exp(-G_TR[9] * t)]

    ###########################
    # Часть 3
    ##########################

    # ВБР  МШВ без мажорирования MCHV будет списком (P(tn)... P(tn))
    for x in range(len(P_TR)):
        MCHV[x] = P_R1[x] * \
                  P_V1[x] * P_V1[x] * \
                  P_V2[x] * P_V2[x] * \
                  P_D1[x] * P_D1[x] * \
                  P_D2[x] * P_D2[x] * \
                  P_D3[x] * P_D3[x] * \
                  P_I1[x] * \
                  P_I2[x] * \
                  P_C1[x] * P_C1[x] * P_C1[x] * P_C1[x] * P_C1[x] * P_C1[x] * P_C1[x] * P_C1[x] * \
                  P_C2[x] * \
                  P_C3[x] * \
                  P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * \
                  P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * \
                  P_C5[x] * P_C5[x] * \
                  P_C6[x] * P_C6[x] * \
                  P_C7[x] * P_C7[x] * P_C7[x] * \
                  P_M1[x] * \
                  P_M2[x] * P_M2[x] * \
                  P_M3[x] * P_M3[x] * \
                  P_M4[x] * P_M4[x] * \
                  P_M5[x] * \
                  P_M6[x] * P_M6[x] * P_M6[x] * \
                  P_M7[x] * \
                  P_M8[x] * \
                  P_M10[x] * P_M10[x] * P_M10[x] * P_M10[x] * \
                  P_M11[x] * \
                  P_M12[x] * \
                  P_M13[x] * \
                  P_M14[x] * P_M14[x] * \
                  P_M15[x] * \
                  P_M16[x] * \
                  P_R2[x] * \
                  P_R3[x] * \
                  P_R4[x] * P_R4[x] * P_R4[x] * P_R4[x] * P_R4[x] * P_R4[x] * P_R4[x] * \
                  P_R5[x] * \
                  P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * \
                  P_R6[x] * \
                  P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * \
                  P_R7[x] * P_R7[x] * \
                  P_R8[x] * \
                  P_R9[x] * \
                  P_RZ1[x] * \
                  P_RZ2[x] * \
                  P_RZ3[x] * \
                  P_V3[x] * \
                  P_D4[x] * \
                  P_T1[x] * P_T1[x] * P_T1[x] * P_T1[x] * P_T1[x] * \
                  P_TR[x]

        # ВБР элементов мажоритарного узла, которые соединнных последовательно
        MAZ[x] = P_M16[x] * P_R2[x] * P_R6[x] * P_R6[x] * P_RZ3[x]
        # голосование 2 из 3
        P_MAZ[x] = P_M9[x] * (3 * (MAZ[x] ** 2) - 2 * (MAZ[x] ** 3))
        # Состав МШВ с мажорированием
        MCHV_MAZH[x] = P_MAZ[x] * \
                       P_R1[x] * \
                       P_V1[x] * P_V1[x] * \
                       P_V2[x] * P_V2[x] * \
                       P_D1[x] * P_D1[x] * \
                       P_D2[x] * P_D2[x] * \
                       P_D3[x] * P_D3[x] * \
                       P_I1[x] * \
                       P_I2[x] * \
                       P_C1[x] * P_C1[x] * P_C1[x] * P_C1[x] * P_C1[x] * P_C1[x] * P_C1[x] * P_C1[x] * \
                       P_C2[x] * \
                       P_C3[x] * \
                       P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * \
                       P_C4[x] * \
                       P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * P_C4[x] * \
                       P_C4[x] * \
                       P_C5[x] * P_C5[x] * \
                       P_C6[x] * P_C6[x] * \
                       P_C7[x] * P_C7[x] * P_C7[x] * \
                       P_M1[x] * \
                       P_M2[x] * P_M2[x] * \
                       P_M3[x] * P_M3[x] * \
                       P_M4[x] * P_M4[x] * \
                       P_M5[x] * \
                       P_M6[x] * P_M6[x] * P_M6[x] * \
                       P_M7[x] * \
                       P_M8[x] * \
                       P_M10[x] * P_M10[x] * P_M10[x] * P_M10[x] * \
                       P_M11[x] * \
                       P_M12[x] * \
                       P_M13[x] * \
                       P_M14[x] * P_M14[x] * \
                       P_M15[x] * \
                       P_R3[x] * \
                       P_R4[x] * P_R4[x] * P_R4[x] * P_R4[x] * P_R4[x] * P_R4[x] * P_R4[x] * \
                       P_R5[x] * \
                       P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * \
                       P_R6[x] * P_R6[x] * \
                       P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * P_R6[x] * \
                       P_R7[x] * P_R7[x] * \
                       P_R8[x] * \
                       P_R9[x] * \
                       P_RZ1[x] * \
                       P_RZ2[x] * \
                       P_RZ3[x] * \
                       P_V3[x] * \
                       P_D4[x] * \
                       P_T1[x] * P_T1[x] * P_T1[x] * P_T1[x] * P_T1[x] * \
                       P_TR[x]
        # дублирование без мажорирования
        D_MCHV[x] = 1 - (1 - MCHV[x]) ** 2
        # дублирование с мажорированием
        D_MCHV_MAZH[x] = 1 - (1 - MCHV_MAZH[x]) ** 2
        '''
        n = 5

        D_MCHV_ZIP = 0
        TEM = math.factorial(n-1)**(-1)


        # D_MCHV_ZIP = 1 - ((1- MCHV[x]) ** 2) * (TEM * (1 - MCHV[x]) ** n)
        D_MCHV_ZIP = 1 - ((1 - MCHV[x]) ** 2) * (TEM * (1 - MCHV[x]) ** (n-1))
        D_MCHV_ZIP_B = 1 - (1 - MCHV[x]) ** 2
        print D_MCHV_ZIP, D_MCHV_ZIP_B, TEM
        '''
        n = 1 # при 1 количество модулей ЗИП равно 0, это необходимо для работы формулы
        D_MCHV_ZIP = 0
        while D_MCHV_ZIP < 0.996:
            TEM = math.factorial(n - 1) ** (-1)
            D_MCHV_ZIP = 1 - ((1 - MCHV[x]) ** 2) * TEM * (1 - MCHV[x]) ** (n-1)
            DZIP[x] = n - 1
            # print DZIP
            n = n + 1
            if n > 40:
                break
        if x > 8:
            # print DZIP
            COUNT_ZIP = np.vstack((COUNT_ZIP, DZIP))





            # Int_ot
        ###########################
        # Часть 3
        ###########################

    VBR = np.vstack((VBR, MCHV))
    VBR_MAZH = np.vstack((VBR_MAZH, MCHV_MAZH))
    VBR_D = np.vstack((VBR_D, D_MCHV))
    VBR_D_MAZH = np.vstack((VBR_D_MAZH, D_MCHV_MAZH))
#    COUNT_ZIP = np.vstack((COUNT_ZIP, DZIP))
    T.append(t)
COUNT_ZIP = np.delete(COUNT_ZIP, 0, 0)
# print COUNT_ZIP
# np.save("T", T)
# np.save("T15", T)
# np.save("COUNT_ZIP", COUNT_ZIP)
# np.save("VBR", VBR)
# np.save("VBR_MAZH", VBR_MAZH)
# np.save("VBR_D_MAZH", VBR_D_MAZH)
# np.save("VBR_D", VBR_D)

# np.save("MCHV", MCHV)
# np.save("MCHV_MAZH", MCHV_MAZH)
# np.save("D_MCHV", D_MCHV)
# np.save("D_MCHV_MAZH", D_MCHV_MAZH)

# T, VBR_D_MAZH, D_MCHV_MAZH, MCHV ,MCHV_MAZH, D_MCHV, VBR, VBR_MAZH, VBR_D, VBR_D_MAZH
