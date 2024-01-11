from dataclasses import asdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from collectAllMeasureDataInOneFile import*
from ExperimentClass import*
import seaborn as sns
from InvestigationClass import*
from thesis_general_imports import*


scaleTo = 48

## Pile Saine 2020_01_24 50 A #####################################################################################
noiseBFieldPath = r'C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_24\Bruit\\'
filenamenoiseAV = "Ref_Bruit_Ambiant_Aux_On_AV_az.lvm"
filenamenoiseCenter = "Ref_Bruit_Ambiant_Aux_On_Centre_az.lvm"
filenamenoiseAR = "Ref_Bruit_Ambiant_Aux_On_AR_az.lvm"

bFieldPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_24\Pile_Saine\\"
filenameAR = 'Ref_Pile_I48A_AR.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameC = 'Ref_Pile_I48A_Centre.lvm'                  ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameAV = 'Ref_Pile_I48A_AV.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
measuredCurrent = 48


# Ref50AExperiment2020_01_24 = Experiment(2020, "Reference", "24.01.2020", measuredCurrent, scaleTo, noiseBFieldPath, filenamenoiseAV, filenamenoiseCenter,filenamenoiseAR, bFieldPath, filenameAV, filenameC, filenameAR)
# RefExperiment2020_01_24.calculateCleanFields()


## Pile Saine 2020_01_24 100 A #####################################################################################
noiseBFieldPath = r'C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_24\Bruit\\'
filenamenoiseAV = "Ref_Bruit_Ambiant_Aux_On_AV_az.lvm"
filenamenoiseCenter = "Ref_Bruit_Ambiant_Aux_On_Centre_az.lvm"
filenamenoiseAR = "Ref_Bruit_Ambiant_Aux_On_AR_az.lvm"

bFieldPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_24\Pile_Saine\\"
filenameAR = 'Ref_Pile_I100A_AR.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameC = 'Ref_Pile_I100A_Centre.lvm'                  ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameAV = 'Ref_Pile_I100A_AV.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
measuredCurrent = 100


Ref100AExperiment2020_01_24 = Experiment(2020, "Reference_100A", "24.01.2020", measuredCurrent, scaleTo, noiseBFieldPath, filenamenoiseAV, filenamenoiseCenter,filenamenoiseAR, bFieldPath, filenameAV, filenameC, filenameAR)


## Pile Saine 48 A 2020_01_22 #####################################################################################
noiseBFieldPath = r'C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_22\Bruit\\'
filenamenoiseAV = "Ref_Bruit_Ambiant_FM_Aux_On_AV_2.lvm"
filenamenoiseCenter = "Ref_Bruit_Ambiant_FM_Aux_On_Centre_1.lvm"
filenamenoiseAR = "Ref_Bruit_Ambiant_FM_Aux_On_AR_1.lvm"

bFieldPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_22\Pile Saine\Def_PileSaine\\"
filenameAR = 'Ref_Pile_I48A_AR.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameC = 'Ref_Pile_I48A_Centre.lvm'                  ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameAV = 'Ref_Pile_I48A_AV.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
measuredCurrent = 48

RefExperiment48A2020_01_22 = Experiment(2020, "Reference 48A", "22.01.2020", measuredCurrent, scaleTo, noiseBFieldPath, filenamenoiseAV, filenamenoiseCenter,filenamenoiseAR, bFieldPath, filenameAV, filenameC, filenameAR)
# RefExperiment2020_01_22.calculateCleanFields()


## Pile Saine 2021_07_28 100 A #####################################################################################
noiseBFieldPath = r'C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesure_2021\2021_07_28\Bruitmesure\\'
filenamenoiseAV = "Banc_on_sans_courant_Idc0A_Iac_0A_f0Hz_AV.lvm"
filenamenoiseCenter = "Banc_on_sans_courant_Idc0A_Iac_0A_f0Hz_CENTRE.lvm"
filenamenoiseAR = "Banc_on_sans_courant_Idc0A_Iac_0A_f0Hz_AR.lvm"

bFieldPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesure_2021\2021_07_28\Pile_saine\\"
filenameAR = 'Pile_saine_Idc100A_Iac_10A_f0Hz_AR.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameC = 'Pile_saine_Idc100A_Iac_10A_f0Hz_CENTRE.lvm'                  ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameAV = 'Pile_saine_Idc100A_Iac_10A_f0Hz_AV.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
measuredCurrent = 100


# Ref100AExperiment2021_07_28 = Experiment(2021, "Reference 100A", "28.07.2021", measuredCurrent, scaleTo, noiseBFieldPath, filenamenoiseAV, filenamenoiseCenter,filenamenoiseAR, bFieldPath, filenameAV, filenameC, filenameAR)



## Humidity 2020_01_24 50 A #####################################################################################
noiseBFieldPath = r'C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_24\Bruit\\'
filenamenoiseAV = "Ref_Bruit_Ambiant_Aux_On_AV_az.lvm"
filenamenoiseCenter = "Ref_Bruit_Ambiant_Aux_On_Centre_az.lvm"
filenamenoiseAR = "Ref_Bruit_Ambiant_Aux_On_AR_az.lvm"

bFieldPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_24\Humidite\\"
filenameAR = 'Def_Hum30_I50A_AR.lvm'                    ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameC = 'Def_Hum30_I50A_Centre.lvm'                 ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameAV = 'Def_Hum30_I50A_AV.lvm'                    ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
measuredCurrent = 50


# Humidity50AExperiment2020_01_24 = Experiment(2020, "Humidity 30 %", "24.01.2020", measuredCurrent, scaleTo, noiseBFieldPath, filenamenoiseAV, filenamenoiseCenter,filenamenoiseAR, bFieldPath, filenameAV, filenameC, filenameAR)
# HumidityExperiment2020_01_24.calculateCleanFields()

## Humidity 2020_01_24 50 A #####################################################################################
noiseBFieldPath = r'C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_24\Bruit\\'
filenamenoiseAV = "Ref_Bruit_Ambiant_Aux_On_AV_az.lvm"
filenamenoiseCenter = "Ref_Bruit_Ambiant_Aux_On_Centre_az.lvm"
filenamenoiseAR = "Ref_Bruit_Ambiant_Aux_On_AR_az.lvm"

bFieldPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_24\Humidite\Autres\\"
filenameAR = 'Def_Hum30_I100A_AR.lvm'                    ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameC = 'Def_Hum30_I100A_Centre.lvm'                 ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameAV = 'Def_Hum30_I100A_AV.lvm'                    ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
measuredCurrent = 100


# Humidity100AExperiment2020_01_24 = Experiment(2020, "100A Humidity 30 %", "24.01.2020", measuredCurrent, scaleTo, noiseBFieldPath, filenamenoiseAV, filenamenoiseCenter,filenamenoiseAR, bFieldPath, filenameAV, filenameC, filenameAR)

## Pile Saine 2020_01_22 110 A #####################################################################################
noiseBFieldPath = r'C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_22\Bruit\\'
filenamenoiseAV = "Ref_Bruit_Amb_Aux_ON_AV.lvm"
filenamenoiseCenter = "Ref_Bruit_Amb_Aux_ON_Centre.lvm"
filenamenoiseAR = "Ref_Bruit_Amb_Aux_ON_AR.lvm"

bFieldPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_22\Pile Saine\Def_PileSaine\\"
filenameAR = 'Ref_Pile_I110A_AR.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameC = 'Ref_Pile_I110A_Centre.lvm'                  ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameAV = 'Ref_Pile_I110A_AV.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
measuredCurrent = 110


# Ref110AExperiment2020_01_22 = Experiment(2020, "Reference_110A", "22.01.2020", measuredCurrent, scaleTo, noiseBFieldPath, filenamenoiseAV, filenamenoiseCenter,filenamenoiseAR, bFieldPath, filenameAV, filenameC, filenameAR)


## Stoichio 100 A 22.01.2020 #####################################################################################
noiseBFieldPath = r'C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_22\Bruit\\'
filenamenoiseAV = "Ref_Bruit_Ambiant_FM_Aux_On_AV_2.lvm"
filenamenoiseCenter = "Ref_Bruit_Ambiant_FM_Aux_On_Centre_1.lvm"
filenamenoiseAR = "Ref_Bruit_Ambiant_FM_Aux_On_AR_1.lvm"


bFieldPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_22\Stochio_1_5\\"
filenameAR = 'Def_Stoch1_5_I100A_AR.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameC = 'Def_Stoch1_5_I100A_Centre.lvm'                 ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameAV = 'Def_Stoch1_5_I100A_AV.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
measuredCurrent = 100

# StoichiometryExperiment100A2020_01_22 = Experiment(2020, "Stoichiometry 1.5 100A", "22.01.2020", measuredCurrent, scaleTo, noiseBFieldPath, filenamenoiseAV, filenamenoiseCenter,filenamenoiseAR, bFieldPath, filenameAV, filenameC, filenameAR)

## Stoichio 48 A 22.01.2020 #####################################################################################
noiseBFieldPath = r'C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_22\Bruit\\'
filenamenoiseAV = "Ref_Bruit_Ambiant_FM_Aux_On_AV_2.lvm"
filenamenoiseCenter = "Ref_Bruit_Ambiant_FM_Aux_On_Centre_1.lvm"
filenamenoiseAR = "Ref_Bruit_Ambiant_FM_Aux_On_AR_1.lvm"


bFieldPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesures 2020\CEA\2020_01_22\Stochio_1_5\Def_Stoch_1_5\\"
filenameAR = 'Def_Stoch1_5_I48A_AR.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameC = 'Def_Stoch1_5_I48A_Centre.lvm'                 ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameAV = 'Def_Stoch1_5_I48A_AV.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
measuredCurrent = 51.32


StoichiometryExperiment48A2020_01_22 = Experiment(2020, "Stoichiometry 1.5", "22.01.2020", measuredCurrent, scaleTo, noiseBFieldPath, filenamenoiseAV, filenamenoiseCenter,filenamenoiseAR, bFieldPath, filenameAV, filenameC, filenameAR)


## 100A Humidity 20 % 2021_07_28 100 A #####################################################################################
noiseBFieldPath = r'C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesure_2021\2021_07_28\Bruitmesure\\'
filenamenoiseAV = "Banc_on_sans_courant_Idc0A_Iac_0A_f0Hz_AV.lvm"
filenamenoiseCenter = "Banc_on_sans_courant_Idc0A_Iac_0A_f0Hz_CENTRE.lvm"
filenamenoiseAR = "Banc_on_sans_courant_Idc0A_Iac_0A_f0Hz_AR.lvm"

bFieldPath = r"C:\Users\freiseml\Nextcloud\01_France\04_Stage\00-Travail\03-PAC\Mesure_2021\2021_07_28\Defaut_humidite\\"
filenameAR = 'RH20%_Idc100A_Iac_10A_f0Hz_AR.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameC = 'RH20%_Idc100A_Iac_10A_f0Hz_CENTRE.lvm'                  ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
filenameAV = 'Rh20%_Idc100A_Iac_10A_f0Hz_AV.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
measuredCurrent = 100


# Humidity100AExperiment2021_07_28 = Experiment(2021, "100A Humidity 20 %", "28.07.2021", measuredCurrent, scaleTo, noiseBFieldPath, filenamenoiseAV, filenamenoiseCenter,filenamenoiseAR, bFieldPath, filenameAV, filenameC, filenameAR)



# sensorsOfInterestPlane1 = np.linspace(0, 29, 30, dtype=int)
sensorsOfInterest = np.linspace(60, 89, 30, dtype=int)
# sensorsOfInterest = np.append(sensorsOfInterestPlane1, sensorsOfInterestPlane2)

# TestInvestigation = Investigation(Ref100AExperiment2021_07_28, Humidity100AExperiment2021_07_28, sensorsOfInterest)

TestInvestigation = Investigation(RefExperiment48A2020_01_22, StoichiometryExperiment48A2020_01_22, sensorsOfInterest)