# coding=utf-8
# создано сотрудниками АО "НИИЧаспром"
# Данная программа предназначена для анализа надежности радиоэлектронных модулей, выполн
# !pip install brewer2mpl
#
# Import Data
import warnings

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

# % matplotlib
# from typing import List, Union


warnings.filterwarnings(action='once')

from matplotlib import rc  # для вывода русских букв

font = {'family': 'Verdana',
        'weight': 'normal'}
rc('font', **font)

# VBR = np.load("VBR.npy")
T = np.load("T15.npy")
COUNT_ZIP = np.load("COUNT_ZIP.npy")
index = np.arange(len(T))

fig1 = plt.figure(figsize=(5, 5))
ax1 = fig1.add_subplot(1, 1, 1, aspect=18)
ax1.xaxis.set_major_locator(MultipleLocator(10))
ax1.xaxis.set_minor_locator(AutoMinorLocator(1))
ax1.yaxis.set_major_locator(MultipleLocator(1))
ax1.set_xlim(0, 130)
ax1.set_ylim(0, 6)
ax1.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
for i in range(len(T)):
    ax1.bar(index[i], COUNT_ZIP[i, 9], 1, align='edge', color='orange')
#    ax1.bar(index[i], COUNT_ZIP[i, 8], 1, align='edge', color='orange')
#    ax1.bar(index[i], COUNT_ZIP[i, 7], 1, align='edge', color='green')
#   ax1.bar(index[i], COUNT_ZIP[i, 6], 1, align='edge', color='red')
#    ax1.bar(index[i], COUNT_ZIP[i, 5], 1, align='edge', color='pink')
#    ax1.bar(index[i], COUNT_ZIP[i, 4], 1, align='edge', color='brown')
#    ax1.bar(index[i], COUNT_ZIP[i, 3], 1, align='edge', color='pink')
#    ax1.bar(index[i], COUNT_ZIP[i, 2], 1, align='edge', color='gray')
#    ax1.bar(index[i], COUNT_ZIP[i, 1], 1, align='edge', color='olive')
    ax1.bar(index[i], COUNT_ZIP[i, 0], 1, align='edge', color='pink')
# два последних значения выводим отдельно для корректного отображения легенды

ax1.bar(130, COUNT_ZIP[130, 9], 1, align='edge', color='1', label=u"Температура экспуатации")
ax1.bar(130, COUNT_ZIP[130, 9], 1, align='edge', color='orange', label='t = 70' + r'C$^{\circ}$')
ax1.bar(130, COUNT_ZIP[130, 0], 1, align='edge', color='pink', label='t = 25' + r'C$^{\circ}$')

# ax1.text(4.0, -0.4, "(JSC) Scientific Research Institute For Watch Industry", fontsize=14, ha="right", color='.5')
ax1.set_xlabel(u"Время работы (тыс. ч)", fontsize=10)
ax1.set_ylabel(u"Количество МШВ в ЗИП", fontsize=10)
ax1.legend(fontsize=10)

# plt.savefig('small3.png', dpi=100)
plt.savefig('big3.png', dpi=400)
plt.show()
