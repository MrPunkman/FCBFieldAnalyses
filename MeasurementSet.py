import numpy as np
import pandas as pd
from DataSeries import DataSeries
import json
import os
import matplotlib.pyplot as plt
from thesis_general_imports import*
import math

class MeasurementSet:
    def __init__(self,  file_path, file_name, fileFormat, name):
        self.file_path = file_path 
        self.file_name = file_name
        self.name = name
        self.fileFormat = fileFormat
        self.df: pd.DataFrame
        self.metaInfo: dict
        self.commentDict: dict
        self.skip_rows: int
        self.mean_value_dict: dict
        self.physic_mean_value_dict: dict
        self.physic_without_Noise_mean_value_dict: dict
        self.std_value_dict: dict
        self.axialSensorNames: list
        self.radialSensorNames: list
        self.currantData: dict
        self.sensorPositions: pd.DataFrame
        self.b_field_sensors = []


        self.data_series_list, self.metaInfo = self._load_data()
        self.get_all_Names_AxialSensors()
        self.get_all_Names_RadialSensors()
        self.b_field_sensors = self.radialSensorNames + self.axialSensorNames
        self.pass_sensor_positions(r"Z:\06-Sensors\01-SensorPositions\2024-Leonard\Pos\2025-06-17-SensorPositionsWithOneAsField.txt")



    def pass_sensor_positions(self, sensor_position_file: str):
        """ Pass a sensor positions with x|y|z|u|v|w to annotate the information to each data series"""
        if self.axialSensorNames is None:
            self.get_all_Names_AxialSensors()
        if self.radialSensorNames is None:
            self.get_all_Names_RadialSensors()

        # Lade CSV mit Spalten: name, x, y
        self.sensorPositions = pd.read_csv(sensor_position_file, sep="	", header = None)

        sensor:DataSeries
        # Sensoren nacheinander mit Positionen verbinden
        for i, sensor in enumerate(self.b_field_sensors):
            # print(sensor)
            # print(type(sensor))
            x = self.sensorPositions.iloc[i, 0]
            y = self.sensorPositions.iloc[i, 1]
            z = self.sensorPositions.iloc[i, 2]
            u = self.sensorPositions.iloc[i, 3]
            v = self.sensorPositions.iloc[i, 4]
            w = self.sensorPositions.iloc[i, 5]
            r, theta = self.compute_sensor_angles(x, y)

            self.get_series_by_name(sensor).sensor_position_x = x
            self.get_series_by_name(sensor).sensor_position_y = y
            self.get_series_by_name(sensor).sensor_position_z = z
            self.get_series_by_name(sensor).sensor_position_u = u
            self.get_series_by_name(sensor).sensor_position_v = v
            self.get_series_by_name(sensor).sensor_position_w = w
            self.get_series_by_name(sensor).sensor_position = [x, y, z, u, v, w]
            self.get_series_by_name(sensor).sensor_Angle_theta = theta
            self.get_series_by_name(sensor).sensor_radius_r = r
            # print(self.get_series_by_name(sensor).sensor_position)




    def compute_sensor_angles(self, x, y):
        r = math.sqrt(x**2 + y**2)            # Radius
        theta = math.degrees(math.atan2(y, x))  # Winkel in Grad (-180 bis 180)
        
        # Sicherstellen, dass Winkel im Bereich 0–360 liegt
        if theta < 0:
            theta += 360

        return r, theta
             
        


    def read_lvm_data(self, filepath) -> tuple[pd.DataFrame, list]:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Finde die zweite End_of_Header-Zeile
        header_end_count = 0
        self.metaInfo = {}
        data_start_index = None
        self.skip_rows = None

        for i, line in enumerate(lines):
            line = line.strip()
            if header_end_count < 1 and line:
            # Versuche, tab-getrennte Key-Value-Paare zu extrahieren
                parts = line.split('\t')
                if len(parts) >= 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    self.metaInfo[key] = value
                elif len(parts) == 1:
                    # Zeilen mit nur einem Teil (z. B. "LabVIEW Measurement")
                    self.metaInfo[f"__info_{len(self.metaInfo)}"] = parts[0]

            if '***End_of_Header***' in line:
                header_end_count += 1
                if header_end_count == 2:
                    # Erste Zeile nach dem 2. Header-Ende ist die Spaltennamen-Zeile
                    data_start_index = i + 1
                    self.skip_rows = data_start_index
                    break
                 
            

        # Lade Daten mit pandas, setze die richtige Trennung und das richtige Dezimalzeichen
        self.df = self.createDF()
        self.df = self.df.replace(",", ".", regex=True)  # Ensure numbers are correctly formatted
        self.df = self.df.dropna()
        self.df = self.df.astype(float)  # Convert all data to float type
        # df = df.dropna() # Drops rows having a NAN

        return self.df, self.metaInfo
    
    def createDF(self) -> pd.DataFrame:
        """
        Reads a .lvm file and removes the metainfo before processing the data to a DataFrame.
        Saves the comment in an extra dict.
        """
        full_path = self.file_path + self.file_name  # Concatenate paths properly
        self.df = pd.read_csv(
            full_path, sep="\t", skiprows=[i for i in range(0, self.skip_rows)], header = 0
        )
        self.df = self.df.replace(",", ".", regex=True)  # Ensure numbers are correctly formatted
        # Extract 'comment' column if it exists
        
        self.comment_dict = {}
        if 'Comment' in self.df.columns:
            non_empty_comments = self.df['Comment'].dropna().astype(str)
            non_empty_comments = non_empty_comments[non_empty_comments.str.strip() != '']
            self.comment_dict = non_empty_comments.to_dict()
            self.df = self.df.drop(columns=['Comment'])  # Remove comment from main DataFrame
       
        self.df = self.df.astype(float)  # Convert all data to float type
       
        return self.df
    
    def _load_data(self):
        """
        Reads the .lvm file and creates multiple DataSeries objects, one for each column.
        The first column is time and the subsequent columns are data series.
        """
        metaInfo = None
        if self.fileFormat == "lvm":
            self.df, metaInfo = self.read_lvm_data(self.file_path + self.file_name)
            
        elif self.fileFormat == "csv":
            self.df = pd.read_csv(
                self.file_path + self.file_name, sep="\t", header = 0
            )
            self.df = self.df.replace(",", ".", regex=True)  # Ensure numbers are correctly formatted
            self.df = self.df.astype(float)  # Convert all data to float type
            self.df = self.df.dropna() # Drops rows having a NAN
            
        else: print("Delete . in file format or the file format is not supported.")
       
        time_column = self.df.columns[0]
        time_values = self.df[time_column].values
        
        data_series_list = []
        for col in self.df.columns[1:]:
            data_series = DataSeries(time_values, self.df[col].values, name=col)
            data_series_list.append(data_series)
        
        return data_series_list, metaInfo
    
    def get_series_by_name(self, name) -> DataSeries:
        """
        Retrieves a DataSeries object by its name.
        """
        for series in self.data_series_list:
            if series.name == name:
                return series
        return series
    
    def get_Sensor_Position_By_name(self, name) -> dict:
        """Returns a dict with Sensor Name and its position as a list [x, y, z, u, v, w]"""
        return {name: self.get_series_by_name(name).sensor_position}


    def get_Mean_Value_Of_DataSeries(self, dataSeriesName:str) -> float:
        """
        Obtain mean value of the specific Data Series
        """
        series = self.get_series_by_name(dataSeriesName)
        if not hasattr(series, 'mean_value'):   
            mean = series.calculate_mean()
        else: mean = series.mean_value
        return mean

    def get_Std_Value_Of_DataSeries(self, dataSeriesName:str) -> float:
        """
        Obtain std value of the specific Data Series
        """
        series = self.get_series_by_name(dataSeriesName)
        if not hasattr(series, 'std'):
            std = series.calculate_std()
        else: std = series.std
        return std    

    def save_to_file(self, filepath):
        """Saves the MeasurementSet to a CSV file."""
        # Create a dictionary with time as the first column and data series as other columns
        time_values = self.data_series_list[0].data_series.keys()
        data = {"Time": list(time_values)}
        series: DataSeries
        for series in self.data_series_list:
            data[series.name] = list(series.data_series.values())
        
        # Convert the dictionary to a DataFrame and save it as CSV
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)  # Save the DataFrame to CSV without index column

    def crop_MeasurementSet(self, minX, maxX):
        """
        Crops the current MeasurementSet to only include data series that
        have time values within the specified range [minX, maxX].
        Returns a new MeasurementSet containing the cropped data and saves it to a file.
        """
        cropped_data_series = []
        series: DataSeries
        # For each DataSeries in the current MeasurementSet, crop it to the desired time range
        for series in self.data_series_list:
            cropped_series = series.get_series_in_time_span(minX, maxX)
            cropped_data_series.append(cropped_series)
        
        # Return a new MeasurementSet with the cropped data series
        cropped_measurement_set = MeasurementSet(
            file_path = self.file_path,
            file_name = self.file_name,
            name = f"{self.name} - Cropped {minX:.2f} to {maxX:.2f}",
            skip_rows = self.skip_rows
        )
        
        # Update the new MeasurementSet with the cropped data series
        cropped_measurement_set.data_series_list = cropped_data_series
        
        # Generate the new file name containing the crop range
        new_file_name = f"{os.path.splitext(self.file_name)[0]}_Cropped_{minX:.2f}_to_{maxX:.2f}.csv"
        new_file_path = os.path.join(self.file_path, new_file_name)
        
        # Save the cropped MeasurementSet to a CSV file
        cropped_measurement_set.save_to_file(new_file_path)
        
        # Return the cropped MeasurementSet
        return cropped_measurement_set
        
    def get_Data_Frame(self) -> pd.DataFrame:
        return self.data_series_list
    
    def get_all_Mean_Values(self) -> dict:
        sensor: DataSeries
        self.mean_value_dict = {}
        for sensor in self.data_series_list:
            self.mean_value_dict.update({sensor.name: sensor.calculate_mean()})
        return self.mean_value_dict
    
    def get_all_Physic_Mean_with_Noise_Values(self) -> dict:
        sensor: DataSeries
        self.physic_mean_value_dict = {}
        for sensor in self.data_series_list:
            self.physic_mean_value_dict.update({sensor.name: sensor.calculate_physic_mean()})
        return self.physic_mean_value_dict
    

    def get_all_std_Values(self) -> dict:
        sensor: DataSeries
        self.std_value_dict = {}
        for sensor in self.data_series_list:
            self.std_value_dict.update({sensor.name: sensor.calculate_std()})
        return self.std_value_dict
    

    def createNewSeriesAndRemoveOutliersFromSeries(self, nameOfSeries : DataSeries, threshold = 1):
        if not hasattr(self.get_series_by_name(nameOfSeries), "std"):
            self.get_series_by_name(nameOfSeries).calculate_mean()
            self.get_series_by_name(nameOfSeries).calculate_std()
        newDataSeries = self.get_series_by_name(nameOfSeries).get_filtered_series(threshold)
        newDataSeries.name = self.get_series_by_name(nameOfSeries).name + "-Filtered-"+ str(threshold)
        self.data_series_list.append(newDataSeries)
        newDataSeries.convert_raw_to_data_series()
        print(newDataSeries.name)
    
    def get_all_Names_RadialSensors(self) -> list:
        """This function supports only Sensor data which have an string "Rad" as ending"""
        self.radialSensorNames = []
        sensor: DataSeries

        for sensor in self.data_series_list:
            if sensor.name[-3:] == 'Rad':
                self.radialSensorNames.append(sensor.name)
                sensor.unit_name = "B"
        return self.radialSensorNames       
    
    def get_all_Names_AxialSensors(self) -> list:
        """This function supports only Sensor data which have an string "Ax" as ending"""
        self.axialSensorNames = []
        sensor: DataSeries
        for sensor in self.data_series_list:
            if sensor.name[-2:] == 'Ax':
                self.axialSensorNames.append(sensor.name)
                sensor.unit_name = "B"
        return self.axialSensorNames

    def get_Current_data(self, factor = 100) -> dict:
        """This function returns a dict with time stamp and currant data converted respecting your passed factor"""
        self.currentData = {}
        sensor : DataSeries

        for sensor in self.data_series_list:
            if sensor.name[-2:] == '-I':
                self.currentData = sensor.convert_raw_to_data_series(factor)
                sensor.unit_name = "I"
        return self.currentData
    
    def get_Voltage_data(self, factor = 1) -> dict:
        """This function returns a dict with name and voltage data converted respecting your passed factor"""
        self.tensionData = {}
        sensor : DataSeries

        for sensor in self.data_series_list:
            if "Tension" in sensor.name:
                sensor.unit_name = "U"
                self.tensionData.update({sensor.name: list(sensor.convert_raw_to_data_series(factor).values())})
        return self.tensionData

    def plot_Field_measurement_over_time(self, sensorsOfInterest: list[list[str]], save_Annotation = ""):
        """Give a list with the Magnetic field sensor names you want to plot.
        The List must contain 4 entries of different Lists with the Sensors for Y-Neg, X-Neg, Y-Pos, X-Pos"""

        all_values_Y = []  # Y-Neg & Y-Pos
        all_values_X = []  # X-Neg & X-Pos

        fig, axs = plt.subplots(2, 2, figsize=(15 , 14))
        titles = ["Y-Neg", "X-Neg", "Y-Pos", "X-Pos"]
        positions = [(0, 0), (1, 0), (0, 1), (1, 1)]

        for idx, sensor_list in enumerate(sensorsOfInterest):
            row, col = positions[idx]
            ax = axs[row][col]

            for sensor_name in sensor_list:
                series = self.get_series_by_name(sensor_name)
                if series:
                    values = list(series.convert_raw_to_data_series().values())
                    ax.plot(values, label=sensor_name)

                    # collect values for later y limits
                    if row == 0:
                        all_values_Y.extend(values)
                    else:
                        all_values_X.extend(values)

            ax.set_title(titles[idx])
            ax.legend()
        
            # Y- annotation
            if row == 0:
                ax.set_ylabel("Magnetic Field [Y]")
            else:
                ax.set_ylabel("Magnetic Field [X]")

                # set y - limits
            if all_values_Y:
                ymin, ymax = min(all_values_Y), max(all_values_Y)
                axs[0][0].set_ylim(ymin, ymax)
                axs[0][1].set_ylim(ymin, ymax)

            if all_values_X:
                xmin, xmax = min(all_values_X), max(all_values_X)
                axs[1][0].set_ylim(xmin, xmax)
                axs[1][1].set_ylim(xmin, xmax)
            fig.savefig(self.file_path + self.name + save_Annotation +"Field-Time-Vizualisation.pdf",transparent=True)
            fig.savefig(self.file_path + self.name + save_Annotation +"Field-Time-Vizualisation.svg",transparent=True)

    
    def plot_current_measurement_over_time(self, factor = 10, save_Annotation = ""):
        """Plots the current over time. You can apply a factor if needed to convert from raw data to phyisics (10 is given as standard)"""
        currentDataSeries = self.get_Current_data(factor)
        fig, ax = plt.subplots(1, 1, figsize=set_size())
        ax.plot(currentDataSeries.values(), label = "Current")
        ax.set_ylim(0, max(currentDataSeries.values())*1.1)
        ax.set_ylabel("Current in A")
        ax.set_xlabel("Measurement Point ()")
        ax.legend()
        fig.savefig(self.file_path + self.name + save_Annotation +"Current-Time-Vizualisation.pdf",transparent=True)
        fig.savefig(self.file_path + self.name + save_Annotation +"Current-Time-Vizualisation.svg",transparent=True)
        
        
    def plot_voltage_measurement_over_time(self, sensorsOfInterest: list):
        """Plots the voltage over time """
        pass      


    def plot_polar_Mean_fixed_sensors(self, sensor_names: list):
        """
        Plots mean value for each sensor, respecting its position on the circle around the stack
        """
        
        num_sensors = len(sensor_names)
        
        # Berechne feste Winkelpositionen (gegen den Uhrzeigersinn)
        angles_deg = []
        angles_rad = []

        means = []
        for name in sensor_names:
            sensor = self.get_series_by_name(name)
            if sensor:
                means.append(sensor.calculate_physic_mean())
                angles_rad.append(np.deg2rad(sensor.sensor_Angle_theta))
            else:
                angles_rad.append(0)
                means.append(0)

        # Kreis schließen
        angles_rad = np.append(angles_rad, angles_rad[0])
        means = np.append(means, means[0])

        # Plot
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=set_size())
        ax.errorbar(angles_rad, means, xerr=0, yerr=0, capsize=0.5,fmt=",", c="blue")

        # Achsen-Einstellungen
        ax.set_theta_zero_location('N')    # 0° ist oben
        ax.set_theta_direction(-1)         # gegen den Uhrzeigersinn
        ax.set_title("Mean value in \micro T", va='bottom')

        # Labels außen, horizontal
        label_radius = max(means) * 1.1
        for angle, name in zip(angles_rad[:-1], sensor_names):  # ohne duplizierten Wert
            ax.text(angle, label_radius, name, ha='center', va='center', fontsize=8)

    def plot_polar_STD_fixed_sensors(self, sensor_names: list):
        """
        Plots std value for each sensor, respecting its position on the circle around the stack
        """
        
        num_sensors = len(sensor_names)
        
        # Berechne feste Winkelpositionen (gegen den Uhrzeigersinn)
        angles_deg = []
        angles_rad = []

        std = []
        for name in sensor_names:
            sensor = self.get_series_by_name(name)
            if sensor:
                std.append(sensor.calculate_std())
                angles_rad.append(np.deg2rad(sensor.sensor_Angle_theta))
            else:
                angles_rad.append(0)
                std.append(0)

        # Kreis schließen
        angles_rad = np.append(angles_rad, angles_rad[0])
        std = np.append(std, std[0])

        # Plot
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=set_size())
        ax.errorbar(angles_rad, std, xerr=0, yerr=0, capsize=0.5,fmt=",", c="blue")

        # Achsen-Einstellungen
        ax.set_theta_zero_location('N')    # 0° ist oben
        ax.set_theta_direction(-1)         # gegen den Uhrzeigersinn
        ax.set_title("Std value in V", va='bottom')

        # Labels außen, horizontal
        label_radius = max(std) * 1.1
        for angle, name in zip(angles_rad[:-1], sensor_names):  # ohne duplizierten Wert
            ax.text(angle, label_radius, name, ha='center', va='center', fontsize=8)
    
    def get_All_Cleaned_Data(self) -> dict:
        """This function returns all mean values subtracted by mean noise in Phyical Unit"""
        sensor: DataSeries
        cleanedDataDict = {}
        for sensor in self.b_field_sensors:
            cleanedDataDict.update({sensor: self.get_series_by_name(sensor).physic_mean_Minus_meanNoise})
        return cleanedDataDict
    
    def get_All_Mean_Data(self) -> dict:
        """This function returns all mean values subtracted by mean noise in Phyical Unit"""
        sensor: DataSeries
        cleanedDataDict = {}
        for sensor in self.b_field_sensors:
            cleanedDataDict.update({sensor: self.get_series_by_name(sensor).physic_mean_with_Noise})
        return cleanedDataDict
# measurement_set = MeasurementSet(r"Z:\09-Data\02-Hellen\Mesure_2021\2021_06_18\Stockio1_5", "Def_Stoch1_5_I100A_Centre_1.lvm", name="Noise")
# print(measurement_set.name)
# print([series.name for series in measurement_set.data_series_list])
# Assuming you have an existing MeasurementSet object
# measurement_set = MeasurementSet(r"Z:\09-Data\02-Hellen\Mesure_2021\2021_06_18\Stockio1_5", "test.lvm", name="Noise")

# Crop the data to the time range from 10 to 20 and save to a new file
# cropped_measurement_set = measurement_set.crop_MeasurementSet(minX=1, maxX=2)