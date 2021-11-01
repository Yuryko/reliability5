# coding=utf-8
# создано сотрудниками АО "НИИЧаспром"
# Данная программа предназначена для анализа надежности радиоэлектронных модулей, выполн
# !pip install brewer2mpl
#
# Import Data

import numpy as np
import matplotlib.pyplot as plt

# VBR = np.load("VBR.npy")
T = np.load("T15.npy")
COUNT_ZIP = np.load("COUNT_ZIP.npy")
# series1 = np.array([3,4,5,3])
# series2 = np.array([1,2,2,5])
# series3 = np.array([2,3,3,4])
'''
index = np.arange(len(T))
# plt.axis([1, 13001, 0, 8])
for i in range(len(T+1)):
    plt.bar(index[i], COUNT_ZIP[i, 9], color='g')
    plt.bar(index[i], COUNT_ZIP[i, 3], color='b')
    
'''
plt.show()
