# coding=utf-8
# создано сотрудниками АО "НИИЧаспром"
# Данная программа предназначена для анализа надежности радиоэлектронных модулей, выполн
# !pip install brewer2mpl

import warnings

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

# % matplotlib
# from typing import List, Union


warnings.filterwarnings(action='once')

from matplotlib import rc  # для вывода русских букв

font = {'family': 'Verdana',
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
# Часть 1 - 4  в файле MSHV.py
###########################

'''Часть 5'''
Z = np.load("Z.npy")
T = np.load("T.npy")
VBR = np.load("VBR.npy")
VBR_MAZH = np.load("VBR_MAZH.npy")
VBR_D_MAZH = np.load("VBR_D_MAZH.npy")
VBR_D = np.load("VBR_D.npy")

MCHV = np.load("MCHV.npy")
MCHV_MAZH = np.load("MCHV_MAZH.npy")
D_MCHV = np.load("D_MCHV.npy")
D_MCHV_MAZH = np.load("D_MCHV_MAZH.npy")

print VBR
# zip = np.load("zip.npy")

fig = plt.figure(figsize=(10, 10))  # для гигантских картинок надо дописать dpi
# plt.tick_params(axis='both', which='major', labelsize=14)
plt.rcParams['font.size'] = '14'
ax = fig.add_subplot(1, 1, 1, aspect=T[-1] + 180000)  # type


def minor_tick(x, pos):
    if not x % 1.0:
        return ""
    return "%.2f" % x


ax.xaxis.set_major_locator(MultipleLocator(10000.000))
ax.xaxis.set_minor_locator(AutoMinorLocator(9))
ax.yaxis.set_major_locator(MultipleLocator(0.025))
ax.set_xlim(0, T[-1] + 1000)
ax.set_ylim(0.65, 1.01)
ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
ax.plot(T, VBR[0:len(T), 0], lw=2,
        label=u"без мажорирования")  # ax.plot(T, vbr, c=(0.25, 0.25, 1.00), lw=2, label="Blue signal", zorder=10)
ax.plot(T, VBR_MAZH[0:len(T), 0], lw=2,
        label=u"мажорирование без дублирования")  # ax.plot(T, vbr1, c=(1.00, 0.25, 0.25), lw=2, label="Red signal")
ax.plot(T, VBR_D[0:len(T), 0], lw=2, label=u"дублирование без мажорирования")
ax.plot(T, VBR_D_MAZH[0:len(T), 0], lw=2, label=u"дублирование и мажорирование")
ax.set_xlabel(u"Время работы (ч)", fontsize=14)
ax.set_ylabel(u"Вероятность", fontsize=14)
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


# стрелки с подписью про надежность
color = 'blue'
rel = str(round(MCHV[0], 3))
rel_mazh = str(round(MCHV_MAZH[0], 3))
rel_d = str(round(D_MCHV[0], 3))
rel_mazh_d = str(round(D_MCHV_MAZH[0], 3))
ax.annotate(rel, xy=(T[-1] - 150, MCHV[0]), xycoords='data',
            xytext=(T[-1] - 15000, 0.75), textcoords='data',
            weight='bold', color=color, fontsize=14,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3",
                            color=color))
ax.annotate(rel_mazh, xy=(T[-1] - 150, MCHV_MAZH[0]), xycoords='data',
            xytext=(T[-1] - 15000, 0.8), textcoords='data',
            weight='bold', color=color, fontsize=14,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3", color=color))
ax.annotate(rel_d, xy=(T[-1] - 150, D_MCHV[0]), xycoords='data',
            xytext=(T[-1] - 15000, 0.925), textcoords='data',
            weight='bold', color=color, fontsize=14,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3", color=color))
ax.annotate(rel_mazh_d, xy=(T[-1] - 100, D_MCHV_MAZH[0]), xycoords='data',
            xytext=(T[-1] - 15000, 0.975), textcoords='data',
            weight='bold', color=color, fontsize=14,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3",
                            color=color))

ax.text(4.0, -0.4, "(JSC) Scientific Research Institute For Watch Industry",
        fontsize=14, ha="right", color='.5')

rel = []  # подписи к осям

fig1 = plt.figure(figsize=(10, 10))
ax1 = fig1.add_subplot(1, 1, 1, aspect=T[-1] + 220000)
ax1.xaxis.set_major_locator(MultipleLocator(10000.000))
ax1.xaxis.set_minor_locator(AutoMinorLocator(9))
ax1.yaxis.set_major_locator(MultipleLocator(0.025))
ax1.set_xlim(0, T[-1] + 1000)
ax1.set_ylim(0.72, 1.01)
ax1.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
for x in range(len(Z)):
    ax1.plot(T, VBR_D_MAZH[0:len(T), x], lw=2, label='t=' + (str(Z[x])) + r'C$^{\circ}$')
    rel.append(str(round(D_MCHV_MAZH[x], 3)))
    ax1.annotate(rel[x], xy=(T[-1] - 100, D_MCHV_MAZH[x]), xycoords='data',
                 xytext=(T[-1] + 1000, D_MCHV_MAZH[x]), textcoords='data',
                 weight='bold', color=color, fontsize=14)
ax1.text(4.0, -0.4, "(JSC) Scientific Research Institute For Watch Industry",
         fontsize=14, ha="right", color='.5')
ax1.set_xlabel(u"Время работы (ч)", fontsize=14)
ax1.set_ylabel(u"Вероятность", fontsize=14)
ax1.legend(fontsize=14)

# fig3 = plt.figure(figsize=(10, 10))
# ax3 = fig3.add_subplot(1, 1, 1)
# ax3.hist(zip, bins=Z)


plt.show() # раскоментровать для графиков


# T, VBR_D_MAZH, D_MCHV_MAZH, MCHV_MAZH, D_MCHV, VBR, VBR_MAZH, VBR_D, VBR_D_MAZH
