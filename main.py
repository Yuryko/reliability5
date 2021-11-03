# coding=utf-8
# создано сотрудниками АО "НИИЧаспром"
# Данная программа предназначена для анализа надежности радиоэлектронных модулей, выполн
# !pip install brewer2mpl
import math

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
from math import e

Z = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70]  # Температура для которой расчитывается коэффициент

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
# Часть 1 - 4  в файле MSHV.py
###########################

'''Часть 5'''
T = np.load("T.npy")
VBR = np.load("VBR.npy")
VBR_MAZH = np.load("VBR_MAZH.npy")
VBR_D_MAZH = np.load("VBR_D_MAZH.npy")
VBR_D = np.load("VBR_D.npy")

MCHV = np.load("MCHV.npy")
MCHV_MAZH = np.load("MCHV_MAZH.npy")
D_MCHV = np.load("D_MCHV.npy")
D_MCHV_MAZH = np.load("D_MCHV_MAZH.npy")

fig = plt.figure(figsize=(10, 10))
# plt.tick_params(axis='both', which='major', labelsize=14)
plt.rcParams['font.size'] = '14'
ax = fig.add_subplot(1, 1, 1, aspect=T[-1] + 100000)

def minor_tick(x, pos):
    if not x % 1.0:
        return ""
    return "%.2f" % x

ax.xaxis.set_major_locator(MultipleLocator(10000.000))
#ax.xaxis.set_major_locator(MultipleLocator(10000.000)) для гигантских картинок
ax.xaxis.set_minor_locator(AutoMinorLocator(9))
ax.yaxis.set_major_locator(MultipleLocator(0.025))

# ax.yaxis.set_minor_locator(AutoMinorLocator(2))
# ax.xaxis.set_minor_formatter(FuncFormatter(minor_tick))

ax.set_xlim(0, T[-1] + 1000)
ax.set_ylim(0.55, 1.01)

# ax.tick_params(which='major', width=1.0)
# ax.tick_params(which='major', length=1.0)
# ax.tick_params(which='minor', width=1.0, labelsize=1.0)
# ax.tick_params(which='minor', length=5, labelsize=10, labelcolor='0.25')

ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)

ax.plot(T, VBR[0:len(T), 0], lw=2, label=u"без мажорирования")  # ax.plot(T, vbr, c=(0.25, 0.25, 1.00), lw=2, label="Blue signal", zorder=10)
ax.plot(T, VBR_MAZH[0:len(T), 0], lw=2, label=u"мажорирование без дублирования")  # ax.plot(T, vbr1, c=(1.00, 0.25, 0.25), lw=2, label="Red signal")
ax.plot(T, VBR_D[0:len(T), 0], lw=2, label=u"дублирование без мажорирования")
ax.plot(T, VBR_D_MAZH[0:len(T), 0], lw=2, label=u"дублирование и мажорирование")

# ax.plot(X, Y3, linewidth=0,
#        marker='o', markerfacecolor='w', markeredgecolor='k')

# ax.set_title(u"Вероятность безотказной работы", fontsize=20, verticalalignment='bottom')
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
            xytext=(T[-1] - 15000, 0.65), textcoords='data',
            weight='bold', color=color, fontsize=14,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3",
                            color=color))

ax.annotate(rel_mazh, xy=(T[-1] - 150, MCHV_MAZH[0]), xycoords='data',
            xytext=(T[-1] - 15000, 0.7), textcoords='data',
            weight='bold', color=color, fontsize=14,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3", color=color))

ax.annotate(rel_d, xy=(T[-1] - 150, D_MCHV[0]), xycoords='data',
            xytext=(T[-1] - 15000, 0.85), textcoords='data',
            weight='bold', color=color, fontsize=14,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3", color=color))
ax.annotate(rel_mazh_d, xy=(T[-1] - 100, D_MCHV_MAZH[0]), xycoords='data',
            xytext=(T[-1] - 15000, 0.9), textcoords='data',
            weight='bold', color=color, fontsize=14,
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
        fontsize=14, ha="right", color='.5')


rel = []    # подписи к осям

fig1 = plt.figure(figsize=(10, 10))
ax1 = fig1.add_subplot(1, 1, 1, aspect=T[-1] + 220000)

# ax1 = fig1.add_subplot(1, 1, 1, aspect=T[-1] + 220000) для гиганских картинок

ax1.xaxis.set_major_locator(MultipleLocator(10000.000))
# ax1.xaxis.set_major_locator(MultipleLocator(10000.000))  для гиганских картинок

ax1.xaxis.set_minor_locator(AutoMinorLocator(9))
ax1.yaxis.set_major_locator(MultipleLocator(0.025))

ax1.set_xlim(0, T[-1] + 1000)
ax1.set_ylim(0.72, 1.01)

ax1.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)

# ax1.annotate(r't, C$^{\circ}$', xy=(T[-1] - 100, D_MCHV_MAZH[5]), xycoords='data',
#            xytext=(T[-1] + 1000, 1.01), textcoords='data',
#            weight='bold', color=color)


for x in range(len(Z)):
    ax1.plot(T, VBR_D_MAZH[0:len(T), x], lw=2, label='t='+(str(Z[x]))+r'C$^{\circ}$')
    rel.append(str(round(D_MCHV_MAZH[x], 3)))
    ax1.annotate(rel[x], xy=(T[-1] - 100, D_MCHV_MAZH[x]), xycoords='data',
            xytext=(T[-1] + 1000, D_MCHV_MAZH[x]), textcoords='data',
            weight='bold', color=color, fontsize=14)
#    color = 'blue'

ax1.text(4.0, -0.4, "(JSC) Scientific Research Institute For Watch Industry",
        fontsize=14, ha="right", color='.5')

ax1.set_xlabel(u"Время работы (ч)", fontsize=14)
ax1.set_ylabel(u"Вероятность", fontsize=14)
# ax1.set_zlabel(u"Вероятность")
ax1.legend(fontsize=14)



fig2 = plt.figure(figsize=(10, 10))
ax2 = fig2.add_subplot(1, 1, 1, aspect=T[-1] + 220000)

# ax1 = fig1.add_subplot(1, 1, 1, aspect=T[-1] + 220000) для гиганских картинок

ax2.xaxis.set_major_locator(MultipleLocator(10000.000)) # шкала снизу
# ax1.xaxis.set_major_locator(MultipleLocator(10000.000))  для гиганских картинок

ax2.xaxis.set_minor_locator(AutoMinorLocator(9))
ax2.yaxis.set_major_locator(MultipleLocator(0.025))

ax2.set_xlim(0, T[-1] + 100)
ax2.set_ylim(0.72, 1.01)

ax2.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)

# ax1.annotate(r't, C$^{\circ}$', xy=(T[-1] - 100, D_MCHV_MAZH[5]), xycoords='data',
#            xytext=(T[-1] + 1000, 1.01), textcoords='data',
#            weight='bold', color=color)

# график 25 градусов
ax2.plot(T, VBR_D_MAZH[0:len(T), 0], lw=2, label='t='+(str(Z[0]))+r'C$^{\circ}$')
rel.append(str(round(D_MCHV_MAZH[0], 30)))
ax2.annotate(rel[0], xy=(T[-1] - 100, D_MCHV_MAZH[0]), xycoords='data',
             xytext=(T[-1] + 1000, D_MCHV_MAZH[0]), textcoords='data',
             weight='bold', color=color, fontsize=14)
#    color = 'blue'

# график 75 градусов
ax2.plot(T, VBR_D_MAZH[0:len(T), 9], lw=2, label='t='+(str(Z[9]))+r'C$^{\circ}$', color = 'blue')
rel.append(str(round(D_MCHV_MAZH[9], 3)))
ax2.annotate(rel[9], xy=(T[-1] - 100, D_MCHV_MAZH[9]), xycoords='data',
             xytext=(T[-1] + 1000, D_MCHV_MAZH[9]), textcoords='data',
             weight='bold', color=color, fontsize=14)

# circle(0.75, 1000, 0.5)

#ax2.annotate("coor", xy=(10000, 0.8), xycoords='data',
#            xytext=(10000, 0.9), textcoords='data',
#            weight='bold', color=color, fontsize=14,
#            arrowprops=dict(arrowstyle='wedge',
#                            connectionstyle="arc3",
#                            color=color))

ax2.plot(10000, 0.8, linewidth=0,
        marker='o', markerfacecolor='w', markeredgecolor='k')


# ax2.annotate(circle(10000, 0.8, 0.15))

#    color = 'blue'

ax2.set_xlabel(u"Время работы (ч)", fontsize=14)
ax2.set_ylabel(u"Вероятность", fontsize=14)
# ax1.set_zlabel(u"Вероятность")
ax2.legend(fontsize=14)


plt.show() # раскоментровать для графиков



