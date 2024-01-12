from dataclasses import dataclass


@dataclass
class ExperimentDescriptionDataClass:
    """Use this class to save your different experiment descriptions and have a cleaner note book"""
    scaleCurrentTo: float
    noiseBFieldPath: str
    fileNameNoiseAV: str
    fileNameNoiseCenter: str
    fileNameNoiseAR: str

    bFieldPath: str
    fileNameAV: str
    fileNameC: str
    fileNameAR: str

    measuredCurrent: float
    measurementName: str
    measurementDate: str
    measurementYear: int


RefExperiment20170207 = ExperimentDescriptionDataClass(100,
                                                r'C:\Users\freiseml\Nextcloud2\00-These Leo\99-Travaux Lyes\Mesures CEA_2D\07_02_2017\Caract_Bruit\\',
                                                "champ_Aux_on_PD.lvm",
                                                "champ_Aux_on_PC.lvm",
                                                "champ_Aux_on_PG.lvm",
                                                r'C:\Users\freiseml\Nextcloud2\00-These Leo\99-Travaux Lyes\Mesures CEA_2D\07_02_2017\Stochio\\',
                                                'champ_I100A_PD.lvm',
                                                'champ_I100A_PC.lvm',
                                                "champ_I100A_PG.lvm",
                                                100,
                                                "Reference 100 A",
                                                "07.02.2017",
                                                2017)



# print(RefExperiment20170207.measurementYear)



# scaleTo = 100

# noiseBFieldPath = r'C:\Users\freiseml\Nextcloud2\00-These Leo\99-Travaux Lyes\Mesures CEA_2D\07_02_2017\Caract_Bruit\\'
# filenamenoiseAV = "champ_Aux_on_PD.lvm"
# filenamenoiseCenter = "champ_Aux_on_PC.lvm"
# filenamenoiseAR = "champ_Aux_on_PG.lvm"

# bFieldPath = r'C:\Users\freiseml\Nextcloud2\00-These Leo\99-Travaux Lyes\Mesures CEA_2D\07_02_2017\Stochio\\'
# filenameAV = 'champ_I100A_PD.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
# filenameC = 'champ_I100A_PC.lvm'                  ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!
# filenameAR = 'champ_I100A_PG.lvm'                     ###!!!!!!!!-----------> Change here <-----------!!!!!!!!!!!!!!!!

# measuredCurrent = 100
# measurementName = "Reference 100 A"
# measurementDate = "07.02.2017"
# measurementYear = 2017