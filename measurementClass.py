from dataclasses import dataclass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from collectAllMeasureDataInOneFile import*
from ExperimentClass import Experiment as Exp
from thesis_general_imports import*

@dataclass
class MeasurementClass():
    """This Class is used to create for each sensor an information class. So the basic info are given to evaluate between the different sensors. It is not used yet"""
    scaleFactor: float
    meanValueOnEachSensor: float
    medianOnEachSensor: float
    standardDeviation: float
    rawData: np.array