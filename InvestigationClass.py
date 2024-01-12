from dataclasses import asdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from collectAllMeasureDataInOneFile import*
from ExperimentClass import Experiment as Exp
from thesis_general_imports import*
# import seaborn as sns



class Investigation:
    '''Class to handle two experiments and get the differential B-Field'''
    def readSensorMatrix(self):
        # read Sensor file
        self.sensorPath = r'C:\Users\freiseml\Nextcloud2\00-These Leo\00-Travail\03-PAC\00-Dataplots\\'
        self.sensorFilename = "PYTHON_GENEPAC_Sensors_3_Plan_AV_C_AR.txt"
        sensorMatrix = pd.read_csv(self.sensorPath + self.sensorFilename, sep="	", header = None)
        # print(sensorMatrix)
        self.sensoMatrix = np.asarray(sensorMatrix)
        return self.sensoMatrix
    
    def creatSensorMapping(self):
        self.sensorsOfInterestArray = np.zeros((len(self.sensorArray),7))
        # fill sensormatrix with x y z u v w B-Field
        lengthOfSensorArray = len(self.sensorArray)
        sensorData = np.multiply(self.diffBField,1)
        for i in range(0,lengthOfSensorArray):
            line = self.sensorArray[i]
            self.sensorsOfInterestArray [i, 0:6] = self.sensoMatrix[line, :]
            self.sensorsOfInterestArray [i, -1] = sensorData[line]*self.FaultExperiment.arrayScaleFactor

        # print(self.sensorsOfInterestArray)
        # Save as .txt
        np.savetxt(self.savepath+'SensorPositionsWithFields.txt', np.multiply(self.sensorsOfInterestArray,1), delimiter='\t')  
        return self.sensorsOfInterestArray

    def plotHealthyAndFaultyField(self):
        # vizualize both, the healthy and the faulty B-Field
        if self.FaultExperiment.year == 2020:
            ylimBFieldUp = 250
            ylimBFieldDown = -250
        elif self.FaultExperiment.year == 2021:
            ylimBFieldUp = 100
            ylimBFieldDown = -100
        elif self.FaultExperiment.year == 2017:
            ylimBFieldUp = 40
            ylimBFieldDown = -40
        # print("Visualization of healthy, faulty and diff Field")
        f2 = plt.subplots(1, 1, figsize=set_size(), sharey=True)
        plt.plot(np.multiply(self.RefExperiment.scaledField, self.FaultExperiment.arrayPlotFactor), label = "Reference Fuel Cell B-Field in $\mu$T", color = specific_colors['G2EGreen'])
        plt.plot(np.multiply(self.FaultExperiment.scaledField, self.FaultExperiment.arrayPlotFactor), label = "Investigated Fuel Cell B-Field in $\mu$T", color = specific_colors['FaultyCell'])
        plt.plot(np.multiply(self.diffBField,self.FaultExperiment.arrayPlotFactor), label = "Dif B-Field in $\mu$T", color = specific_colors['MPM_red'])
        plt.xlim(0,len(self.diffBField)-1)
        plt.ylim(ylimBFieldDown,ylimBFieldUp)
        ymin = -180
        ymax = 150  
        plt.vlines(30,ymin, ymax,'b')
        plt.vlines(60,ymin, ymax,'b')
        plt.vlines(90,ymin, ymax,'b')
        plt.vlines(120,ymin, ymax,'b')
        plt.vlines(150,ymin, ymax,'b')
        plt.legend()
        plt.title('B-Field comparison:\n {date} between {ref} and {faulty} for {amps} A'.format(date = self.FaultExperiment.date, ref = self.RefExperiment.name, faulty = self.FaultExperiment.name, amps = self.FaultExperiment.scaleCurrentTo))
        plt.xlabel("Sensor number")
        plt.ylabel("Magnetic Induction ($\mu$T)")
        plt.savefig(self.savepath + self.FaultExperiment.name + "_B_diffFields.pdf")

    def plotDiffField(self):
        # vizualize both, the faulty B-Field
        # print("Visualization of diff Field")
        f3 = plt.subplots(1, 1, figsize=set_size(), sharey=True)
        plt.plot(np.multiply(self.diffBField,self.FaultExperiment.arrayPlotFactor), label = "Dif B-Field in $\mu$T", color = specific_colors['MPM_red'])
        plt.xlim(0,len(self.diffBField)-1)
        # plt.ylim(-10,10)
        #plt.title('Differential B-Field caused by {faulty} for {amps} A the {date}'.format(date = self.FaultExperiment.date, faulty = self.FaultExperiment.name, amps = self.FaultExperiment.scaleCurrentTo))
        ymin = -30
        ymax = 30  
        plt.ylim((ymin,ymax))
        plt.vlines(30,ymin, ymax,'b')
        plt.vlines(60,ymin, ymax,'b')
        plt.vlines(90,ymin, ymax,'b')
        plt.vlines(120,ymin, ymax,'b')
        plt.vlines(150,ymin, ymax,'b')
        plt.legend()
        plt.xlabel("Sensor number")
        plt.ylabel("Magnetic Induction ($\mu$T)")
        plt.savefig(self.savepath + self.FaultExperiment.name + "_B_diffField.pdf")

    def plotInvestiagtedField(self):
        # vizualize the faulty B-Field
        # print("Visualization of Investigated diff Field")
        f4 = plt.subplots(1, 1, figsize=set_size(), sharey=True)
        # plt.tight_layout()
        plt.plot(np.multiply(self.sensorsOfInterestArray[:,-1],self.FaultExperiment.arrayDiffFieldFactor), label = " Investigated dif B-Field in $\mu$T", color = specific_colors['MPM_red'])
        plt.xlim(0,len(self.sensorsOfInterestArray)-1)
        plt.ylim(-15,15)
        #plt.title('Differential B-Field caused by {faulty} for {amps} A the {date}'.format(date = self.FaultExperiment.date, faulty = self.FaultExperiment.name, amps = self.FaultExperiment.scaleCurrentTo))
        plt.legend()
        plt.xlabel("Sensor number")
        plt.ylabel("Magnetic Induction ($\mu$T)")
        plt.savefig(self.savepath + self.FaultExperiment.name + "_Investig_B_diffField.pdf")

    def plotPolarCompFieldsOfExperiments(self):  #plotNbLayer = 1 , plotU = True, plotV = bool, 
        ''' Plot for each layer array position Bu above Bw and experiment together --> 3 x 2 plots with each two colors
        - interest is to determine outliers with a visual method
        - SensorsOfInterest:  np.linspace(2, 32, 30, dtype=int), dataSet = testExperiment.bFieldDataC, ringsStd = [0, 0.25,  0.5, 0.75], ringsData = [-100, -50, 0, 50, 100]
        titleInformationData = "With(/Without) noise"
        ''' 
        ringsData = [-100, -50, 0, 50, 100]
        ## plot sensor circle with errorbars:
        # Calculate standard deviation of each Sensor:
        sensorsOfInterest = 30
        refDataAVBu = np.zeros(sensorsOfInterest)
        invDataAVBu = np.zeros(sensorsOfInterest)
        refDataAVBw = np.zeros(sensorsOfInterest)
        invDataAVBw = np.zeros(sensorsOfInterest)

        refDataCBu = np.zeros(sensorsOfInterest)
        invDataCBu = np.zeros(sensorsOfInterest)
        refDataCBw = np.zeros(sensorsOfInterest)
        invDataCBw = np.zeros(sensorsOfInterest)

        refDataARBu = np.zeros(sensorsOfInterest)
        invDataARBu = np.zeros(sensorsOfInterest)
        refDataARBw = np.zeros(sensorsOfInterest)
        invDataARBw = np.zeros(sensorsOfInterest)
        npos = 0

        for i in range(0,30):
            refDataAVBu[npos] = self.RefExperiment.measuredCleanField[i] * 1E6
            invDataAVBu[npos] = self.FaultExperiment.measuredCleanField[i] * 1E6
            refDataAVBw[npos] = self.RefExperiment.measuredCleanField[29 + i] * 1E6
            invDataAVBw[npos] = self.FaultExperiment.measuredCleanField[29 + i] * 1E6

            refDataCBu[npos] = self.RefExperiment.measuredCleanField[59 + i] * 1E6
            invDataCBu[npos] = self.FaultExperiment.measuredCleanField[59 + i] * 1E6
            refDataCBw[npos] = self.RefExperiment.measuredCleanField[89 + i] * 1E6
            invDataCBw[npos] = self.FaultExperiment.measuredCleanField[89 + i] * 1E6

            refDataARBu[npos] = self.RefExperiment.measuredCleanField[119 + i] * 1E6
            invDataARBu[npos] = self.FaultExperiment.measuredCleanField[119 + i] * 1E6
            refDataARBw[npos] = self.RefExperiment.measuredCleanField[149 + i] * 1E6
            invDataARBw[npos] = self.FaultExperiment.measuredCleanField[149 + i] * 1E6

            npos = npos + 1

        # get angle position of each sensor around the FC-Stack
        theta = np.arange(0, 2 * np.pi, np.pi / 15)
        

        ## plot Standard Deviation on sensors
        fig, ax1 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax1.errorbar(theta, refDataAVBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax1.errorbar(theta, invDataAVBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="red")
        ax1.set_title("AV: $B_u$ measured on sensors "+ "\n" +self.RefExperiment.name + " " + self.RefExperiment.date + " and \n" + self.FaultExperiment.name + " " + self.FaultExperiment.date)
        ax1.set_rticks(ringsData)
        fig.savefig(self.FaultExperiment.bFieldPath + "InvestigationPolarCompAVBu.pdf")

        ## plot Values on sensors
        fig, ax2 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax2.errorbar(theta, refDataAVBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax2.errorbar(theta, invDataAVBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="red")
        ax2.set_title("AV: $B_w$ measured on sensors "+ "\n" +self.RefExperiment.name + " " + self.RefExperiment.date + " and \n" + self.FaultExperiment.name + " " + self.FaultExperiment.date)
        ax2.set_rticks(ringsData)
        fig.savefig(self.FaultExperiment.bFieldPath + "InvestigationPolarCompAVBw.pdf")

        fig, ax3 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax3.errorbar(theta, refDataCBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax3.errorbar(theta, invDataCBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="red")
        ax3.set_title("Center: $B_u$ measured on sensors "+ "\n" +self.RefExperiment.name + " " + self.RefExperiment.date + " and \n" + self.FaultExperiment.name + " " + self.FaultExperiment.date)
        ax3.set_rticks(ringsData)
        fig.savefig(self.FaultExperiment.bFieldPath + "InvestigationPolarCompCBu.pdf")

        ## plot Values on sensors
        fig, ax4 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax4.errorbar(theta, refDataCBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax4.errorbar(theta, invDataCBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="red")
        ax4.set_title("Center: $B_w$ measured on sensors "+ "\n" +self.RefExperiment.name + " " + self.RefExperiment.date + " and \n" + self.FaultExperiment.name + " " + self.FaultExperiment.date)
        ax4.set_rticks(ringsData)
        fig.savefig(self.FaultExperiment.bFieldPath + "InvestigationPolarCompCBw.pdf")

        fig, ax3 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax3.errorbar(theta, refDataARBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax3.errorbar(theta, invDataARBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="red")
        ax3.set_title("AR: $B_u$ measured on sensors "+ "\n" +self.RefExperiment.name + " " + self.RefExperiment.date + " and \n" + self.FaultExperiment.name + " " + self.FaultExperiment.date)
        ax3.set_rticks(ringsData)
        fig.savefig(self.FaultExperiment.bFieldPath + "InvestigationPolarCompARBu.pdf")

        ## plot Values on sensors
        fig, ax4 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax4.errorbar(theta, refDataARBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax4.errorbar(theta, invDataARBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="red")
        ax4.set_title("AR: $B_w$ measured on sensors "+ "\n" +self.RefExperiment.name + " " + self.RefExperiment.date + " and \n" + self.FaultExperiment.name + " " + self.FaultExperiment.date)
        ax4.set_rticks(ringsData)
        fig.savefig(self.FaultExperiment.bFieldPath + "InvestigationPolarCompARBw.pdf")

    def compOfTwoSensors(self, sensorName, figureName: str, dataSet1: pd.DataFrame, dataSet2: pd.DataFrame, experiment1: Exp, experiment2: Exp):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=set_size(), sharey=True)
        ax1.plot(dataSet1.loc[:,sensorName]*experiment1.arrayPlotFactor)
        ax1.set_x
        plt.xlim([0,len(dataSet1.loc[:,sensorName])])
        plt.xlabel("t (ms)")
        plt.ylabel("Magnetic Induction ($\mu$T)")
        

        ax2.plot(dataSet2.loc[:,sensorName]*experiment2.arrayPlotFactor)
        factor = experiment2.arrayPlotFactor
        plt.xlabel("t")
        plt.ylabel("Magnetic Induction ($\mu$T)")
        plt.xlim([0,len(dataSet2.loc[:,sensorName])])
        ax1.set_title(figureName + " " + sensorName + " " + experiment1.date)
        ax2.set_title(figureName + " " + sensorName + " " + experiment2.date)

    def diffFieldOf180sensorsWithNOISE(self):
        # vizualize both, the faulty B-Field
        # print("Visualization of diff Field")
        f3 = plt.subplots(1, 1, figsize=set_size(), sharey=True)
        errorGraph = np.multiply((np.multiply(self.directDifferentialField,1E6) - np.multiply(self.diffBField,self.FaultExperiment.arrayPlotFactor))/np.multiply(self.directDifferentialField,1E6),100)
        plt.plot(np.multiply(self.directDifferentialField,1E6), label = "Direct Dif B-Field in $\mu$T without Noise subtraction", color = specific_colors['MPM_red'])
        plt.plot(np.multiply(self.diffBField,self.FaultExperiment.arrayPlotFactor), label = "Dif B-Field in $\mu$T with Noise subtraction", color = specific_colors['G2EGreen'])
        plt.plot(errorGraph, label = "Error in %", color = specific_colors['RawField'])
        plt.xlim(0,len(self.diffBField)-1)
        # plt.ylim(-10,10)
        #plt.title('Differential B-Field caused by {faulty} for {amps} A the {date}'.format(date = self.FaultExperiment.date, faulty = self.FaultExperiment.name, amps = self.FaultExperiment.scaleCurrentTo))
        ymin = -120
        ymax = 120  
        plt.vlines(30,ymin, ymax,'b')
        plt.vlines(60,ymin, ymax,'b')
        plt.vlines(90,ymin, ymax,'b')
        plt.vlines(120,ymin, ymax,'b')
        plt.vlines(150,ymin, ymax,'b')
        plt.legend()
        plt.xlabel("Sensor number")
        plt.ylabel("Magnetic Induction ($\mu$T)")
        plt.savefig(self.savepath + self.FaultExperiment.name + "_B_diffFieldWithNOISE.pdf")



    def __init__(self, currentDirectionIsTheSame:bool, RefExperiment: Exp, FaultExperiment: Exp, sensorList: list):
        self.RefExperiment = RefExperiment
        self.FaultExperiment = FaultExperiment
        ## Calculation of the differential field via the direct subtraction of Bmes2 - Bmes1. Here, we use mean fields with noise on each measurement and extract the noise by subtracting each measured mean value from measurement 2 - measurement 1.
        ## so we get the signature of the error.
        self.diffFieldONAV = self.FaultExperiment.BFieldMeanvalueWithNoiseAV - self.RefExperiment.BFieldMeanvalueWithNoiseAV
        self.diffFieldONC = self.FaultExperiment.BFieldMeanvalueWithNoiseC - self.RefExperiment.BFieldMeanvalueWithNoiseC
        self.diffFieldONAR = self.FaultExperiment.BFieldMeanvalueWithNoiseAR - self.RefExperiment.BFieldMeanvalueWithNoiseAR
        ## put all the 3 together
        self.directDifferentialField = np.append(self.diffFieldONAV, np.append(self.diffFieldONC, self.diffFieldONAR))

        self.sensorArray = sensorList
        self.sensorsOfInterestArray = np.zeros((len(sensorList),7))
        self.sensoMatrix = self.readSensorMatrix()
        self.savepath = FaultExperiment.bFieldPath
        self.currentDirectionIsTheSame = currentDirectionIsTheSame
        if self.currentDirectionIsTheSame == True: self.CurrentInversionFactor = 1
        else: self.currentDirectionIsTheSame = -1
        self.diffBField = np.subtract(FaultExperiment.scaledField,RefExperiment.scaledField)
        self.sensorsOfInterestArray = self.creatSensorMapping()
        self.plotHealthyAndFaultyField()
        # plot of diff Field with noise subtraction during experiment data treatment
        self.plotDiffField()
        self.plotInvestiagtedField()
        # plot of diff Field without noise subtraction



        
        
## Test:
# RefExperiment = 1
# FaultExperiment = 2
# sensorList = [1,2,3,4,5,6,8,9]
# testInv = Investigation(RefExperiment, FaultExperiment, sensorList)
# print(testInv.sensorsOfInterestArray)

