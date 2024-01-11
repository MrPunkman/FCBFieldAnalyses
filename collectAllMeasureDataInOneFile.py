'''This module is created by Leonard Freisem and is used to create diff B-Field for an investigated case.'''
from ctypes import sizeof
from tracemalloc import stop
from turtle import color
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from thesis_general_imports import*
from ExperimentClass import*
from InvestigationClass import*
# import seaborn as sns

# import csv and change ',' to '.' . Change df to float df 
def createDF(bFieldPath, filename):
    ## import file and set file path -- lyes data-->>>> [i for i in range(0, 22) ]; 2020/21 data-->>>> [i for i in range(0, 23) ]
    df = pd.read_csv(bFieldPath+filename, sep="	",skiprows = [i for i in range(0, 22) ])

    ## change , to . for later calculations. Otherwise, the cell is declared as string and no calculation can be done
    df = df.replace(',','.',regex=True)

    # change type to float
    df = df.astype(float)
    
    return df


# create mean values of the raw data and save in array
def getMeanValueOfDFColumnInVolt(df):                           # this function returns a mean value of the raw data per column of the DataFrame
    # create list with mean value of every sensor column
    meanData = []
    columnMean = []

    for i in range(1,68):
        columnMean = df.iloc[1:,i]
        meanData.append(mean(columnMean))

    # get V values in a list
    vValuesMeanData = meanData[0:len(meanData):1] 
    return vValuesMeanData

# returns B-Field meanvalues as np.array
def getMeanValueBFieldOfDFInVolt(df):                               # returns B-field meanvalues in V as np.array
    meanValuesForEachCol = getMeanValueOfDFColumnInVolt(df)
    # get V values for B-field in a list
    vValuesBFieldData = meanValuesForEachCol[1:61:1]                # selects the meanvalues for the B-Field in the array
    return np.asarray(vValuesBFieldData)

def getMeanValueCurrentAndTensions(df):                               # returns B-field meanvalues in V as np.array
    meanValuesForEachCol = df.iloc[1,1]
    meanValuesCurrent = mean(meanValuesForEachCol)
    # get V values for B-field in a list
    vValuesBFieldData = meanValuesForEachCol[1:61:1]                # selects the meanvalues for the B-Field in the array
    return np.asarray(vValuesBFieldData)

# return measurements as matrix array
def returnAllColumnsOfDFasArray(bFieldPath, filename):              # return measurements as n x m array
    df = np.asarray(createDF(bFieldPath, filename))
    return df


def plotFieldMeasurementDataAndSavePlots(rawField, noiseField, cleanField, year, bFieldPath, filename):
# plot B-Field respecting factors depending on the investigated year and save clean field mean values as txt
    # depending on the year, different factors need to be applied
    if year == 2020:
        arrayPlotFactor = 1E6
        arrayScaleFactor = 1E6
        arrayDataFactor = 1E6
        ylimBFieldUp = 250
        ylimBFieldDown = -250
    elif year == 2021:
        arrayPlotFactor = 1E2
        arrayScaleFactor = 1E4
        arrayDataFactor = 1E-2
        ylimBFieldUp = 100
        ylimBFieldDown = -100
    elif year == 2017:
        arrayPlotFactor = 1E6
        arrayScaleFactor = 1E0
        arrayDataFactor = 1E0
        ylimBFieldUp = 200
        ylimBFieldDown = -200

    f1 = plt.subplots(1, 1, figsize=set_size(), sharey=True)
    plt.plot(np.multiply(noiseField, arrayPlotFactor), ":" , label = "Noise mean value in $\mu$T", color = specific_colors['G2E_black'])
    plt.plot(np.multiply(rawField, arrayPlotFactor), ':' , label = "B-Field with noise in $\mu$T", color = specific_colors['RawField'])
    plt.plot(np.multiply(cleanField, arrayPlotFactor),   label = "Clean B-Field in $\mu$T", color = specific_colors['MPM_lightblue'])
    plt.xlabel("Sensor number")
    plt.ylabel("Field Strength ($\mu$T)")
    plt.ylim(ylimBFieldDown, ylimBFieldUp)
    plt.xlim(0,len(cleanField)-1)
    plt.legend()


    plt.savefig(bFieldPath + filename[0: -11]+"_B_Field_CleanMeasured.pdf")
    measuredField = np.multiply(cleanField, arrayDataFactor)
    # # write values to csv
    print("Exported DataFrame to: " + bFieldPath + filename[0: -11]+"_B_Field_CleanMeasured.dat")
    np.savetxt(bFieldPath + filename[0: -11] + "_B_Field_CleanMeasured.dat", 
            measuredField,
            delimiter =", ", 
            fmt ='% s')


def plotDiffField(diffBField, date, name, affectedCurrent, savepath):
    # This function is used to visualize both, the faulty B-Field
    print("Visualization of diff Field")
    f3 = plt.subplots(1, 1, figsize=set_size(), sharey=True)
    plt.plot(np.multiply(diffBField,1), label = "Dif B-Field in $\mu$T mapped on Sensors", color = specific_colors['MPM_red'])
    plt.xlim(0,len(diffBField)-1)
    # plt.ylim(-10,10) # is not used, since the 
    plt.title('Differntial B-Field caused by {faulty} for {amps} A the {date}'.format(date = date, faulty = name, amps = affectedCurrent))
    plt.legend()
    plt.xlabel("Sensor number")
    plt.ylabel("B-Field Strength ($\mu$T)")
    plt.savefig(savepath + name + "_B_diffField_investigated.pdf")

def createViolinPlot(sensorDataFrame, name, savePath):
    # this is implemented in jupyter notebook and needs to be passed here
    pass


def normalizeBFieldsToCurrents(dataframeWithCurrentInfo, BbFieldWithoutNoiseMean, desiredCorruntNormalization, scalevCurrentToAmps):    # normalize B-Fields to current
    # this function is scaling the B-Field values to a certain current respecting linear conditions of the B-Field
    ## get mean value of current
    vVlauesOfCurrent = dataframeWithCurrentInfo[:,1]
    currentMeanValue = np.multiply(np.mean(vVlauesOfCurrent),scalevCurrentToAmps)
    ## calc factor for normalization
    normalizationFactor = desiredCorruntNormalization/currentMeanValue
    ## scale with the factor
    scaledBFieldWithoutNoiseMean = np.multiply(BbFieldWithoutNoiseMean, normalizationFactor)
    return scaledBFieldWithoutNoiseMean

# def plotErrorPlotsForOneSensorLayer(sensorsOfInterest, titleInformationData, ringsStd = list, ringsData = list, dataSet = pd.DataFrame, experiment = Experiment):  
#     '''SensorsOfInterest:  np.linspace(2, 32, 30, dtype=int), dataSet = testExperiment.bFieldDataC, ringsStd = [0, 0.25,  0.5, 0.75], ringsData = [-100, -50, 0, 50, 100]
#     titleInformationData = "With(/Without) noise"
#     ''' 
#     ## plot sensor circle with errorbars:
#     # Calculate standard deviation of each Sensor:
#     r2020 = np.zeros(len(sensorsOfInterest))
#     yErr2020 = np.zeros(len(sensorsOfInterest))
#     npos = 0
#     for i in sensorsOfInterest:
#         r2020[npos] = dataSet.iloc[:,i].mean()*experiment.arrayPlotFactor
#         yErr2020[npos] = dataSet.iloc[:,i].std(ddof=1)*experiment.arrayPlotFactor
#         npos = npos + 1

#     # get angle position of each sensor around the FC-Stack
#     theta = np.arange(0, 2 * np.pi, np.pi / 15)



    # ## plot Standard Deviation on sensors
    # fig, ax1 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
    # ax1.errorbar(theta, yErr2020, xerr=0, yerr=0, capsize=0.5,fmt=".", c="seagreen")
    # ax1.set_title(titleInformationData + " Standard Deviation on sensor measurements "+ "\n" +experiment.name + " " + experiment.date)
    # ax1.set_rticks(ringsStd)
    # fig.savefig(testExperiment.bFieldPath + testExperiment.name + "_Std_Polar.pdf")

    # ## plot Values on sensors
    # fig, ax2 = plt.subplots(1, 1, figsize=set_size(), sharey=True, subplot_kw={'projection': 'polar'})
    # ax2.errorbar(theta, r2020, xerr=0, yerr=0, capsize=1,fmt=",", c="seagreen")
    # ax2.set_title(titleInformationData + " Measurement around the Fuel Cell"+ "\n" +experiment.name + " " + experiment.date)
    # ax2.set_rticks(ringsData)
    # fig.savefig(experiment.bFieldPath + experiment.name + "_Measurement_Polar.pdf")


## Test:
# refMeasurementFile = "Pile_saine_Idc100A_Iac_10A_f0Hz_CENTRE.lvm"
# refMeasurementPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesure_2021\2021_07_28\Pile_saine\\"

# refMeasurementFile = "Ref_Pile_I48A_Centre.lvm"
# refMeasurementPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_24\Pile_Saine\\"


# measurementFile = "Ref_Pile_I48A_Centre.lvm"
# measurementPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_22\Pile Saine\Def_PileSaine\\"

# noisefile = "Ref_Bruit_Amb_Aux_ON_Centre.lvm"
# noisetPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_22\Bruit\\"

# # noisefile = "Banc_on_sans_courant_Idc0A_Iac_0A_f0Hz_CENTRE.lvm"
# # noisetPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesure_2021\2021_07_28\Bruitmesure\\"

# year = 2020
# scaleBFieldToFollowingCurrent = 50
# investigatedCurrent = 50
# sensorCount = 60

# # creatDiffBfieldForMIPSE(sensorCount, noisetPath, noisefile, refMeasurementPath, refMeasurementFile, measurementPath, measurementFile, year, scaleBFieldToFollowingCurrent, investigatedCurrent = investigatedCurrent, plotIt = False)
# sensorsOfInterest = np.linspace(60,89,30,dtype=int)
# date = "20200124"
# name = "Humidity 30 %"
# affectedCurrent = 50
# bFieldPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_24\Humidite\\"
# # appendSensorValuesonSensorMapping(sensorsOfInterest, date, name, affectedCurrent,bFieldPath)