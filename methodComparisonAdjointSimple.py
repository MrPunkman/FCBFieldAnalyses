from tracemalloc import stop
from turtle import color
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from collectAllMeasureDataInOneFile import*
import seaborn as sns
from scipy.fft import fft, ifft
from ExperimentClass import*
from InvestigationClass import*



#  Tool to plot heat map (rho base) heat map (result); heat map (error) convergence for CEFC 2024. Comparison of reconstruction and base 
dataPath = r'Z:\00_Sandbox\MIPSE\\'
reconstructedField =  "2023-12-11-11-14-ResultFieldAdjoint.txt"
reconstructedResistivity = "2023-12-11-11-14-ResultConAdjoint.txt"

baseField = "00-fieldBase.txt"

# 1. plot heat map for rho base
## create 5x5 matrix from data
baseResistivity = "00-rhoBase.txt"
baseResistivityArray = np.loadtxt(dataPath + baseResistivity)
baseResistivityMatrix = np.array_split(baseResistivityArray,5)
# print(baseResistivityMatrix)









# calculate plot residual
residualData = "2023-12-11-11-14-ResidualAdjoint.txt"
residualDataPoints = np.loadtxt(dataPath + residualData)
residualDataPoints = pd.DataFrame(residualDataPoints)

# rolling average by 25 points
rollingResidualDataPoints = residualDataPoints.rolling(25).sum()


# column width from latex for later plot settings
columnWidth = 252

# fig = plt.figure()
fig, axs = plt.subplots(2, 2, figsize=set_size(columnWidth,subplots=(2, 2)))

# , ax12, ax21, ax22
ax11 = axs[0,0]
ax12 = axs[0,1]
ax21 = axs[1,0]
ax22 = axs[1,1]

# ax11.plot(rollingResidualDataPoints)
ax11.imshow(baseResistivityMatrix)
label_list = np.arange(1,6, 1)
ax11.set_xticks(label_list)
ax11.set_yticks(label_list)
HM = ax11.imshow(baseResistivityMatrix, cmap = 'viridis', vmin = 0, vmax = 1.5, extent= [0, 5, 5, 0])
# plt.setp(ax11.get_xticklabels(), rotation=0, ha="left", va = "top",
#          rotation_mode="anchor")

plt.grid(True)
cbar = fig.colorbar(HM, label = "Resistivity")
# for i in range(len(baseResistivityMatrix)):
#     for j in range(len(baseResistivityMatrix)):
#         text = ax11.text(j, i, baseResistivityMatrix[i][j],  color="b")


# ax12.plot(rollingResidualDataPoints)
ax12.plot(rollingResidualDataPoints)
plt.yscale('log')
plt.ylim(1e-13, 5e-8)
plt.yticks([1e-13, 1e-10, 1e-7])

ax21.plot(rollingResidualDataPoints)
plt.yscale('log')
plt.ylim(1e-13, 5e-8)
plt.yticks([1e-13, 1e-10, 1e-7])

ax22.plot(rollingResidualDataPoints)
plt.yscale('log')
plt.ylim(1e-13, 5e-8)
plt.yticks([1e-13, 1e-10, 1e-7])

plt.show()
