from dataclasses import asdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from collectAllMeasureDataInOneFile import *
from thesis_general_imports import *
import csv
# from deprecated import deprecated
from MeasurementSet import*

# import seaborn as sns


class DynamicExperiment:
    # for 2020: 64.86 (50 A); 60 to 100 A
    # scaleVCurrentToAmps = 64.86
    # scaleCurrentTo = 50
# noiseBFieldPath : str, filenamenoiseC : str,

    def __init__(self, name : str,  bFieldPath : str, filenameC : str, fileFormat : str):
        self.name = name
        self.fileFormat = fileFormat
        ## Create Measurement Set object for measurement
        
        self.measurement = MeasurementSet(bFieldPath, filenameC, "lvm", "Test")
        
        # self.dataOnly, self.metaInfo = self.measurement.read_lvm_data(bFieldPath + filenameC)
        
        # get date
        self.date = self.measurement.metaInfo["Date"]
        self.time = self.measurement.metaInfo["Time"]
        ## Create Measurement Set object for noise
                
        
        ## Define path and files for noise Data
        # self.noiseBFieldPath = noiseBFieldPath

        # self.filenamenoiseCenter = measurementSetNoiseC
     

    # ____________________________________________________________Start new Functions_____________________________________________________________________________________________
    
    


    ## for noise treatment: subtract vector with 60 entries
    def clearNoiseFromBFieldMeasurements(self, df, subtractor):
        # print("Clean Noise from measurements start")
        c = 0
        result = pd.DataFrame(columns=self.sensorNames[2:62])
        for i in range(2, 62):
            result.iloc[:, c] = df.iloc[:, i].sub(subtractor[c])
            c = c + 1
        # print("Clean Noise from measurements end")
        return result

    ## Calculate field with: $B_mean - B_noise_mean$
    # @deprecated("This Function uses the calculation of the $B_mean - B_noise_mean$ to try to reproduce results from Lyes Ifrek. DO NOT USE!")
    def BFieldMeanCalcTest(self):
        self.BFieldDirtyC = np.subtract(self.BFieldMeanvalueWithNoiseC, self.noiseBFieldMeanvalueC)
        
    ## calculate B-Field mean values of a Noise frame
    def BFieldMeanValueNoise(self, df):  
        # print("Calculate Mean values start")
        BFieldArray = np.zeros(60)
        i = 0
        for sensors in range(2, 62):
            BFieldArray[i] = df.iloc[:, sensors].mean(axis=0)
            i = i + 1
        # print("Calculate Mean values end")
        return BFieldArray

    ## calculate B-Field mean values of a noise-free DF
    def BFieldMeanValueClean(self, df):
        # print("Calculate Mean values noise free start")
        BFieldArray = np.zeros(60)
        i = 1
        for sensors in range(0, len(BFieldArray)):
            BFieldArray[sensors] = df.iloc[:, sensors].mean(axis=0)
            i = i + 1
        # print("Calculate Mean values noise free end")
        return BFieldArray

    def createDF(self, bFieldPath, filename):
        """This function is to read a .lvm file and read the data without the header"""
        ## import file and set file path
        # print("reading Data start")
        df = pd.read_csv(
            bFieldPath + filename, sep="	", skiprows=[i for i in range(0, self.skipRows)]
        )
        ## change , to . for later calculations. Otherwise, the cell is declared as string and no calculation can be done
        df = df.replace(",", ".", regex=True)
        # change type to float
        df = df.astype(float)
        # print("reading Data end")
        return df
    
    

   
# Test
# filePath = r"Z:\09-Data\00-Thesis\00_TestBench_Ini\2025-05-13\\"
# fileName = r"5A-FieldTest.lvm"
filePath = r"Z:\09-Data\02-Hellen\Mesure_2021\2021_06_18\Stockio1_5\\"
fileName = r"test.lvm"
name = "test"
testExperiment = DynamicExperiment(name, filePath, fileName, ".lvm")
print(testExperiment.date)
print(testExperiment.time)
# print(TestExperiment.dataOnly[2].mean)
series = testExperiment.measurement.get_series_by_name("S2_V4_C5_X_AI06")
print(series.length)
mean = testExperiment.measurement.get_Mean_Value_Of_DataSeries("S2_V4_C5_X_AI06")
print(mean)

# print(TestExperiment.measurement.get_series_by_name("S2_V7_C8_X_AI02").get_Value(0))
########### Test
# noiseBFieldPath = r'C:\Users\Mein\tubCloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_22\Bruit\\'
# filenamenoiseAV = "Ref_Bruit_Ambiant_FM_Aux_On_AV_2.lvm"
# filenamenoiseCenter = "Ref_Bruit_Ambiant_FM_Aux_On_Centre_1.lvm"
# filenamenoiseAR = "Ref_Bruit_Ambiant_FM_Aux_On_AR_1.lvm"


# bFieldPath = r"C:\Users\Mein\tubCloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_22\Stochio_1_5\Def_Stoch_1_5\\"

# # call file name
# filenameAR = 'Def_Stoch1_5_I48A_AR.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
# filenameC = 'Def_Stoch1_5_I48A_Centre.lvm'                 ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
# filenameAV = 'Def_Stoch1_5_I48A_AV.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!


# TestExperiment = Experiment(2020, 50, "22.01.2020", 48, 100, noiseBFieldPath, filenamenoiseAV, filenamenoiseCenter,filenamenoiseAR, bFieldPath, filenameAV, filenameC, filenameAR)
# TestExperiment.calculateCleanFields()

## Humidity 2020_01_24 #####################################################################################
# noiseBFieldPath = r'C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_24\Bruit\\'
# filenamenoiseAV = "Ref_Bruit_Ambiant_FM_Aux_On_AV.lvm"
# filenamenoiseCenter = "Ref_Bruit_Ambiant_FM_Aux_On_Centre.lvm"
# filenamenoiseAR = "Ref_Bruit_Ambiant_FM_Aux_On_AR.lvm"

# bFieldPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_24\Humidite\\"
# filenameAR = 'Def_Hum30_I50A_AR.lvm'                    ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
# filenameC = 'Def_Hum30_I50A_Centre.lvm'                 ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
# filenameAV = 'Def_Hum30_I50A_AV.lvm'                    ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
# year = 2020
# scaleBFieldToFollowingCurrent = 50
# investigatedCurrent = 50

# testExperiment = Experiment(2020, "Humidity 30 %", "24.01.2020", 50, 50, noiseBFieldPath, filenamenoiseAV, filenamenoiseCenter,filenamenoiseAR, bFieldPath, filenameAV, filenameC, filenameAR)
