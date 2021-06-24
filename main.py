# coding=utf-8
# создано сотрудниками АО "НИИЧаспром"
# Данная программа предназначена для анализа надежности радиоэлектронных модулей и системы в целом
# !pip install brewer2mpl

import numpy as np
import pandas as pd
# import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter

# % matplotlib
warnings.filterwarnings(action='once')

from matplotlib import rc  # для вывода русских букв

font = {'family': 'Verdana',  # для вывода русских букв
        'weight': 'normal'}
rc('font', **font)

# matplotlib inline

# Version
# print(mpl.__version__)  # > 3.0.0
# print(sns.__version__)  # > 0.9.0

# Значение гаммы взято из спавочника
#                 шт. Название

R1 = 0.015E-6  # 1  Блок (резистор.) Б19К-2-10кОм±10%	ОЖ0.206.018ТУ
V1 = 0.00103E-6  # 2  Вилка СНП59-64/94х11В-23-1-В	НЩ0.364.061ТУ
V2 = 0.0157E-6  # 2  Гнездо Г1,6 чер."5" В	ТУ6315.00207593842  (не нашел гамму в справочнике, взял типовую)
D1 = 0.17E-6  # 2  Диод 2Д212Б /СО 	АЕЯР.432120.177ТУ
D2 = 0.078E-6  # 2  Диод 2Д222АС 	аА0.339.327ТУ
D3 = 0.032E-6  # 2  Диод 2Д522Б	ДР3.362.029-01ТУ/02	38
I1 = 0.18E-6  # 1  индикатор ИПД148В-Л	аА0.339.189ТУ
I2 = 0.21E-6  # 1  Индикатор ИПВ72А1-4/5х7К (красный)	АЕЯР.432220.232ТУ
C1 = 0.033E-6  # 8  Конд. К10-17а-М47-22 пФ±10%-В	ОЖ0.460.107ТУ
C2 = 0.033E-6  # 2  Конд. К10-17а-М47-330 пФ±10%-В	ОЖ0.460.107ТУ
C3 = 0.033E-6  # 1  Конд. К10-17а-МП0-50 В-47 пФ±10%-1-В	ОЖ0.460.107ТУ
C4 = 0.033E-6  # 30 Конд. К10-17а-Н90-0,033 мкФ-В	ОЖ0.460.107ТУ
C5 = 0.155E-6  # 2  Конд. К53-18-20В-22 мкФ±10%-В	ОЖ0.464.136ТУ
C6 = 0.155E-6  # 2  Конд. К53-18-20В-47 мкФ±10%-В	ОЖ0.464.136ТУ
C7 = 0.155E-6  # 3  Конд. К53-18-20В-100 мкФ±10%-В	ОЖ0.464.136ТУ
M1 = 0.0291E-6  # 1 (взял типовую) Микросборка 852ИН2П	АЕЯР.431230.419ТУ
M2 = 0.0485E-6  # 2 (типовая 386 бит ЗУ)Микросхема 1533АП6*5	бК0.347.364-55ТУ
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
M16 = 0.4362E-6  # 4_1  (типовая для макс. знач. ЗУ) Микросхема РIС17С44-33 I/P(40)
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
V3 = 0.00074E-6  # 1  Розетка РП15-9 ГВФ-В "5"	НКЦС.434410.509ТУ
D4 = 0.01E-6  # 1  Стабилитрон 2С147В 	СМ3.362.839ТУ
T1 = 0.036E-6  # 5  Транзистор 2Т208А (3л)	ЮФ3.365.035ТУ
TR = 0.0019E-6  # 1  Трансформатор ТИЛ3В "5"	АГ0.472.105ТУ

exp = 2.71828

vbr = []
vbr1 = []
T = []

for t in range(1, 90000, 1000):
    P_R1 = exp ** (-R1 * t)
    P_V1 = exp ** (-V1 * t)  # 2 шт
    P_V2 = exp ** (-V2 * t)  # 2 шт
    P_D1 = exp ** (-D1 * t)  # 2 шт
    P_D2 = exp ** (-D2 * t)  # 2 шт
    P_D3 = exp ** (-D3 * t)  # 2 шт
    P_I1 = exp ** (-I1 * t)
    P_I2 = exp ** (-I2 * t)
    P_C1 = exp ** (-C1 * t)  # 8 шт
    P_C2 = exp ** (-C2 * t)
    P_C3 = exp ** (-C3 * t)
    P_C4 = exp ** (-C4 * t)  # 30 шт
    P_C5 = exp ** (-C5 * t)  # 2 шт
    P_C6 = exp ** (-C6 * t)  # 2 шт
    P_C7 = exp ** (-C7 * t)  # 3 шт
    P_M1 = exp ** (-M1 * t)
    P_M2 = exp ** (-M2 * t)  # 2 шт
    P_M3 = exp ** (-M3 * t)  # 2 шт
    P_M4 = exp ** (-M4 * t)  # 2 шт
    P_M5 = exp ** (-M5 * t)
    P_M6 = exp ** (-M6 * t)  # 3 шт
    P_M7 = exp ** (-M7 * t)  # 2 шт
    P_M8 = exp ** (-M8 * t)
    P_M9 = exp ** (-M9 * t)  # (это элемент или в мажоритарном узел)
    P_M10 = exp ** (-M10 * t)  # 4 шт
    P_M11 = exp ** (-M11 * t)
    P_M12 = exp ** (-M12 * t)
    P_M13 = exp ** (-M13 * t)
    P_M14 = exp ** (-M14 * t)  # 2
    P_M15 = exp ** (-M15 * t)
    P_M16 = exp ** (-M16 * t)  # 4_1 шт
    P_R2 = exp ** (-R2 * t)  # 4_1 шт
    P_R3 = exp ** (-R3 * t)
    P_R4 = exp ** (-R4 * t)  # 7 шт
    P_R5 = exp ** (-R5 * t)
    P_R6 = exp ** (-R6 * t)  # 22_16 шт
    P_R7 = exp ** (-R7 * t)  # 2 шт
    P_R8 = exp ** (-R8 * t)
    P_R9 = exp ** (-R9 * t)
    P_RZ1 = exp ** (-RZ1 * t)
    P_RZ2 = exp ** (-RZ2 * t)
    P_RZ3 = exp ** (-RZ3 * t)  # 4_1 шт
    P_V3 = exp ** (-V3 * t)
    P_D4 = exp ** (-D4 * t)
    P_T1 = exp ** (-T1 * t)  # 5 шт
    P_TR = exp ** (-TR * t)

    # Состав МШВ без мажорирования (матрица MC_HV для проверки состава)

    MC_HV = P_R1 * \
            P_V1 * P_V1 * \
            P_V2 * P_V2 * \
            P_D1 * P_D1 * \
            P_D2 * P_D2 * \
            P_D3 * P_D3 * \
            P_I1 * \
            P_I2 * \
            P_C1 * P_C1 * P_C1 * P_C1 * P_C1 * P_C1 * P_C1 * P_C1 * \
            P_C2 * \
            P_C3 * \
            P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * \
            P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * \
            P_C5 * P_C5 * \
            P_C6 * P_C6 * \
            P_C7 * P_C7 * P_C7 * \
            P_M1 * \
            P_M2 * P_M2 * \
            P_M3 * P_M3 * \
            P_M4 * P_M4 * \
            P_M5 * \
            P_M6 * P_M6 * P_M6 * \
            P_M7 * \
            P_M8 * \
            P_M10 * P_M10 * P_M10 * P_M10 * \
            P_M11 * \
            P_M12 * \
            P_M13 * \
            P_M14 * P_M14 * \
            P_M15 * \
            P_M16 * \
            P_R2 * \
            P_R3 * \
            P_R4 * P_R4 * P_R4 * P_R4 * P_R4 * P_R4 * P_R4 * \
            P_R5 * \
            P_R6 * P_R6 * P_R6 * P_R6 * P_R6 * P_R6 * P_R6 * P_R6 * P_R6 * P_R6 * P_R6 * \
            P_R6 * P_R6 * P_R6 * P_R6 * \
            P_R7 * P_R7 * \
            P_R8 * \
            P_R9 * \
            P_RZ1 * \
            P_RZ2 * \
            P_RZ3 * \
            P_V3 * \
            P_D4 * \
            P_T1 * P_T1 * P_T1 * P_T1 * P_T1 * \
            P_TR

    vbr.append(MC_HV)

    MAZ = P_M16 * P_R2 * P_R6 * P_R6 * P_RZ3  # ВБР элементов мажоритарного узла* соединнных последовательно
    P_MAZ = P_M9 * (3 * (MAZ ** 2) - 2 * (MAZ ** 3))  # голосование 2 из 3

    # Состав МШВ с мажорированием

    MCHV_MAMZ = P_MAZ * \
                P_R1 * \
                P_V1 * P_V1 * \
                P_V2 * P_V2 * \
                P_D1 * P_D1 * \
                P_D2 * P_D2 * \
                P_D3 * P_D3 * \
                P_I1 * \
                P_I2 * \
                P_C1 * P_C1 * P_C1 * P_C1 * P_C1 * P_C1 * P_C1 * P_C1 * \
                P_C2 * \
                P_C3 * \
                P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * \
                P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * P_C4 * \
                P_C5 * P_C5 * \
                P_C6 * P_C6 * \
                P_C7 * P_C7 * P_C7 * \
                P_M1 * \
                P_M2 * P_M2 * \
                P_M3 * P_M3 * \
                P_M4 * P_M4 * \
                P_M5 * \
                P_M6 * P_M6 * P_M6 * \
                P_M7 * \
                P_M8 * \
                P_M10 * P_M10 * P_M10 * P_M10 * \
                P_M11 * \
                P_M12 * \
                P_M13 * \
                P_M14 * P_M14 * \
                P_M15 * \
                P_R3 * \
                P_R4 * P_R4 * P_R4 * P_R4 * P_R4 * P_R4 * P_R4 * \
                P_R5 * \
                P_R6 * P_R6 * P_R6 * P_R6 * P_R6 * P_R6 * P_R6 * P_R6 * P_R6 * P_R6 * P_R6 * \
                P_R6 * P_R6 * P_R6 * P_R6 * P_R6 * \
                P_R7 * P_R7 * \
                P_R8 * \
                P_R9 * \
                P_RZ1 * \
                P_RZ2 * \
                P_RZ3 * \
                P_V3 * \
                P_D4 * \
                P_T1 * P_T1 * P_T1 * P_T1 * P_T1 * \
                P_TR
    vbr1.append(MCHV_MAMZ)
    T.append(t)
'''
#    print(result)
# настройки графика

plt.rc('text', usetex=True)  # использование теха

plt.style.use('seaborn-whitegrid')
sns.set_style("white")

x_values1 = T
y_values1 = vbr
x_values2 = T
y_values2 = vbr1

fig = plt.figure()
plt.grid()  # сетка
ax = fig.add_subplot(111, label="1")
ax2 = fig.add_subplot(111, label="2", frame_on=False)

# ax3=fig.add_subplot(111, label="3", frame_on=False)

ax.plot(x_values1, y_values1, color="C0")
ax.set_xlabel("x label 1", color="C0")
ax.set_ylabel(r'$y = x^2$', color="C0")
ax.tick_params(axis='x', colors="C0")
ax.tick_params(axis='y', colors="C0")
ax2.plot(x_values2, y_values2, color="C1")

plt.show()

'''

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(1, 1, 1, aspect=90000)

def minor_tick(x, pos):
    if not x % 1.0:
        return ""
    return "%.2f" % x

ax.xaxis.set_major_locator(MultipleLocator(9000.000))
ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_major_locator(MultipleLocator(0.1))
ax.yaxis.set_minor_locator(AutoMinorLocator(1))
# ax.xaxis.set_minor_formatter(FuncFormatter(minor_tick))

ax.set_xlim(0, 90000)
ax.set_ylim(0.5, 1.1)

ax.tick_params(which='major', width=1.0)
ax.tick_params(which='major', length=1.0)
ax.tick_params(which='minor', width=1.0, labelsize=1.0)
# ax.tick_params(which='minor', length=5, labelsize=10, labelcolor='0.25')

ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)

ax.plot(T, vbr, lw=2, label=u"Без мажорирования")  # ax.plot(T, vbr, c=(0.25, 0.25, 1.00), lw=2, label="Blue signal", zorder=10)
ax.plot(T, vbr1, lw=2, label=u"С мажорированием") # ax.plot(T, vbr1, c=(1.00, 0.25, 0.25), lw=2, label="Red signal")
# ax.plot(X, Y3, linewidth=0,
#        marker='o', markerfacecolor='w', markeredgecolor='k')

ax.set_title(u"Вероятность безотказной работы", fontsize=20, verticalalignment='bottom')
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


color = 'blue'
ax.annotate('Spines', xy=(4.0, 0.35), xycoords='data',
            xytext=(3.3, 0.5), textcoords='data',
            weight='bold', color=color,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3",
                            color=color))

ax.annotate('', xy=(3.15, 0.0), xycoords='data',
            xytext=(3.45, 0.45), textcoords='data',
            weight='bold', color=color,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3",
                            color=color))
'''

ax.text(4.0, -0.4, "(JSC) Scientific Research Institute For Watch Industry",
        fontsize=10, ha="right", color='.5')

plt.show()

# отображение отказа
fig1 = plt.figure(figsize=(9, 9))
ax = fig1.add_subplot(1, 1, 1, aspect=90000)

ax.xaxis.set_major_locator(MultipleLocator(9000.000))
ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_major_locator(MultipleLocator(0.1))
ax.yaxis.set_minor_locator(AutoMinorLocator(1))
# ax.xaxis.set_minor_formatter(FuncFormatter(minor_tick))

ax.set_xlim(0, 90000)
ax.set_ylim(0.5, 1.1)

ax.tick_params(which='major', width=1.0)
ax.tick_params(which='major', length=1.0)
ax.tick_params(which='minor', width=1.0, labelsize=1.0)
# ax.tick_params(which='minor', length=5, labelsize=10, labelcolor='0.25')

ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)

ax.plot(T, vbr, lw=2, label=u"Без мажорирования")  # ax.plot(T, vbr, c=(0.25, 0.25, 1.00), lw=2, label="Blue signal", zorder=10)
ax.plot(T, vbr1, lw=2, label=u"С мажорированием") # ax.plot(T, vbr1, c=(1.00, 0.25, 0.25), lw=2, label="Red signal")
# ax.plot(X, Y3, linewidth=0,
#        marker='o', markerfacecolor='w', markeredgecolor='k')

ax.set_title(u"Вероятность безотказной работы \n с моделированием отказа", fontsize=20, verticalalignment='bottom')
ax.set_xlabel(u"Время работы (ч)")
ax.set_ylabel(u"Вероятность")

ax.legend()


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


color = 'blue'
ax.annotate('Spines', xy=(4.0, 0.35), xycoords='data',
            xytext=(3.3, 0.5), textcoords='data',
            weight='bold', color=color,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3",
                            color=color))

ax.annotate('', xy=(3.15, 0.0), xycoords='data',
            xytext=(3.45, 0.45), textcoords='data',
            weight='bold', color=color,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3",
                            color=color))
'''

ax.text(4.0, -0.4, "(JSC) Scientific Research Institute For Watch Industry",
        fontsize=10, ha="right", color='.5')

plt.show()