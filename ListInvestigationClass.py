from DynamicExperimentClass import *
import pandas as pd

class ListInvestigation():
    def __init__(self, listOfExperiments :list) -> None:
        self.listOfExperiments = listOfExperiments
        self.sensorsOfInterest: list
        self.sensorMeanValuesHealthy: dict
        self.sensorMeanValuesHealthy_Noise: dict
        self.sensorMeanValuesHealthy_without_Noise: dict
        self.sensorMeanValuesFaulty: dict
        self.sensorMeanValuesFaulty_Noise: dict
        self.sensorMeanValuesFaulty_without_Noise: dict
        self.differential_Mean_Values_without_Noise: dict
        self.differential_Mean_Values_with_Noise: dict
        self.sensorPositions: dict
        self.healthy_voltages: dict
        self.faulty_voltages: dict
        self.healthy_current: float
        self.faulty_current: float
        self.differential_scaled_Mean_Values_without_Noise = {}
        self.differential_scaled_Mean_Values_with_Noise = {}

    def scale_current_to_Current(self, scaleToCurrent:float):
        self.scaleToCurrent = scaleToCurrent
        self.healthyExperiment.scaleToCurrent = scaleToCurrent
        self.faultyExperiment.scaleToCurrent = scaleToCurrent
        
        if not hasattr(self, "healthy_current"): self.healthy_current = self.get_Mean_current_Healthy_Measurement()
        if not hasattr(self, "faulty_current"): self.faulty_current = self.get_Mean_current_Faulty_Measurement()
        
        # compute scaling factor for field, assuming, a linear behavior between current and field stength
        self.healthyExperiment.currentScaleFactor = self.healthyExperiment.scaleToCurrent/self.healthy_current
        self.faultyExperiment.currentScaleFactor = self.faultyExperiment.scaleToCurrent/self.faulty_current

        # scale current:
        self.faultyExperiment.scale_Current_with_currentScaleFactor()
        self.healthyExperiment.scale_Current_with_currentScaleFactor()


    def set_sensors_Of_Interest(self, sensorNamelist: list):
        self.sensorsOfInterest = sensorNamelist
        self.healthyExperiment.sensorsOfInterest = sensorNamelist
        self.faultyExperiment.sensorsOfInterest = sensorNamelist

    def get_sensors_Of_interest(self) -> list:
        return self.sensorsOfInterest
    
    def compute_Healthy_sensors_mean_Values_with_Noise(self) -> dict:
        """Compute Healthy (PointOne) mean values of the Sensors of interest. This value includes noise"""
        self.sensorMeanValuesHealthy = {}
        sensor: DataSeries
        for sensor in self.healthyExperiment.dataMeasurement.b_field_sensors:
            if sensor in self.sensorsOfInterest:
                if not hasattr(self.healthyExperiment.dataMeasurement.get_series_by_name(sensor), "physic_mean_with_Noise"): self.healthyExperiment.dataMeasurement.get_series_by_name(sensor).calculate_physic_mean()
                self.sensorMeanValuesHealthy.update({sensor: self.healthyExperiment.dataMeasurement.get_series_by_name(sensor).physic_mean_with_Noise})
        return self.sensorMeanValuesHealthy
    
    def compute_Faulty_sensors_mean_Values_with_Noise(self) -> dict:
        """Compute Faulty (PointTwo)  mean values of the Sensors of interest. This value includes noise"""
        self.sensorMeanValuesFaulty = {}
        sensor: DataSeries
        for sensor in self.faultyExperiment.dataMeasurement.b_field_sensors:
            if sensor in self.sensorsOfInterest:
                if not hasattr(self.faultyExperiment.dataMeasurement.get_series_by_name(sensor), "physic_mean_with_Noise"): self.faultyExperiment.dataMeasurement.get_series_by_name(sensor).calculate_physic_mean()
                self.sensorMeanValuesFaulty.update({sensor: self.faultyExperiment.dataMeasurement.get_series_by_name(sensor).physic_mean_with_Noise})
        return self.sensorMeanValuesFaulty
    
    def compute_Faulty_sensors_mean_Values_without_Noise(self) -> dict:
        """Compute Faulty (PointTwo)  mean values of the Sensors of interest without Noise."""
        self.sensorMeanValuesFaulty_without_Noise = {}
        self.sensorMeanValuesFaulty_without_Noise = self.faultyExperiment.compute_Physic_Mean_minus_Noise_mean_Values()
        return self.sensorMeanValuesFaulty_without_Noise
    
    def compute_Differential_Mean_valeus(self):
        """Computes Faulty - Healthy. Therefore, we must first subtract the noise"""
        if not hasattr(self, "sensorMeanValuesHealthy"):
            self.compute_Healthy_sensors_mean_Values_with_Noise()
        if not hasattr(self, "sensorMeanValuesFaulty"):
            self.compute_Faulty_sensors_mean_Values_with_Noise()

        if not hasattr(self, "sensorMeanValuesHealthy_Noise"):
            self.sensorMeanValuesHealthy_Noise = self.healthyExperiment.compute_Noise_Mean_dict()
        if not hasattr(self, "sensorMeanValuesFaulty_Noise"):
            self.sensorMeanValuesFaulty_Noise = self.faultyExperiment.compute_Noise_Mean_dict()
        
        self.differential_Mean_Values_without_Noise = {}
        self.differential_Mean_Values_with_Noise = {}
        for sensorName in self.sensorMeanValuesFaulty:
            faulty = self.sensorMeanValuesFaulty[sensorName] - self.sensorMeanValuesFaulty_Noise[sensorName]
            healhy = self.sensorMeanValuesHealthy[sensorName] - self.sensorMeanValuesHealthy_Noise[sensorName]
            differntialValue = faulty - healhy
            self.differential_Mean_Values_without_Noise.update({sensorName: differntialValue})

    def compute_Differential_Mean_valeus_with_scaled_Current(self):
        """Computes scaled values: Faulty - Healthy. Therefore, we must first subtract the noise. The magnetic field strength must be scaled before hand to a desired current"""
        # if not hasattr(self, "sensorMeanValuesHealthyScaled"):
        #     self.compute_Healthy_sensors_mean_Values_with_Noise()
        # if not hasattr(self, "sensorMeanValuesFaultyScaled"):
        #     self.compute_Faulty_sensors_mean_Values_with_Noise()

        if not hasattr(self, "sensorMeanValuesHealthy_Noise"):
            self.sensorMeanValuesHealthy_Noise = self.healthyExperiment.compute_Noise_Mean_dict()
        if not hasattr(self, "sensorMeanValuesFaulty_Noise"):
            self.sensorMeanValuesFaulty_Noise = self.faultyExperiment.compute_Noise_Mean_dict()
        
        self.differential_scaled_Mean_Values_without_Noise = {}
        self.differential_scaled_Mean_Values_with_Noise = {}
        for sensorName in self.sensorMeanValuesFaulty:
            faulty = self.faultyExperiment.physic_mean_value_dict_scaled_to_current[sensorName] - self.sensorMeanValuesFaulty_Noise[sensorName]
            healhy = self.healthyExperiment.physic_mean_value_dict_scaled_to_current[sensorName] - self.sensorMeanValuesHealthy_Noise[sensorName]
            differntialValue = faulty - healhy
            self.differential_scaled_Mean_Values_without_Noise.update({sensorName: differntialValue})

    def compute_Differential_Mean_valeus_with_Noise(self):    
        """Compute differential field including noise: (10 A - (-10 A))/2"""
        if not hasattr(self, "sensorMeanValuesHealthy"):
            self.compute_Healthy_sensors_mean_Values_with_Noise()
        if not hasattr(self, "sensorMeanValuesFaulty"):
            self.compute_Faulty_sensors_mean_Values_with_Noise()
        
        self.differential_Mean_Values_with_Noise = {}

        for sensorName in self.sensorMeanValuesFaulty:
            differntialValue = (self.sensorMeanValuesFaulty[sensorName] - self.sensorMeanValuesHealthy[sensorName])/2
            self.differential_Mean_Values_with_Noise.update({sensorName: differntialValue})

    def get_Sensor_positions_XY(self) -> dict:
        self.sensorPositions = {}
        for sensor in self.sensorsOfInterest:
            position = self.healthyExperiment.dataMeasurement.get_Sensor_Position_By_name(sensor)
            for key, value in position.items():
                self.sensorPositions[key] = value
        return self.sensorPositions
        
    def get_Mean_current_Faulty_Measurement(self) -> float:
        """computes mean of current data from dict for the faulty stack"""
        self.faulty_current = np.array(list(self.faultyExperiment.dataMeasurement.get_Current_data().values())).mean()
        return self.faulty_current

    def get_Mean_current_Healthy_Measurement(self) -> float:
        """computes mean of current data from dict for the healthy stack"""
        self.healthy_current = np.array(list(self.healthyExperiment.dataMeasurement.get_Current_data().values())).mean()
        return self.healthy_current
    
    def get_tensions_Faulty(self) -> dict:
        self.faulty_voltages = self.faultyExperiment.dataMeasurement.get_Voltage_data()
        return self.faulty_voltages
    
    def get_tensions_Healthy(self) -> dict:
        self.healthy_voltages = self.healthyExperiment.dataMeasurement.get_Voltage_data()
        return self.healthy_voltages
    
    def plot_Sensor_Positions_In_Space(self):
        test = self.get_Sensor_positions_XY()
        x = []
        y =[]
        for sensor in self.sensorPositions:
            x.append(test[sensor][0])
            y.append(test[sensor][1])
        plt.scatter(x, y)

    def plot_differential_Field_With_Noise(self):
        """Plot Differential Data for not cleaned data. It is usefull when having two experiments with opposit current flow.
        Then, (10 A - (-10 A))/2 is plotted """
        if not hasattr(self, "differential_Mean_Values_with_Noise"): self.compute_Differential_Mean_valeus_with_Noise()
        fig, ax = plt.subplots()
        ax.plot(self.differential_Mean_Values_with_Noise.keys(), self.differential_Mean_Values_with_Noise.values(), marker = ".")
        plt.xticks(rotation = 90)
        plt.ylabel("B-Field ($\mu$T)")
        # get y-axis limits of the plot
        low, high = plt.ylim()
        # find the new limits
        bound = max(abs(low), abs(high))
        # set new limits
        plt.ylim(-bound, bound)

    def plot_scaled_differential_field(self):
        """Plot Differential Data. Noise will be subtracted and faulty - healthy will be computed. Hence only the error is visible."""
        if not hasattr(self, "differential_scaled_Mean_Values_without_Noise"): self.compute_Differential_Mean_valeus_with_scaled_Current()
        fig, ax = plt.subplots(figsize=set_size())
        ax.plot(self.differential_scaled_Mean_Values_without_Noise.keys(), self.differential_scaled_Mean_Values_without_Noise.values(), marker = ".")
        plt.xticks(rotation = 90)
        plt.ylabel("B-Field ($\mu$T)")
        # get y-axis limits of the plot
        low, high = plt.ylim()
        # find the new limits
        bound = max(abs(low), abs(high))
        # set new limits
        plt.ylim(-bound, bound)

    def plot_differential_Field(self):
        """Plot Differential Data. Noise will be subtracted and faulty - healthy will be computed"""
        if not hasattr(self, "differential_Mean_Values_without_Noise"): self.compute_Differential_Mean_valeus()
        fig, ax = plt.subplots(figsize=set_size())
        ax.plot(self.differential_Mean_Values_without_Noise.keys(), self.differential_Mean_Values_without_Noise.values(), marker = ".")
        plt.xticks(rotation = 90)
        plt.ylabel("B-Field ($\mu$T)")
        # get y-axis limits of the plot
        low, high = plt.ylim()
        # find the new limits
        bound = max(abs(low), abs(high))
        # set new limits
        plt.ylim(-bound, bound)

    def plot_Healthy_And_Faulty_Field(self):
        fig, ax = plt.subplots()
        ax.plot(self.sensorMeanValuesHealthy.keys(), self.sensorMeanValuesHealthy.values(), marker = ".", label = "Healthy")
        ax.plot(self.sensorMeanValuesFaulty.keys(), self.sensorMeanValuesFaulty.values(), marker = ".", label = "Faulty")
        plt.legend()
        plt.xticks(rotation = 90)
        plt.ylabel("B-Field ($\mu$T)")
        # get y-axis limits of the plot
        low, high = plt.ylim()
        # find the new limits
        bound = max(abs(low), abs(high))
        # set new limits
        plt.ylim(-bound, bound)


    def plot_Healthy_And_Faulty_Field_Scaled(self):
        fig, ax = plt.subplots()
        ax.plot(self.healthyExperiment.physic_mean_value_dict_scaled_to_current.keys(), self.healthyExperiment.physic_mean_value_dict_scaled_to_current.values(), marker = ".", label = "Healthy")
        ax.plot(self.faultyExperiment.physic_mean_value_dict_scaled_to_current.keys(), self.faultyExperiment.physic_mean_value_dict_scaled_to_current.values(), marker = ".", label = "Faulty")
        plt.legend()
        plt.xticks(rotation = 90)
        plt.ylabel("B-Field ($\mu$T)")
        # get y-axis limits of the plotf
        low, high = plt.ylim()
        # find the new limits
        bound = max(abs(low), abs(high))
        # set new limits
        plt.ylim(-bound, bound)


    def save_in_txt_DiffField_in_muT(self):
        """Saves diff field data as txt file in micro Tesla!"""
        positions = list(self.sensorPositions.values()) 
        field = list(self.differential_Mean_Values_without_Noise.values())

        for i in range(len(positions)):
            if i < len(field):
                positions[i].append(field[i])

        df = pd.DataFrame(positions)
        df.to_csv(self.faultyExperiment.bFieldPath + "SensorPositionsWithFieldsInmuT.txt", index=False, sep = "	",header=None)
    
    

    def save_in_txt_Field_in_T(self, experiment: DynamicExperiment):
        """Saves field data as txt file in Tesla!"""
        positions = list(self.sensorPositions.values()) 
        field = list(experiment.compute_Physic_Mean_minus_Noise_mean_Values().values())

        for i in range(len(positions)):
            if i < len(field):
                positions[i].append(field[i]*1E-6)

        df = pd.DataFrame(positions)
        df.to_csv(experiment.bFieldPath + "SensorPositionsWithFieldsInT.txt", index=False, sep = "	",header=None)

    def save_in_txt_DiffField_in_T(self):
        """Saves data as txt file in Tesla!"""
        positions = list(self.sensorPositions.values()) 
        field = list(self.differential_Mean_Values_without_Noise.values())

        for i in range(len(positions)):
            if i < len(field):
                positions[i].append(field[i]*1E-6)

        df = pd.DataFrame(positions)
        df.to_csv(self.faultyExperiment.bFieldPath + "SensorPositionsWithFieldsInT.txt", index=False, sep = "	",header=None)

    def save_mean_faulty_Voltage_in_txt_in_V(self, name: list):
        meanValues = np.zeros(len(name))
        n = 0
        for i in range(len(name)):
            if name[i] in self.faulty_voltages.keys():
                meanValues[i] = mean(self.faulty_voltages[name[i]])
        meanValues.tofile(self.faultyExperiment.bFieldPath + "Us.txt",  sep = '\n')

    def save_mean_healthy_Voltage_in_txt_in_V(self, name: list):
        meanValues = np.zeros(len(name))
        n = 0
        for i in range(len(name)):
            if name[i] in self.healthy_voltages.keys():
                meanValues[i] = mean(self.healthy_voltages[name[i]])
        meanValues.tofile(self.healthyExperiment.bFieldPath + "Us.txt",  sep = '\n')

    def save_mean_faulty_current_in_txt_in_A(self):
        meanvalue = np.zeros(1)
        meanvalue[0] = np.array(list(self.faultyExperiment.dataMeasurement.get_Current_data().values())).mean()
        meanvalue.tofile(self.faultyExperiment.bFieldPath + "Is.txt",  sep = '\n')

    def save_mean_healthy_current_in_txt_in_A(self):
        meanvalue = np.zeros(1)
        meanvalue[0] = np.array(list(self.healthyExperiment.dataMeasurement.get_Current_data().values())).mean()
        meanvalue.tofile(self.healthyExperiment.bFieldPath + "Is.txt",  sep = '\n')
    
    
    
    

    