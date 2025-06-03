import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plotErrorPlotsForOneSensorLayer(self, sensorsOfInterest, titleInformationData, ringsStd = list, ringsData = list, dataSet = pd.DataFrame):  #plotNbLayer = 1 , plotU = True, plotV = bool, 
        '''SensorsOfInterest:  np.linspace(2, 32, 30, dtype=int), dataSet = testExperiment.bFieldDataC, ringsStd = [0, 0.25,  0.5, 0.75], ringsData = [-100, -50, 0, 50, 100]
        titleInformationData = "With(/Without) noise"
        ''' 
        ## plot sensor circle with errorbars:
        # Calculate standard deviation of each Sensor:
        r2020 = np.zeros(len(sensorsOfInterest))
        yErr2020 = np.zeros(len(sensorsOfInterest))
        npos = 0
        for i in sensorsOfInterest:
            r2020[npos] = dataSet.iloc[:,i].mean()*self.arrayPlotFactor
            yErr2020[npos] = dataSet.iloc[:,i].std(ddof=1)*self.arrayPlotFactor
            npos = npos + 1

        # get angle position of each sensor around the FC-Stack
        theta = np.arange(0, 2 * np.pi, np.pi / 15)
        

        ## plot Standard Deviation on sensors
        fig, ax1 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax1.errorbar(theta, yErr2020, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax1.set_title(titleInformationData + " Standard Deviation on sensor measurements "+ "\n" +self.name + " " + self.date)
        ax1.set_rticks(ringsStd)
        fig.savefig(self.bFieldPath + self.name + "_EXP_Std_Polar.pdf")
        # print(self.bFieldPath + self.name + "_EXP_Std_Polar.pdf")

        ## plot Values on sensors
        fig, ax2 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
        ax2.errorbar(theta, r2020, xerr=0, yerr=0, capsize=0.5,fmt=",", c="seagreen")
        ax2.set_title(titleInformationData + " Measurement around the Fuel Cell"+ "\n" +self.name + " " + self.date)
        ax2.set_rticks(ringsData)
        fig.savefig(self.bFieldPath + self.name + "_EXP_Measurement_Polar.pdf")

def plotFieldMeasurementDataAndSavePlots(self):
# plot B-Field respecting factors depending on the investigated year and save clean field mean values as txt
# depending on the year, different factors need to be applied
    if self.year == 2020:
        ylimBFieldUp = 250
        ylimBFieldDown = -250
    elif self.year == 2021:
        ylimBFieldUp = 100
        ylimBFieldDown = -100
    elif self.year == 2017:
        ylimBFieldUp = 200
        ylimBFieldDown = -200

    f1 = plt.subplots(1, 1, figsize=set_size(), sharey=True)
    plt.plot(np.multiply(self.measuredMeanNoiseField, self.arrayPlotFactor), ":" , label = "Noise mean value in $\mu$T", color = specific_colors['G2E_black'])
    plt.plot(np.multiply(self.measuredMeanFieldWithNoise, self.arrayPlotFactor), ':' , label = "B-Field with noise in $\mu$T", color = specific_colors['RawField'])
    plt.plot(np.multiply(self.measuredCleanField, self.arrayPlotFactor),   label = "Clean B-Field in $\mu$T", color = specific_colors['MPM_lightblue'])
    ## set red lines for each 30 sensors
    ymin = -180
    ymax = 150  
    plt.vlines(30,ymin, ymax,'r')
    plt.vlines(60,ymin, ymax,'r')
    plt.vlines(90,ymin, ymax,'r')
    plt.vlines(120,ymin, ymax,'r')
    plt.vlines(150,ymin, ymax,'r')
    plt.xlabel("Sensor number")
    plt.ylabel("Field Strength ($\mu$T)")
    plt.ylim(ylimBFieldDown, ylimBFieldUp)
    plt.xlim(0,len(self.measuredCleanField)-1)
    plt.legend()


    plt.savefig(self.bFieldPath + self.name[0: -11]+"_B_Field_CleanMeasured.pdf")
    self.measuredField = np.multiply(self.measuredCleanField, self.arrayDataFactor)
    # # write values to csv
    # print("Exported DataFrame to: " + self.bFieldPath + self.name[0: -11]+"_B_Field_CleanMeasured.dat")
    np.savetxt(self.bFieldPath + self.name[0: -11] + "_B_Field_CleanMeasured.dat", 
            self.measuredField,
            delimiter =", ", 
            fmt ='% s')