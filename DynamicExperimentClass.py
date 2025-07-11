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
plt.style.use('./ieee.mplstyle')

# import seaborn as sns


class DynamicExperiment:
    """ Name the Experiment with name, pass a path, a filename and a file format for the experiment data. 
    Pass the same information for the noise data"""
    # for 2020: 64.86 (50 A); 60 to 100 A
    # scaleVCurrentToAmps = 64.86
    # scaleCurrentTo = 50
# noiseBFieldPath : str, filenamenoiseC : str,

    def __init__(self, dataName : str,  bFieldPath : str, dataFileName : str, fileFormat : str,
                 noiseName: str, noisebFieldPath : str, noiseDataFileName : str, noiseFileFormat : str):
        self.name = dataName
        self.bFieldPath = bFieldPath
        self.dataFileName = dataFileName
        self.fileFormat = fileFormat
        self.noisebFieldPath = noisebFieldPath
        self.noiseDataFileName = noiseDataFileName
        self.noiseFileFormat = noiseFileFormat
        self.noiseName = noiseName
        
        self.noiseMean: dict
        self.noise_Mean_physic: dict
        self.physic_with_noise_mean_value_dict: dict
        self.physic_without_Noise_mean_value_dict : dict
        self.physic_mean_value_dict_scaled_to_current: dict
        self.scaleToCurrent: float
        self.currentScaleFactor: float
        
        ## Create Measurement Set object for measurement
        self.dataMeasurement = MeasurementSet(self.bFieldPath, self.dataFileName, fileFormat, dataName)

        ## Create Seconde Measurement Set object for noise
        self.noiseMeasurement = MeasurementSet(self.noisebFieldPath, self.noiseDataFileName, self.noiseFileFormat, self.noiseName)
        
        # get date
        self.dataDate = self.dataMeasurement.metaInfo["Date"]
        self.dataTime = self.dataMeasurement.metaInfo["Time"]
        self.noiseDate = self.noiseMeasurement.metaInfo["Date"]
        self.noiseTime = self.noiseMeasurement.metaInfo["Time"]
        self.sensorsOfInterest = self.set_ini_all_sensors_of_interest()
    # ____________________________________________________________Start new Functions_____________________________________________________________________________________________
    
    def set_ini_all_sensors_of_interest(self) -> list:
        self.sensorsOfInterest = self.dataMeasurement.get_all_Names_RadialSensors() + self.dataMeasurement.get_all_Names_AxialSensors()
        return self.sensorsOfInterest

    def get_all_magnetic_Field_mean_values_with_noise(self) -> dict:
        """Compute and returns all magnetic field values containing noise"""
        self.dataMeasurement.get_all_Physic_Mean_with_Noise_Values()
        self.magnetic_Field_mean_values_with_noise = {}
        for sensor in self.dataMeasurement.b_field_sensors:
            if self.dataMeasurement.get_series_by_name(sensor).unit_name == "B":
                self.magnetic_Field_mean_values_with_noise.update({self.dataMeasurement.get_series_by_name(sensor).name : self.dataMeasurement.get_series_by_name(sensor).calculate_physic_mean()})
        return self.magnetic_Field_mean_values_with_noise
    
    def scale_Current_with_currentScaleFactor(self):
        if not hasattr(self, 'physic_without_Noise_mean_value_dict'): self.compute_Physic_Mean_minus_Noise_mean_Values()
        # print(self.dataMeasurement.)
        self.physic_mean_value_dict_scaled_to_current = {}
        for sensor in self.physic_without_Noise_mean_value_dict:
            scaledValue = self.physic_without_Noise_mean_value_dict[sensor] * self.currentScaleFactor
            self.physic_mean_value_dict_scaled_to_current.update({sensor: scaledValue})
    
    def compute_Noise_Mean_dict(self) -> dict:
        self.noiseMean = self.noiseMeasurement.get_all_Mean_Values()
        return self.noiseMeasurement.get_all_Mean_Values()
    
    def compute_physic_with_noise_mean_value_dict(self) -> dict:
        """Returns all mean values with noise for all sensors"""
        self.physic_with_noise_mean_value_dict = self.dataMeasurement.get_all_Physic_Mean_with_Noise_Values()
        return self.physic_with_noise_mean_value_dict
    
    def compute_Noise_Mean_Physic_dict(self) -> dict:
        """Returns all noise mean values for all sensors"""
        self.noise_Mean_physic = self.noiseMeasurement.get_all_Physic_Mean_with_Noise_Values()
        return self.noiseMeasurement.get_all_Physic_Mean_with_Noise_Values()
    
    def compute_Data_Mean_dict(self) -> dict:
        return self.dataMeasurement.get_all_Mean_Values()
    
    def compute_Noise_std_dict(self) -> dict:
        return self.noiseMeasurement.get_all_std_Values()
    
    def compute_Data_std_dict(self) -> dict:
        return self.dataMeasurement.get_all_std_Values()
    
    def compute_Physic_Mean_minus_Noise_mean_Values(self) -> dict:
        sensor: DataSeries
        self.physic_without_Noise_mean_value_dict = {}
        for sensor in self.dataMeasurement.data_series_list:
            # print(sensor.name) 
            if sensor.name in self.sensorsOfInterest:
                # print(sensor.name + " in list")
                meanData = self.dataMeasurement.get_series_by_name(sensor.name).calculate_physic_mean()
                # print(meanData)
                meanNoise = self.noiseMeasurement.get_series_by_name(sensor.name).calculate_physic_mean()
                # print(meanNoise)
                value = meanData - meanNoise
                # print(value)
                self.dataMeasurement.get_series_by_name(sensor.name).physic_mean_Minus_meanNoise = value 
                self.physic_without_Noise_mean_value_dict.update({sensor.name: self.dataMeasurement.get_series_by_name(sensor.name).physic_mean_Minus_meanNoise})
            # else: print(sensor.name + " NOT in list")
        return self.physic_without_Noise_mean_value_dict
    
    

    def plot_scaled_and_initial_Field(self):
        """Plots the initial Field and the scaled field. Can be used to visualize the impact of the scaling"""
        fig, ax = plt.subplots(figsize=set_size())
        ax.plot(self.physic_without_Noise_mean_value_dict.keys(), self.physic_without_Noise_mean_value_dict.values(), marker = ".", label = "Measured Field")
        ax.plot(self.physic_mean_value_dict_scaled_to_current.keys(),self.physic_mean_value_dict_scaled_to_current.values(), marker = ".", label = "Scaled Field")
        plt.legend()
        plt.xticks(rotation = 90)

        # get y-axis limits of the plot
        low, high = plt.ylim()
        # find the new limits
        bound = max(abs(low), abs(high))
        # set new limits
        plt.ylim(-bound, bound)

    def plot_polar_Mean_for_CleanedValues_fixed_sensors(self, sensor_names: list):
        """
        Plots std value for each sensor, respecting its position on the circle around the stack
        """
        
        num_sensors = len(sensor_names)
        
        # Compute angle positions
        angles_deg = []
        angles_rad = []
        sensor: DataSeries
        value = []
        for name in sensor_names:
            sensor = self.dataMeasurement.get_series_by_name(name)
            if sensor:
                value.append(sensor.physic_mean_Minus_meanNoise)
                angles_rad.append(np.deg2rad(sensor.sensor_Angle_theta))
            else:
                angles_rad.append(0)
                value.append(0)

        # Kreis schließen
        angles_rad = np.append(angles_rad, angles_rad[0])
        value = np.append(value, value[0])

        # Plot
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=set_size())
        ax.errorbar(angles_rad, value, xerr=0, yerr=0, capsize=0.5,fmt=",", c="blue")

        # Achsen-Einstellungen
        ax.set_theta_zero_location('N')    # 0° ist oben
        ax.set_theta_direction(-1)         # gegen den Uhrzeigersinn
        ax.set_title("Cleaned value in \micro T", va='bottom')

        # Labels außen, horizontal
        label_radius = max(value) * 1.1
        for angle, name in zip(angles_rad[:-1], sensor_names):  # ohne duplizierten Wert
            ax.text(angle, label_radius, name, ha='center', va='center', fontsize=8)

        
    
    # for noise treatment: subtract vector with 60 entries
    def clearAllNoiseFromBFieldMeasurements(self):
        """ subtracts mean - mean"""
        sensor : DataSeries
        for sensor in self.dataMeasurement.data_series_list:
            self.dataMeasurement.get_series_by_name(sensor.name).physic_mean_Minus_meanNoise = self.noiseMeasurement.get_series_by_name(sensor.name).calculate_physic_mean() - self.dataMeasurement.get_series_by_name(sensor.name).calculate_physic_mean()
        



    
    

   
# Test
# filePath = r"Z:\09-Data\00-Thesis\00_TestBench_Ini\2025-05-13\\"
# fileName = r"5A-FieldTest.lvm"
# NoisePath = r"Z:\09-Data\00-Thesis\00_TestBench_Ini\2025-05-13\\"
# NoiseFile = r"0A-FieldTest.lvm"
# name = "5A-Test"
# noiseName = "noise"
# testExperiment = DynamicExperiment(name, filePath, fileName, "lvm", noiseName, NoisePath, NoiseFile, "lvm")
# print(testExperiment.dataMeasurement.get_all_Names_RadialSensors())
# print(testExperiment.dataMeasurement.get_all_Names_AxialSensors())

# print(testExperiment.dataDate)
# print(testExperiment.dataTime)
# # print(TestExperiment.dataOnly[2].mean)
# series = testExperiment.dataMeasurement.get_series_by_name("S2_V4_C5_X_AI06")
# sensorMeanDict = testExperiment.compute_Noise_Mean_dict()
# print(sensorMeanDict.values())
# mean = testExperiment.dataMeasurement.get_Mean_Value_Of_DataSeries("S2_V4_C5_X_AI06")
# print(mean)

# print(TestExperiment.measurement.get_series_by_name("S2_V7_C8_X_AI02").get_Value(0))
########### Test
# noiseBFieldPath = r'C:\Users\Mein\tubCloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_22\Bruit\\'
# filenamenoiseAV = "Ref_Bruit_Ambiant_FM_Aux_On_AV_2.lvm"
# filenamenoiseCenter = "Ref_Bruit_Ambiant_FM_Aux_On_Centre_1.lvm"
# filenamenoiseAR = "Ref_Bruit_Ambiant_FM_Aux_On_AR_1.lvm"

