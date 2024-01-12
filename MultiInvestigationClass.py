from dataclasses import asdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from collectAllMeasureDataInOneFile import*
from ExperimentClass import Experiment as Exp
from thesis_general_imports import*
from InvestigationClass import*

class MultiInvestigation:
    """"Currently the present class is used to compare 3 (three) different results as used in Lyes et al. Thesis."""
    def passSensorMeasurements(self):
        sensorsOfInterest = 30

        self.exp1DataAVBu = np.zeros(sensorsOfInterest)
        self.exp2DataAVBu = np.zeros(sensorsOfInterest)
        self.exp3DataAVBu = np.zeros(sensorsOfInterest)

        self.exp1DataAVBw = np.zeros(sensorsOfInterest)
        self.exp2DataAVBw = np.zeros(sensorsOfInterest)
        self.exp3DataAVBw = np.zeros(sensorsOfInterest)

        self.exp1DataCBu = np.zeros(sensorsOfInterest)
        self.exp2DataCBu = np.zeros(sensorsOfInterest)
        self.exp3DataCBu = np.zeros(sensorsOfInterest)

        self.exp1DataCBw = np.zeros(sensorsOfInterest)
        self.exp2DataCBw = np.zeros(sensorsOfInterest)
        self.exp3DataCBw = np.zeros(sensorsOfInterest)

        self.exp1DataARBu = np.zeros(sensorsOfInterest)
        self.exp2DataARBu = np.zeros(sensorsOfInterest)
        self.exp3DataARBu = np.zeros(sensorsOfInterest)
        
        self.exp1DataARBw = np.zeros(sensorsOfInterest)
        self.exp2DataARBw = np.zeros(sensorsOfInterest)
        self.exp3DataARBw = np.zeros(sensorsOfInterest)

        npos = 0

        for i in range(0,30):
            self.exp1DataAVBu[npos] = self.Experiment1.diffFieldONAV[i] * 1E6
            self.exp2DataAVBu[npos] = self.Experiment2.diffFieldONAV[i] * 1E6
            self.exp3DataAVBu[npos] = self.Experiment3.diffFieldONAV[i] * 1E6

            self.exp1DataAVBw[npos] = self.Experiment1.diffFieldONAV[29 + i] * 1E6
            self.exp2DataAVBw[npos] = self.Experiment2.diffFieldONAV[29 + i] * 1E6
            self.exp3DataAVBw[npos] = self.Experiment3.diffFieldONAV[29 + i] * 1E6

            self.exp1DataCBu[npos] = self.Experiment1.diffFieldONC[i] * 1E6
            self.exp2DataCBu[npos] = self.Experiment2.diffFieldONC[i] * 1E6
            self.exp3DataCBu[npos] = self.Experiment3.diffFieldONC[i] * 1E6

            self.exp1DataCBw[npos] = self.Experiment1.diffFieldONC[29 + i] * 1E6
            self.exp2DataCBw[npos] = self.Experiment2.diffFieldONC[29 + i] * 1E6
            self.exp3DataCBw[npos] = self.Experiment3.diffFieldONC[29 + i] * 1E6

            self.exp1DataARBu[npos] = self.Experiment1.diffFieldONAR[i] * 1E6
            self.exp2DataARBu[npos] = self.Experiment2.diffFieldONAR[i] * 1E6
            self.exp3DataARBu[npos] = self.Experiment3.diffFieldONAR[i] * 1E6

            self.exp1DataARBw[npos] = self.Experiment1.diffFieldONAR[29 + i] * 1E6
            self.exp2DataARBw[npos] = self.Experiment2.diffFieldONAR[29 + i] * 1E6
            self.exp3DataARBw[npos] = self.Experiment3.diffFieldONAR[29 + i] * 1E6

            npos = npos + 1

    # Polar plot for the evolution of the magnetic signature of a fault at 3 different measurements
    # 
     
    def plotPolarCompFieldsOfExperiments(self):  #plotNbLayer = 1 , plotU = True, plotV = bool, 
        ''' Plot for each layer array position Bu above Bw and experiment together --> 3 x 2 plots with each two colors
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
        ## CHANGE HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        ## plot Standard Deviation on sensors
        fig, ax1 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax1.errorbar(theta, self.exp1DataAVBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax1.errorbar(theta, self.exp2DataAVBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="orange")
        ax1.errorbar(theta, self.exp3DataAVBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="blue")
        ax1.set_title("AV: $\Delta B_u$ measured on sensors "+ "\n" +self.Experiment1.FaultExperiment.name + " " + self.Experiment1.FaultExperiment.date + " ,\n" 
                      + self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date + " and \n" 
                      +self.Experiment3.FaultExperiment.name + " " + self.Experiment3.FaultExperiment.date)
        ax1.set_rticks(ringsData)
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompAVBu.pdf")

        ## plot Values on sensors
        fig, ax2 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax2.errorbar(theta, self.exp1DataAVBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax2.errorbar(theta, self.exp2DataAVBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="orange")
        ax2.errorbar(theta, self.exp3DataAVBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="blue")
        ax2.set_title("AV: $\Delta B_w$ measured on sensors "+ "\n" +self.Experiment1.FaultExperiment.name + " " + self.Experiment1.FaultExperiment.date + " ,\n" 
                      + self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date + " and \n" 
                      +self.Experiment3.FaultExperiment.name + " " + self.Experiment3.FaultExperiment.date)
        ax2.set_rticks(ringsData)
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompAVBw.pdf")

        fig, ax3 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax3.errorbar(theta, self.exp1DataCBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax3.errorbar(theta, self.exp2DataCBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="orange")
        ax3.errorbar(theta, self.exp3DataCBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="blue")
        ax3.set_title("Center: $\Delta B_u$ measured on sensors "+ "\n" +self.Experiment1.FaultExperiment.name + " " + self.Experiment1.FaultExperiment.date + " ,\n" 
                      + self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date + " and \n" 
                      +self.Experiment3.FaultExperiment.name + " " + self.Experiment3.FaultExperiment.date)
        
        ax3.set_rticks(ringsData)
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompCBu.pdf")

        ## plot Values on sensors
        fig, ax4 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax4.errorbar(theta, self.exp1DataCBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax4.errorbar(theta, self.exp2DataCBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="orange")
        ax4.errorbar(theta, self.exp3DataCBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="blue")
        ax4.set_title("Center: $\Delta B_w$ measured on sensors "+ "\n"+self.Experiment1.FaultExperiment.name + " " + self.Experiment1.FaultExperiment.date + " ,\n" 
                      + self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date + " and \n" 
                      +self.Experiment3.FaultExperiment.name + " " + self.Experiment3.FaultExperiment.date)
        ax4.set_rticks(ringsData)
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompCBw.pdf")

        fig, ax5 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax5.errorbar(theta, self.exp1DataARBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax5.errorbar(theta, self.exp2DataARBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="orange")
        ax5.errorbar(theta, self.exp3DataARBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="blue")
        ax5.set_title("AR: $\Delta B_u$ measured on sensors "+ "\n" +self.Experiment1.FaultExperiment.name + " " + self.Experiment1.FaultExperiment.date + " ,\n" 
                      + self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date + " and \n" 
                      +self.Experiment3.FaultExperiment.name + " " + self.Experiment3.FaultExperiment.date)
        ax5.set_rticks(ringsData)
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompARBu.pdf")

        ## plot Values on sensors
        fig, ax6 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax6.errorbar(theta, self.exp1DataARBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax6.errorbar(theta, self.exp2DataARBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="orange")
        ax6.errorbar(theta, self.exp3DataARBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="blue")
        ax6.set_title("AR: $\Delta B_w$ measured on sensors "+ "\n" +self.Experiment1.FaultExperiment.name + " " + self.Experiment1.FaultExperiment.date + " ,\n" 
                      + self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date + " and \n" 
                      +self.Experiment3.FaultExperiment.name + " " + self.Experiment3.FaultExperiment.date)
        ax6.set_rticks(ringsData)
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompARBw.pdf")

    def __init__(self, Experiment1: Investigation, Experiment2: Investigation, Experiment3: Investigation):
        self.Experiment1 = Experiment1
        self.Experiment2 = Experiment2
        self.Experiment3 = Experiment3
        self.passSensorMeasurements()
        
        # self.sensorArray = sensorList
        # self.sensorsOfInterestArray = np.zeros((len(sensorList),7))
        # self.sensoMatrix = self.readSensorMatrix()
        # self.savepath = FaultExperiment.bFieldPath
        # self.currentDirectionIsTheSame = currentDirectionIsTheSame
        # if self.currentDirectionIsTheSame == True: self.CurrentInversionFactor = 1
        # else: self.currentDirectionIsTheSame = -1
        # self.diffBField = np.subtract(FaultExperiment.scaledField,RefExperiment.scaledField)
        # self.sensorsOfInterestArray = self.creatSensorMapping()
        # self.plotHealthyAndFaultyField()
        # plot of diff Field with noise subtraction during experiment data treatment
        # self.plotDiffField()
        # self.plotInvestiagtedField()
        # plot of diff Field without noise subtraction