from dataclasses import asdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from collectAllMeasureDataInOneFile import*
from ExperimentClass import Experiment as Exp
from thesis_general_imports import*
from InvestigationClass import*
from ExperimentDescription import*
from ExperimentClass import Experiment as Exp
from deprecated import deprecated

class MultiInvestigation:
    """"Currently the present class is used to compare 3 (three) different results as used in Lyes et al. Thesis."""
    @deprecated("This Function uses the calculation of the difference between two absolute fields. Use passSensorMeasurementsWithoutNoise instead")
    def passSensorMeasurementsDirect(self):
        sensorsOfInterest = 30
        sensorPosDef = np.linspace(1,30,30,dtype=int)

        self.exp1DataAVBu = np.zeros((sensorsOfInterest,2))
        self.exp2DataAVBu = np.zeros((sensorsOfInterest,2))
        self.exp3DataAVBu = np.zeros((sensorsOfInterest,2))

        self.exp1DataAVBw = np.zeros((sensorsOfInterest,2))
        self.exp2DataAVBw = np.zeros((sensorsOfInterest,2))
        self.exp3DataAVBw = np.zeros((sensorsOfInterest,2))

        self.exp1DataCBu = np.zeros((sensorsOfInterest,2))
        self.exp2DataCBu = np.zeros((sensorsOfInterest,2))
        self.exp3DataCBu = np.zeros((sensorsOfInterest,2))

        self.exp1DataCBw = np.zeros((sensorsOfInterest,2))
        self.exp2DataCBw = np.zeros((sensorsOfInterest,2))
        self.exp3DataCBw = np.zeros((sensorsOfInterest,2))

        self.exp1DataARBu = np.zeros((sensorsOfInterest,2))
        self.exp2DataARBu = np.zeros((sensorsOfInterest,2))
        self.exp3DataARBu = np.zeros((sensorsOfInterest,2))
        
        self.exp1DataARBw = np.zeros((sensorsOfInterest,2))
        self.exp2DataARBw = np.zeros((sensorsOfInterest,2))
        self.exp3DataARBw = np.zeros((sensorsOfInterest,2))

        npos = 0

        for i in range(0,30):
            self.exp1DataAVBu[npos,:] = (sensorPosDef[i], self.Experiment1.diffFieldONAV[i] * 1E6)
            self.exp2DataAVBu[npos,:] = (sensorPosDef[i], self.Experiment2.diffFieldONAV[i] * 1E6)
            self.exp3DataAVBu[npos,:] = (sensorPosDef[i], self.Experiment3.diffFieldONAV[i] * 1E6)

            self.exp1DataAVBw[npos,:] = (sensorPosDef[i], self.Experiment1.diffFieldONAV[29 + i] * 1E6)
            self.exp2DataAVBw[npos,:] = (sensorPosDef[i], self.Experiment2.diffFieldONAV[29 + i] * 1E6)
            self.exp3DataAVBw[npos,:] = (sensorPosDef[i], self.Experiment3.diffFieldONAV[29 + i] * 1E6)

            self.exp1DataCBu[npos,:] = (sensorPosDef[i], self.Experiment1.diffFieldONC[i] * 1E6)
            self.exp2DataCBu[npos,:] = (sensorPosDef[i], self.Experiment2.diffFieldONC[i] * 1E6)
            self.exp3DataCBu[npos,:] = (sensorPosDef[i], self.Experiment3.diffFieldONC[i] * 1E6)

            self.exp1DataCBw[npos,:] = (sensorPosDef[i], self.Experiment1.diffFieldONC[29 + i] * 1E6)
            self.exp2DataCBw[npos,:] = (sensorPosDef[i], self.Experiment2.diffFieldONC[29 + i] * 1E6)
            self.exp3DataCBw[npos,:] = (sensorPosDef[i], self.Experiment3.diffFieldONC[29 + i] * 1E6)

            self.exp1DataARBu[npos,:] = (sensorPosDef[i], self.Experiment1.diffFieldONAR[i] * 1E6)
            self.exp2DataARBu[npos,:] = (sensorPosDef[i], self.Experiment2.diffFieldONAR[i] * 1E6)
            self.exp3DataARBu[npos,:] = (sensorPosDef[i], self.Experiment3.diffFieldONAR[i] * 1E6)

            self.exp1DataARBw[npos,:] = (sensorPosDef[i], self.Experiment1.diffFieldONAR[29 + i] * 1E6)
            self.exp2DataARBw[npos,:] = (sensorPosDef[i], self.Experiment2.diffFieldONAR[29 + i] * 1E6)
            self.exp3DataARBw[npos,:] = (sensorPosDef[i], self.Experiment3.diffFieldONAR[29 + i] * 1E6)

            npos = npos + 1

    # Polar plot for the evolution of the magnetic signature of a fault at 3 different measurements
    # 
    def plotPolarCompFieldsOfExperiments(self):  #plotNbLayer = 1 , plotU = True, plotV = bool, 
        ''' Polar Plot for each layer array position Bu above Bw and experiment together --> 3 x 2 plots with each two colors
        - interest is to determine outliers with a visual method
        - SensorsOfInterest:  np.linspace(2, 32, 30, dtype=int), dataSet = testExperiment.bFieldDataC, ringsStd = [0, 0.25,  0.5, 0.75], ringsData = [-100, -50, 0, 50, 100]
        titleInformationData = "With(/Without) noise"
        ''' 
        ringsData = [-100, -50, 0, 50, 100]
        ## plot sensor circle with errorbars:
        # Calculate standard deviation of each Sensor:
        

        # get angle position of each sensor around the FC-Stack
        theta = np.arange(0, 2 * np.pi, np.pi / 15)
        ###################################

        fig, ax1 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax1.errorbar(theta, self.exp1DataAVBu[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c= self.c3  )
        ax1.errorbar(theta, self.exp2DataAVBu[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c=self.c2)
        ax1.errorbar(theta, self.exp3DataAVBu[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c=self.c1)
        ax1.set_title("AV: $\Delta B_u$ measured on sensors "+ "\n" +self.Experiment1.FaultExperiment.name + " " + self.Experiment1.FaultExperiment.date + " ,\n" 
                      + self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date + " and \n" 
                      +self.Experiment3.FaultExperiment.name + " " + self.Experiment3.FaultExperiment.date)
        ax1.set_rticks(ringsData)
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompAVBu.pdf")

        fig, ax2 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax2.errorbar(theta, self.exp1DataAVBw[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c= self.c3  )
        ax2.errorbar(theta, self.exp2DataAVBw[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c=self.c2)
        ax2.errorbar(theta, self.exp3DataAVBw[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c=self.c1)
        ax2.set_title("AV: $\Delta B_w$ measured on sensors "+ "\n" +self.Experiment1.FaultExperiment.name + " " + self.Experiment1.FaultExperiment.date + " ,\n" 
                      + self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date + " and \n" 
                      +self.Experiment3.FaultExperiment.name + " " + self.Experiment3.FaultExperiment.date)
        ax2.set_rticks(ringsData)
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompAVBw.pdf")

        fig, ax3 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax3.errorbar(theta, self.exp1DataCBu[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c= self.c3  )
        ax3.errorbar(theta, self.exp2DataCBu[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c=self.c2)
        ax3.errorbar(theta, self.exp3DataCBu[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c=self.c1)
        ax3.set_title("Center: $\Delta B_u$ measured on sensors "+ "\n" +self.Experiment1.FaultExperiment.name + " " + self.Experiment1.FaultExperiment.date + " ,\n" 
                      + self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date + " and \n" 
                      +self.Experiment3.FaultExperiment.name + " " + self.Experiment3.FaultExperiment.date)
        
        ax3.set_rticks(ringsData)
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompCBu.pdf")

        fig, ax4 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax4.errorbar(theta, self.exp1DataCBw[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c= self.c3  )
        ax4.errorbar(theta, self.exp2DataCBw[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c=self.c2)
        ax4.errorbar(theta, self.exp3DataCBw[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c=self.c1)
        ax4.set_title("Center: $\Delta B_w$ measured on sensors "+ "\n"+self.Experiment1.FaultExperiment.name + " " + self.Experiment1.FaultExperiment.date + " ,\n" 
                      + self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date + " and \n" 
                      +self.Experiment3.FaultExperiment.name + " " + self.Experiment3.FaultExperiment.date)
        ax4.set_rticks(ringsData)
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompCBw.pdf")

        fig, ax5 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax5.errorbar(theta, self.exp1DataARBu[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c= self.c3  )
        ax5.errorbar(theta, self.exp2DataARBu[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c=self.c2)
        ax5.errorbar(theta, self.exp3DataARBu[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c=self.c1)
        ax5.set_title("AR: $\Delta B_u$ measured on sensors "+ "\n" +self.Experiment1.FaultExperiment.name + " " + self.Experiment1.FaultExperiment.date + " ,\n" 
                      + self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date + " and \n" 
                      +self.Experiment3.FaultExperiment.name + " " + self.Experiment3.FaultExperiment.date)
        ax5.set_rticks(ringsData)
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompARBu.pdf")

        fig, ax6 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax6.errorbar(theta, self.exp1DataARBw[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c= self.c3  )
        ax6.errorbar(theta, self.exp2DataARBw[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c=self.c2)
        ax6.errorbar(theta, self.exp3DataARBw[:,1], xerr=0, yerr=0, capsize=0.5,fmt=",", c=self.c1)
        ax6.set_title("AR: $\Delta B_w$ measured on sensors "+ "\n" +self.Experiment1.FaultExperiment.name + " " + self.Experiment1.FaultExperiment.date + " ,\n" 
                      + self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date + " and \n" 
                      +self.Experiment3.FaultExperiment.name + " " + self.Experiment3.FaultExperiment.date)
        ax6.set_rticks(ringsData)
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompARBw.pdf")

    def passSensorMeasurementsWithoutNoise(self):
        sensorsOfInterest = 30
        sensorPosDef = np.linspace(1,30,30,dtype=int)

        self.exp1DataAVBu = np.zeros((sensorsOfInterest,2))
        self.exp2DataAVBu = np.zeros((sensorsOfInterest,2))
        self.exp3DataAVBu = np.zeros((sensorsOfInterest,2))

        self.exp1DataAVBw = np.zeros((sensorsOfInterest,2))
        self.exp2DataAVBw = np.zeros((sensorsOfInterest,2))
        self.exp3DataAVBw = np.zeros((sensorsOfInterest,2))

        self.exp1DataCBu = np.zeros((sensorsOfInterest,2))
        self.exp2DataCBu = np.zeros((sensorsOfInterest,2))
        self.exp3DataCBu = np.zeros((sensorsOfInterest,2))

        self.exp1DataCBw = np.zeros((sensorsOfInterest,2))
        self.exp2DataCBw = np.zeros((sensorsOfInterest,2))
        self.exp3DataCBw = np.zeros((sensorsOfInterest,2))

        self.exp1DataARBu = np.zeros((sensorsOfInterest,2))
        self.exp2DataARBu = np.zeros((sensorsOfInterest,2))
        self.exp3DataARBu = np.zeros((sensorsOfInterest,2))
        
        self.exp1DataARBw = np.zeros((sensorsOfInterest,2))
        self.exp2DataARBw = np.zeros((sensorsOfInterest,2))
        self.exp3DataARBw = np.zeros((sensorsOfInterest,2))

        npos = 0

        for i in range(0,30):
            self.exp1DataAVBu[npos,:] = (sensorPosDef[i], self.Experiment1.diffBField[i] * 1E6)
            self.exp2DataAVBu[npos,:] = (sensorPosDef[i], self.Experiment2.diffBField[i] * 1E6)
            self.exp3DataAVBu[npos,:] = (sensorPosDef[i], self.Experiment3.diffBField[i] * 1E6)

            self.exp1DataAVBw[npos,:] = (sensorPosDef[i], self.Experiment1.diffBField[29 + i] * 1E6)
            self.exp2DataAVBw[npos,:] = (sensorPosDef[i], self.Experiment2.diffBField[29 + i] * 1E6)
            self.exp3DataAVBw[npos,:] = (sensorPosDef[i], self.Experiment3.diffBField[29 + i] * 1E6)

            self.exp1DataCBu[npos,:] = (sensorPosDef[i], self.Experiment1.diffBField[29 + 30 + i] * 1E6)
            self.exp2DataCBu[npos,:] = (sensorPosDef[i], self.Experiment2.diffBField[29 + 30 + i] * 1E6)
            self.exp3DataCBu[npos,:] = (sensorPosDef[i], self.Experiment3.diffBField[29 + 30 + i] * 1E6)

            self.exp1DataCBw[npos,:] = (sensorPosDef[i], self.Experiment1.diffBField[29 + 60 + i] * 1E6)
            self.exp2DataCBw[npos,:] = (sensorPosDef[i], self.Experiment2.diffBField[29 + 60 + i] * 1E6)
            self.exp3DataCBw[npos,:] = (sensorPosDef[i], self.Experiment3.diffBField[29 + 60 + i] * 1E6)

            self.exp1DataARBu[npos,:] = (sensorPosDef[i], self.Experiment1.diffBField[29 + 90 + i] * 1E6)
            self.exp2DataARBu[npos,:] = (sensorPosDef[i], self.Experiment2.diffBField[29 + 90 + i] * 1E6)
            self.exp3DataARBu[npos,:] = (sensorPosDef[i], self.Experiment3.diffBField[29 + 90 + i] * 1E6)

            self.exp1DataARBw[npos,:] = (sensorPosDef[i], self.Experiment1.diffBField[29 + 120 + i] * 1E6)
            self.exp2DataARBw[npos,:] = (sensorPosDef[i], self.Experiment2.diffBField[29 + 120 + i] * 1E6)
            self.exp3DataARBw[npos,:] = (sensorPosDef[i], self.Experiment3.diffBField[29 + 120 + i] * 1E6)

            npos = npos + 1
    @deprecated("This Function uses the calculation of the difference between two absolute fields. Use plotCompFieldsOfExperimentsWithoutNoise instead")
    def plotCompFieldsOfExperimentsDirect(self):  #plotNbLayer = 1 , plotU = True, plotV = bool, 
        ''' Plot for each layer array position Bu above Bw and experiment together --> 3 x 2 plots with each two colors
        - interest is to determine outliers with a visual method
        - SensorsOfInterest:  np.linspace(2, 32, 30, dtype=int), dataSet = testExperiment.bFieldDataC, ringsStd = [0, 0.25,  0.5, 0.75], ringsData = [-100, -50, 0, 50, 100]
        titleInformationData = "With(/Without) noise"
        ''' 

        ###################################


        fig, axs = plt.subplots(2, 3, figsize=set_size(), sharex=True)

        axs[0,0].plot(self.exp1DataAVBu[:,0], self.exp1DataAVBu[:,1], c =  self.c3  )
        axs[0,0].plot(self.exp1DataAVBu[:,0], self.exp2DataAVBu[:,1], c = self.c2)
        axs[0,0].plot(self.exp1DataAVBu[:,0], self.exp3DataAVBu[:,1], c = self.c1)
        axs[0,0].set_title("AV: $\Delta B_u$")

        axs[1,0].plot(self.exp1DataAVBu[:,0], self.exp1DataAVBw[:,1], c =  self.c3  )
        axs[1,0].plot(self.exp1DataAVBu[:,0], self.exp2DataAVBw[:,1], c = self.c2)
        axs[1,0].plot(self.exp1DataAVBu[:,0], self.exp3DataAVBw[:,1], c = self.c1)
        axs[1,0].set_title("AV: $\Delta B_w$")

        axs[0,1].plot(self.exp1DataAVBu[:,0], self.exp1DataCBu[:,1],c = self.c3  )
        axs[0,1].plot(self.exp1DataAVBu[:,0], self.exp2DataCBu[:,1], c = self.c2)
        axs[0,1].plot(self.exp1DataAVBu[:,0], self.exp3DataCBu[:,1], c = self.c1)
        axs[0,1].set_title("Center: $\Delta B_u$")
        
        axs[1,1].plot(self.exp1DataAVBu[:,0], self.exp1DataCBw[:,1], c =  self.c3  )
        axs[1,1].plot(self.exp1DataAVBu[:,0], self.exp2DataCBw[:,1], c = self.c2)
        axs[1,1].plot(self.exp1DataAVBu[:,0], self.exp3DataCBw[:,1], c = self.c1)
        axs[1,1].set_title("Center: $\Delta B_w$")

        axs[0,2].plot(self.exp1DataAVBu[:,0], self.exp1DataARBu[:,1], c =  self.c3  )
        axs[0,2].plot(self.exp1DataAVBu[:,0], self.exp2DataARBu[:,1], c = self.c2)
        axs[0,2].plot(self.exp1DataAVBu[:,0], self.exp3DataARBu[:,1], c = self.c1)
        axs[0,2].set_title("AR: $\Delta B_u$")

        axs[1,2].plot(self.exp1DataAVBu[:,0], self.exp1DataARBw[:,1], marker='x', c =  self.c3  )
        axs[1,2].plot(self.exp1DataAVBu[:,0], self.exp2DataARBw[:,1], marker='x', c = self.c2)
        axs[1,2].plot(self.exp1DataAVBu[:,0], self.exp3DataARBw[:,1], marker='x', c = self.c1)
        axs[1,2].set_title("AR: $\Delta B_w$")
        axs[1,2].set_xticks([0,5,10,15,20,25,30])
        axs[1,2].set_xlim([0,30])
        # axs[1,2].set_ylim([-3,3])

        labels = [self.Experiment1.FaultExperiment.name, self.Experiment2.FaultExperiment.name, self.Experiment3.FaultExperiment.name]

        fig.legend(labels=labels, 
           loc="upper right") 
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationCompAllDirect.pdf")       

    def plotCompFieldsOfExperimentsWithoutNoise(self):  #plotNbLayer = 1 , plotU = True, plotV = bool, 
        ''' Plot for each layer array position Bu above Bw and experiment together --> 3 x 2 plots with each two colors
        - interest is to determine outliers with a visual method
        - SensorsOfInterest:  np.linspace(2, 32, 30, dtype=int), dataSet = testExperiment.bFieldDataC, ringsStd = [0, 0.25,  0.5, 0.75], ringsData = [-100, -50, 0, 50, 100]
        titleInformationData = "With(/Without) noise"
        ''' 

        ###################################


        fig, axs = plt.subplots(2, 3, figsize=set_size(), sharex=True)

        # fig, ax1 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        axs[0,0].plot(self.exp1DataAVBu[:,0], self.exp1DataAVBu[:,1], c =  self.c3  )
        axs[0,0].plot(self.exp1DataAVBu[:,0], self.exp2DataAVBu[:,1], c = self.c2)
        axs[0,0].plot(self.exp1DataAVBu[:,0], self.exp3DataAVBu[:,1], c = self.c1)
        axs[0,0].set_title("AV: $\Delta B_u$")
        axs[0,0].set_ylim([-15, 15])
        # axs[0,0].set_rticks(ringsData)
        # fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompAVBu.pdf")

        # fig, ax2 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        axs[1,0].plot(self.exp1DataAVBu[:,0], self.exp1DataAVBw[:,1], c =  self.c3  )
        axs[1,0].plot(self.exp1DataAVBu[:,0], self.exp2DataAVBw[:,1], c = self.c2)
        axs[1,0].plot(self.exp1DataAVBu[:,0], self.exp3DataAVBw[:,1], c = self.c1)
        axs[1,0].set_title("AV: $\Delta B_w$")
        axs[1,0].set_ylim([-10, 10])
        # axs[1,0].set_rticks(ringsData)
        # fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompAVBw.pdf")

        # fig, ax3 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        axs[0,1].plot(self.exp1DataAVBu[:,0], self.exp1DataCBu[:,1],c = self.c3  )
        axs[0,1].plot(self.exp1DataAVBu[:,0], self.exp2DataCBu[:,1], c = self.c2)
        axs[0,1].plot(self.exp1DataAVBu[:,0], self.exp3DataCBu[:,1], c = self.c1)
        axs[0,1].set_title("Center: $\Delta B_u$")
        axs[0,1].set_ylim([-15, 15])
        
        # axs[0,1].set_rticks(ringsData)
        # fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompCBu.pdf")

        # fig, axs[1,1] = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        axs[1,1].plot(self.exp1DataAVBu[:,0], self.exp1DataCBw[:,1], c =  self.c3  )
        axs[1,1].plot(self.exp1DataAVBu[:,0], self.exp2DataCBw[:,1], c = self.c2)
        axs[1,1].plot(self.exp1DataAVBu[:,0], self.exp3DataCBw[:,1], c = self.c1)
        axs[1,1].set_title("Center: $\Delta B_w$")
        axs[1,1].set_ylim([-10, 10])
        # axs[1,1].set_rticks(ringsData)
        # fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompCBw.pdf")

        # fig, axs[0,2] = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        axs[0,2].plot(self.exp1DataAVBu[:,0], self.exp1DataARBu[:,1], c =  self.c3  )
        axs[0,2].plot(self.exp1DataAVBu[:,0], self.exp2DataARBu[:,1], c = self.c2)
        axs[0,2].plot(self.exp1DataAVBu[:,0], self.exp3DataARBu[:,1], c = self.c1)
        axs[0,2].set_title("AR: $\Delta B_u$")
        axs[0,2].set_ylim([-15, 15])

        # measured on sensors "+ "\n" +self.Experiment1.FaultExperiment.name + " " + self.Experiment1.FaultExperiment.date + " ,\n" 
                    # + self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date + " and \n" 
                    # +self.Experiment3.FaultExperiment.name + " " + self.Experiment3.FaultExperiment.date
        # axs[0,2].set_rticks(ringsData)
        # fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompARBu.pdf")

        # fig, axs[1,2] = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        axs[1,2].plot(self.exp1DataAVBu[:,0], self.exp1DataARBw[:,1], c =  self.c3  )
        axs[1,2].plot(self.exp1DataAVBu[:,0], self.exp2DataARBw[:,1], c = self.c2)
        axs[1,2].plot(self.exp1DataAVBu[:,0], self.exp3DataARBw[:,1], c = self.c1)
        axs[1,2].set_title("AR: $\Delta B_w$")
        axs[1,2].set_xticks([0,5,10,15,20,25,30])
        axs[1,2].set_xlim([0, 30])
        axs[1,2].set_ylim([-10, 10])

        labels = [self.Experiment1.FaultExperiment.name, self.Experiment2.FaultExperiment.name, self.Experiment3.FaultExperiment.name]

        fig.legend(labels=labels, 
           loc="upper right") 
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationCompAllWithoutNoise.pdf")


    def __init__(self, Experiment1: Investigation, Experiment2: Investigation, Experiment3: Investigation):
        self.c1 = "seagreen"
        self.c2 = "orange"
        self.c3 = "blue"
        self.Experiment1 = Experiment1
        self.Experiment2 = Experiment2
        self.Experiment3 = Experiment3
        self.passSensorMeasurementsWithoutNoise()
        self.plotCompFieldsOfExperimentsWithoutNoise()
        

# for testing:
experiment1DataClass = RefExperiment20170207
experiment1Def = Exp(experiment1DataClass.measurementYear, experiment1DataClass.measurementName, experiment1DataClass.measurementDate, experiment1DataClass.measuredCurrent, experiment1DataClass.scaleCurrentTo,
                                          experiment1DataClass.noiseBFieldPath, experiment1DataClass.fileNameNoiseAV, experiment1DataClass.fileNameNoiseCenter, experiment1DataClass.fileNameNoiseAR, 
                                          experiment1DataClass.bFieldPath, experiment1DataClass.fileNameAV, experiment1DataClass.fileNameC, experiment1DataClass.fileNameAR)
experiment2DataClass = Stoichio13Experiment20170209
experiment2Def = Exp(experiment2DataClass.measurementYear, experiment2DataClass.measurementName, experiment2DataClass.measurementDate, experiment2DataClass.measuredCurrent, experiment2DataClass.scaleCurrentTo,
                                          experiment2DataClass.noiseBFieldPath, experiment2DataClass.fileNameNoiseAV, experiment2DataClass.fileNameNoiseCenter, experiment2DataClass.fileNameNoiseAR, 
                                          experiment2DataClass.bFieldPath, experiment2DataClass.fileNameAV, experiment2DataClass.fileNameC, experiment2DataClass.fileNameAR)

experiment3DataClass = Stoichio15Experiment20170209
experiment3Def = Exp(experiment3DataClass.measurementYear, experiment3DataClass.measurementName, experiment3DataClass.measurementDate, experiment3DataClass.measuredCurrent, experiment3DataClass.scaleCurrentTo,
                                          experiment3DataClass.noiseBFieldPath, experiment3DataClass.fileNameNoiseAV, experiment3DataClass.fileNameNoiseCenter, experiment3DataClass.fileNameNoiseAR, 
                                          experiment3DataClass.bFieldPath, experiment3DataClass.fileNameAV, experiment3DataClass.fileNameC, experiment3DataClass.fileNameAR)

experiment4DataClass = Stoichio20Experiment20170209
experiment4Def = Exp(experiment4DataClass.measurementYear, experiment4DataClass.measurementName, experiment4DataClass.measurementDate, experiment4DataClass.measuredCurrent, experiment4DataClass.scaleCurrentTo,
                                          experiment4DataClass.noiseBFieldPath, experiment4DataClass.fileNameNoiseAV, experiment4DataClass.fileNameNoiseCenter, experiment4DataClass.fileNameNoiseAR, 
                                          experiment4DataClass.bFieldPath, experiment4DataClass.fileNameAV, experiment4DataClass.fileNameC, experiment4DataClass.fileNameAR)

sensorsOfInterest = np.linspace(0, 30, 30, dtype=int)
InvStoichio13 = Investigation(True, experiment1Def, experiment2Def, sensorsOfInterest)
InvStoichio15 = Investigation(True, experiment1Def, experiment3Def, sensorsOfInterest)
InvStoichio20 = Investigation(True, experiment1Def, experiment4Def, sensorsOfInterest)

investigationOf3DifferentProblems = MultiInvestigation(InvStoichio13, InvStoichio15, InvStoichio20)
# investigationOf3DifferentProblems.plotCompFieldsOfExperiments()