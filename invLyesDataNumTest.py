from dataclasses import dataclass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from thesis_general_imports import*
import random


class invLyesData():
    def readSensorMatrix(self):
        # read Sensor file
        self.sensorPath = r'Z:\06-Sensors\01-SensorPositions\2017-Lyes\\'
        self.sensorFilename = "PYTHON_GENEPAC_Sensors_3_Plan_Bu_Bw_AV_C_AR-Lyes.txt"
        sensorMatrix = pd.read_csv(self.sensorPath + self.sensorFilename, sep="	", header = None)
        # print(sensorMatrix)
        self.sensorMatrix = np.asarray(sensorMatrix)
        return self.sensorMatrix

    def createSensorMapping(self):
        self.finalSensorsOfInterest = np.zeros((len(self.sensorsOfInterest),7))
        # fill sensor matrix with x y z u v w B-Field
        lengthOfSensorArray = len(self.sensorsOfInterest)
        self.sensorData = np.multiply(self.fullSensorArray,1)
        for i in range(0,lengthOfSensorArray):
            line = self.sensorsOfInterest[i]
            self.finalSensorsOfInterest [i, 0:6] = self.sensorMatrix[line, :]
            self.finalSensorsOfInterest [i, -1] = self.fullSensorArray[line]
            print(self.finalSensorsOfInterest[i, :])

        # print(self.sensorsOfInterestArray)
        # Save as .txt
        np.savetxt(self.path+'SensorPositionsWithFields.txt', np.multiply(self.finalSensorsOfInterest,1), delimiter='\t')  
        return self.sensorsOfInterest
    
    def plotInvestigatedField(self):
        # visualize the faulty B-Field
        # print("Visualization of Investigated diff Field")
        plotData = np.multiply(self.finalSensorsOfInterest [:, -1], 1E6)

        ## add here an option to plot the sensor number with 5 ticks on the x axes. Marker would be nice too

        # # get xticks for plots depending on sensors, used
        # ## set arrays for plot
        # xlabelPointToSet = self.sensorsOfInterest
        # xrange = np.linspace(0, 29, 30, dtype=int)
        # xrangeToSet = np.linspace(0, 4, 5, dtype=int)
        # xlabelsToSet = np.linspace(0, 4, 5, dtype=int)
        # ## define points for plotting
        # xrange = xrange%5
        # # define tick positions by full divison by 5
        # xlabelPointToSet = xlabelPointToSet%5

        # for i in range(0,5):
        #     xrangeToSet[i] = 
        #     xlabelsToSet[i] = self.sensorsOfInterest[xlabelPointToSet[i]]



        f4 = plt.subplots(1, 1, figsize=set_size(), sharey=True)
        # plt.tight_layout()
        plt.plot(plotData, label = " Investigated differential field in $\mu$T", color = specific_colors['MPM_red'], marker = "|")
        plt.xlim(0,len(self.sensorsOfInterest)-1)
        plt.xticks([0 , 10 , 20, 30])
        plt.ylim(-10,10)
        #plt.title('Differential B-Field caused by {faulty} for {amps} A the {date}'.format(date = self.FaultExperiment.date, faulty = self.FaultExperiment.name, amps = self.FaultExperiment.scaleCurrentTo))
        plt.legend()
        plt.xlabel("Sensor number")
        plt.ylabel("Magnetic Induction ($\mu$T)")
        plt.savefig(self.path + self.name + "_Investig_B_diffField.pdf")


    def createDF(self):
        """This function is to read a .lvm file and read the data without the header"""
        ## import file and set file path
        # print("reading Data start")
        df = pd.read_csv(
            self.path + self.fileName, header = None
        )
        ## change , to . for later calculations. Otherwise, the cell is declared as string and no calculation can be done
        df = df.replace(",", ".", regex=True)
        # change type to float
        df = df.astype(float)
        df = np.asarray(df)
        # print("reading Data end")
        return df
    
    def addMCtoDiffField(self):
        """Adds $B_MC$ to the diff field. Has to be executed for nonlinear method"""
        self.BmC = pd.read_csv("LyesMC.txt", header = None)
        self.BmC = self.BmC.astype(float)
        self.BmC = np.asarray(self.BmC)
        self.fullSensorArray = np.add(self.fullSensorArray, self.BmC)

    def addNoiseOnSimulatedData(self):
        # create new array to save measurement with added noise
        self.noisyFullSensorArray = np.zeros(self.fullSensorArray.shape)
        # loop over new array and add random noise between -500 and 500 nT
        rng = np.random.default_rng()
        self.noisyFullSensorArray = rng.uniform(-500,500,self.noisyFullSensorArray.shape)*1e-9 + self.fullSensorArray
        # for i in range(0,self.noisyFullSensorArray.size):
        #     noise = random.randrange(-500, 500, 1) * 1E-9
        #     element = self.fullSensorArray[i]
        #     value = noise + element
        #     self.noisyFullSensorArray[i] = value
        #     newelemnt = self.noisyFullSensorArray[i]
        r = np.linalg.norm(self.fullSensorArray - self.noisyFullSensorArray)
        print(r)
        self.fullSensorArray = self.noisyFullSensorArray

    
        

    def __init__(self, name:str , path: str, fileName:str, sensorsOfInterest:np.array):
        self.name = name
        self.path = path
        self.fileName = fileName
        self.sensorsOfInterest = sensorsOfInterest
        self.fullSensorArray = self.createDF()
        plt.plot(self.fullSensorArray)
        self.addMCtoDiffField() # use this only for non-linear!!!
        # self.addNoiseOnSimulatedData() # add this line to add some noise!!! +- 500 nT
        plt.plot(self.BmC)
        plt.plot(self.fullSensorArray)
        plt.show()
        self.readSensorMatrix()
        self.createSensorMapping()


        

############### Test
nameTest = "2_addRandomNoiseTest"
sensorsOfInterest = np.linspace(0, 29 , 30, dtype=int)

path = r'Z:\01-TestCases\01-Stability\00-noise\00\\'
fileName = "test-MagFieldOnSensors-noNoise.txt"
testClass = invLyesData(nameTest ,path, fileName, sensorsOfInterest)
print(testClass.fullSensorArray)
testClass.plotInvestigatedField()

#%%


#%%


