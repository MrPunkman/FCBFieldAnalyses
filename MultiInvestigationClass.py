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
        sensorsOfInterest = 30

        exp1DataAVBu = np.zeros(sensorsOfInterest)
        exp2DataAVBu = np.zeros(sensorsOfInterest)
        exp3DataAVBu = np.zeros(sensorsOfInterest)

        exp1DataAVBw = np.zeros(sensorsOfInterest)
        exp2DataAVBw = np.zeros(sensorsOfInterest)
        exp3DataAVBw = np.zeros(sensorsOfInterest)

        exp1DataCBu = np.zeros(sensorsOfInterest)
        exp2DataCBu = np.zeros(sensorsOfInterest)
        exp3DataCBu = np.zeros(sensorsOfInterest)

        exp1DataCBw = np.zeros(sensorsOfInterest)
        exp2DataCBw = np.zeros(sensorsOfInterest)
        exp3DataCBw = np.zeros(sensorsOfInterest)

        exp1DataARBu = np.zeros(sensorsOfInterest)
        exp2DataARBu = np.zeros(sensorsOfInterest)
        exp3DataARBu = np.zeros(sensorsOfInterest)
        
        exp1DataARBw = np.zeros(sensorsOfInterest)
        exp2DataARBw = np.zeros(sensorsOfInterest)
        exp3DataARBw = np.zeros(sensorsOfInterest)

        npos = 0

        for i in range(0,30):
            exp1DataAVBu[npos] = self.Experiment1.diffFieldONAV[i] * 1E6
            exp2DataAVBu[npos] = self.Experiment2.diffFieldONAV[i] * 1E6
            exp3DataAVBu[npos] = self.Experiment3.diffFieldONAV[i] * 1E6

            exp1DataAVBw[npos] = self.Experiment1.diffFieldONAV[29 + i] * 1E6
            exp2DataAVBw[npos] = self.Experiment2.diffFieldONAV[29 + i] * 1E6
            exp3DataAVBw[npos] = self.Experiment3.diffFieldONAV[29 + i] * 1E6

            exp1DataCBu[npos] = self.Experiment1.diffFieldONC[i] * 1E6
            exp2DataCBu[npos] = self.Experiment2.diffFieldONC[i] * 1E6
            exp3DataCBu[npos] = self.Experiment3.diffFieldONC[i] * 1E6

            exp1DataCBw[npos] = self.Experiment1.diffFieldONC[29 + i] * 1E6
            exp2DataCBw[npos] = self.Experiment2.diffFieldONC[29 + i] * 1E6
            exp3DataCBw[npos] = self.Experiment3.diffFieldONC[29 + i] * 1E6

            exp1DataARBu[npos] = self.Experiment1.diffFieldONAR[i] * 1E6
            exp2DataARBu[npos] = self.Experiment2.diffFieldONAR[i] * 1E6
            exp3DataARBu[npos] = self.Experiment3.diffFieldONAR[i] * 1E6

            exp1DataARBw[npos] = self.Experiment1.diffFieldONAR[29 + i] * 1E6
            exp2DataARBw[npos] = self.Experiment2.diffFieldONAR[29 + i] * 1E6
            exp3DataARBw[npos] = self.Experiment2.diffFieldONAR[29 + i] * 1E6

            npos = npos + 1

        # get angle position of each sensor around the FC-Stack
        theta = np.arange(0, 2 * np.pi, np.pi / 15)
        ###################################
        ## CHANGE HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        ## plot Standard Deviation on sensors
        fig, ax1 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax1.errorbar(theta, exp1DataAVBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax1.errorbar(theta, exp2DataAVBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="orange")
        ax1.errorbar(theta, exp3DataAVBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="blue")
        ax1.set_title("AV: $B_u$ measured on sensors "+ "\n" +self.Experiment1.FaultExperiment.name + " " + self.Experiment1.FaultExperiment.date + " ,\n" 
                      + self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date + " and \n" 
                      +self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date)
        ax1.set_rticks(ringsData)
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompAVBu.pdf")

        ## plot Values on sensors
        fig, ax2 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax2.errorbar(theta, exp1DataAVBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax2.errorbar(theta, exp2DataAVBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="orange")
        ax2.errorbar(theta, exp3DataAVBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="blue")
        ax2.set_title("AV: $B_w$ measured on sensors "+ "\n" +self.Experiment1.FaultExperiment.name + " " + self.Experiment1.FaultExperiment.date + " ,\n" 
                      + self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date + " and \n" 
                      +self.Experiment2.FaultExperiment.name + " " + self.Experiment2.FaultExperiment.date)
        ax2.set_rticks(ringsData)
        fig.savefig(self.Experiment1.FaultExperiment.bFieldPath + "MulInvestigationPolarCompAVBw.pdf")

        # fig, ax3 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        # ax3.errorbar(theta, exp1DataCBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        # ax3.errorbar(theta, exp2DataCBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="red")
        # ax3.set_title("Center: $B_u$ measured on sensors "+ "\n" +self.RefExperiment.name + " " + self.RefExperiment.date + " and \n" + self.FaultExperiment.name + " " + self.FaultExperiment.date)## CHANGE HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # ax3.set_rticks(ringsData)
        # fig.savefig(self.FaultExperiment.bFieldPath + "InvestigationPolarCompCBu.pdf")

        # ## plot Values on sensors
        # fig, ax4 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        # ax4.errorbar(theta, exp1DataCBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        # ax4.errorbar(theta, exp2DataCBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="red")
        # ax4.set_title("Center: $B_w$ measured on sensors "+ "\n" +self.RefExperiment.name + " " + self.RefExperiment.date + " and \n" + self.FaultExperiment.name + " " + self.FaultExperiment.date)## CHANGE HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # ax4.set_rticks(ringsData)
        # fig.savefig(self.FaultExperiment.bFieldPath + "InvestigationPolarCompCBw.pdf")

        # fig, ax3 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        # ax3.errorbar(theta, exp1DataARBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        # ax3.errorbar(theta, exp2DataARBu, xerr=0, yerr=0, capsize=0.5,fmt=",", c="red")
        # ax3.set_title("AR: $B_u$ measured on sensors "+ "\n" +self.RefExperiment.name + " " + self.RefExperiment.date + " and \n" + self.FaultExperiment.name + " " + self.FaultExperiment.date)
        # ax3.set_rticks(ringsData)
        # fig.savefig(self.FaultExperiment.bFieldPath + "InvestigationPolarCompARBu.pdf")

        # ## plot Values on sensors
        # fig, ax4 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        # ax4.errorbar(theta, exp1DataARBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        # ax4.errorbar(theta, exp2DataARBw, xerr=0, yerr=0, capsize=0.5,fmt=",", c="red")
        # ax4.set_title("AR: $B_w$ measured on sensors "+ "\n" +self.RefExperiment.name + " " + self.RefExperiment.date + " and \n" + self.FaultExperiment.name + " " + self.FaultExperiment.date)
        # ax4.set_rticks(ringsData)
        # fig.savefig(self.FaultExperiment.bFieldPath + "InvestigationPolarCompARBw.pdf")

    def __init__(self, Experiment1: Investigation, Experiment2: Investigation, Experiment3: Investigation):
        self.Experiment1 = Experiment1
        self.Experiment2 = Experiment2
        self.Experiment3 = Experiment3
        
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