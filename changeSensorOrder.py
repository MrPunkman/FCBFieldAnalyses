from hashlib import new
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from pathlib import Path
import os 
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import io


# call file name
filename = 'SensorsGenepac3Plans.txt'
# read file sensorposition
sensorposFile = pd.read_csv(r'C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\00-Dataplots\\'+filename, sep="	", header = None)

# create values to declare the sensors position and direction

# create values to declare the sensors position and direction
newOrder = np.zeros((180,6))


radintervala = 0
radintervale = 30
axintervala = 90
axintervale = 120
fPositionInNewOrder = 0
ePositionInNewOrder = 30

fPositionInNewOrder = 0
ePositionInNewOrder = 30

for orientation in range(0,3):
    for i in range(0,6):
        m = np.asarray(sensorposFile.iloc[radintervala:radintervale][i])
        newOrder[fPositionInNewOrder:ePositionInNewOrder,i] = m

    fPositionInNewOrder = fPositionInNewOrder + 30
    ePositionInNewOrder = ePositionInNewOrder + 30
    
    for i in range(0,6):
        n = np.asarray(sensorposFile.iloc[axintervala:axintervale][i])
        newOrder[fPositionInNewOrder:ePositionInNewOrder,i] = n

    fPositionInNewOrder = fPositionInNewOrder + 30
    ePositionInNewOrder = ePositionInNewOrder + 30
    radintervala = radintervala + 30
    radintervale = radintervale + 30
    axintervala = axintervala + 30
    axintervale = axintervale + 30

# export dataFrame to csv:

# filepath = Path(r'C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\00-Dataplots\newSensorOrder.csv')  

# filepath.parent.mkdir(parents=True, exist_ok=True)  
np.savetxt('PYTHON_GENEPAC_Sensors_3_Plan_AV_C_AR.txt', newOrder, delimiter='\t',fmt="%.9f")

# df = pd.DataFrame(newOrder)

# df.to_csv(filepath,sep=' ',index=False) 

#df.to_csv(index=False,sep=' ')

intervala = 0
intervale = 180
 
x = newOrder.T[intervala:intervale][0]
y = newOrder.T[intervala:intervale][1]
z = newOrder.T[intervala:intervale][2]
u = newOrder.T[intervala:intervale][3]
v = newOrder.T[intervala:intervale][4]
w = newOrder.T[intervala:intervale][5]


# fig = plt.figure()
# ax = fig.gca(projection='3d')
# ax.quiver(x, y, z, u, v, w, length = 0.01, normalize=True)
# ax.set_xlim(-0.15, 0.15)
# ax.set_ylim(-0.15, 0.15)
# ax.set_zlim(-0.04, 0.04)
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# # ax.quiver(newOrder[:][0],newOrder[:][1],newOrder[:][2],newOrder[:][3],newOrder[:][4],newOrder[:][5],length =0.1, normalize=True)
# # f = io.BytesIO()
# # ET.ElementTree(tree).write('svg_tooltip.svg')
# # ax.set_aspect('equal')
# plt.show()
# plt.savefig(sensorposFile + filename[0: -4] + "ordered.svg") #, format="svg"

# plt.savefig(sensorposFile + filename + "ordered.pdf")
