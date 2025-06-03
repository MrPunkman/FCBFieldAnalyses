import numpy as np
import pandas as pd
from DataSeries import DataSeries
import json
import os

class MeasurementSet:
    def __init__(self,  file_path, file_name, fileFormat, name):
        self.file_path = file_path #.rstrip("\\")  # Remove trailing backslashes
        self.file_name = file_name
        self.name = name
        self.fileFormat = fileFormat
        
        self.data_series_list, self.metaInfo = self._load_data()

    def read_lvm_data(self, filepath) -> tuple[pd.DataFrame, list]:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Finde die zweite End_of_Header-Zeile
        header_end_count = 0
        metaInfo = {}
        data_start_index = None
        skip_rows = None

        for i, line in enumerate(lines):
            line = line.strip()
            if header_end_count < 1 and line:
            # Versuche, tab-getrennte Key-Value-Paare zu extrahieren
                parts = line.split('\t')
                if len(parts) >= 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    metaInfo[key] = value
                elif len(parts) == 1:
                    # Zeilen mit nur einem Teil (z. B. "LabVIEW Measurement")
                    metaInfo[f"__info_{len(metaInfo)}"] = parts[0]

            if '***End_of_Header***' in line:
                header_end_count += 1
                if header_end_count == 2:
                    # Erste Zeile nach dem 2. Header-Ende ist die Spaltennamen-Zeile
                    data_start_index = i + 1
                    skip_rows = data_start_index
                    break
                 
            

        # Lade Daten mit pandas, setze die richtige Trennung und das richtige Dezimalzeichen
        df = self.createDF(skip_rows)
        df = df.replace(",", ".", regex=True)  # Ensure numbers are correctly formatted
        df = df.astype(float)  # Convert all data to float type
        # df = df.dropna() # Drops rows having a NAN

        return df, metaInfo
    
    def createDF(self, skip_rows) -> pd.DataFrame:
        """
        Reads a .lvm file and removes the header before processing.
        """
        full_path = self.file_path + self.file_name  # Concatenate paths properly
        df = pd.read_csv(
            full_path, sep="\t", skiprows=[i for i in range(0, skip_rows)], header = 0
        )
        df = df.replace(",", ".", regex=True)  # Ensure numbers are correctly formatted
        df = df.astype(float)  # Convert all data to float type
        return df
    
    def _load_data(self):
        """
        Reads the .lvm file and creates multiple DataSeries objects, one for each column.
        The first column is time and the subsequent columns are data series.
        """
        metaInfo = None
        if self.fileFormat == "lvm":
            df, metaInfo = self.read_lvm_data(self.file_path + self.file_name)
            
        elif self.fileFormat == "csv":
            df = pd.read_csv(
                self.file_path + self.file_name, sep="\t", header = 0
            )
            df = df.replace(",", ".", regex=True)  # Ensure numbers are correctly formatted
            df = df.astype(float)  # Convert all data to float type
            df = df.dropna() # Drops rows having a NAN
            
        else: print("Delete . in file format or the file format is not supported.")

        # df = self.createDF(self.file_path, self.file_name)

        
        time_column = df.columns[0]
        time_values = df[time_column].values
        
        data_series_list = []
        for col in df.columns[1:]:
            data_series = DataSeries(time_values, df[col].values, name=col)
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
    
    def get_Mean_Value_Of_DataSeries(self, dataSeriesName:str) -> float:
        series = self.get_series_by_name(dataSeriesName)
        mean = series.calculate_mean()
        return mean

    def get_Std_Value_Of_DataSeries(self, dataSeriesName:str) -> float:
        series = self.get_series_by_name(dataSeriesName)
        std = series.calculate_std()
        return std    

    def save_to_file(self, filepath):
        """Saves the MeasurementSet to a CSV file."""
        # Create a dictionary with time as the first column and data series as other columns
        time_values = self.data_series_list[0].data_series.keys()
        data = {"Time": list(time_values)}
        
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
        
    

# measurement_set = MeasurementSet(r"Z:\09-Data\02-Hellen\Mesure_2021\2021_06_18\Stockio1_5", "Def_Stoch1_5_I100A_Centre_1.lvm", name="Noise")
# print(measurement_set.name)
# print([series.name for series in measurement_set.data_series_list])
# Assuming you have an existing MeasurementSet object
# measurement_set = MeasurementSet(r"Z:\09-Data\02-Hellen\Mesure_2021\2021_06_18\Stockio1_5", "test.lvm", name="Noise")

# Crop the data to the time range from 10 to 20 and save to a new file
# cropped_measurement_set = measurement_set.crop_MeasurementSet(minX=1, maxX=2)