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

## 100A Ref 2017_02_07 100 A #####################################################################################
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

## 100A Stoichiometry 1.3 2017_02_09 100 A #####################################################################################
Stoichio13Experiment20170209 = ExperimentDescriptionDataClass(100,
                                                r'C:\Users\freiseml\Nextcloud2\00-These Leo\99-Travaux Lyes\Mesures CEA_2D\09_02_2017\Sto2_100A\\',
                                                "bruitPD.lvm",
                                                "bruitPC.lvm",
                                                "bruitPG.lvm",
                                                r"C:\Users\freiseml\Nextcloud2\00-These Leo\99-Travaux Lyes\Mesures CEA_2D\09_02_2017\Sto13_100A\\",
                                                '100 A PD sto air 1,3.lvm',
                                                '100 A PC sto air 1,3-b.lvm',
                                                '100 A PG sto air 1,3.lvm',
                                                100,
                                                "Stoichiometry 1.3 100 A",
                                                "09.02.2017",
                                                2017)

## 100A Stoichiometry 1.5 2017_02_09 100 A #####################################################################################
Stoichio15Experiment20170209 = ExperimentDescriptionDataClass(100,
                                                r'C:\Users\freiseml\Nextcloud2\00-These Leo\99-Travaux Lyes\Mesures CEA_2D\09_02_2017\Sto2_100A\\',
                                                "bruitPD.lvm",
                                                "bruitPC.lvm",
                                                "bruitPG.lvm",
                                                r"C:\Users\freiseml\Nextcloud2\00-These Leo\99-Travaux Lyes\Mesures CEA_2D\09_02_2017\Sto15_100A\\",
                                                '100 A PD sto air 1,5.lvm',
                                                '100 A PC sto air 1,5.lvm',
                                                '100 A PG sto air 1,5.lvm',
                                                100,
                                                "Stoichiometry 1.5 100 A",
                                                "09.02.2017",
                                                2017)

## 100A Stoichiometry 2.0 2017_02_09 100 A #####################################################################################
Stoichio20Experiment20170209 = ExperimentDescriptionDataClass(100,
                                                r'C:\Users\freiseml\Nextcloud2\00-These Leo\99-Travaux Lyes\Mesures CEA_2D\09_02_2017\Sto2_100A\\',
                                                "bruitPD.lvm",
                                                "bruitPC.lvm",
                                                "bruitPG.lvm",
                                                r"C:\Users\freiseml\Nextcloud2\00-These Leo\99-Travaux Lyes\Mesures CEA_2D\09_02_2017\Sto2_100A\\",
                                                '100 A PD.lvm',
                                                '100 A PC.lvm',
                                                '100 A PG.lvm',
                                                100,
                                                "Stoichiometry 2.0 100 A",
                                                "09.02.2017",
                                                2017)

