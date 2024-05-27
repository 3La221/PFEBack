from enum import Enum





class TypeMaladie(Enum):
    CARDIOVASCULAIRE = "Maladie cardiovasculaire"
    RESPIRATOIRE = "Maladie respiratoire"
    INFECTIEUSE = "Maladie infectieuse"
    AUTOIMMUNE = "Maladie auto-immune"
    MENTALE = "Maladie mentale"
    GENETIQUE = "Maladie génétique"
    CANCER = "Cancer"
    METABOLIQUE = "Trouble métabolique"
    NEUROLOGIQUE = "Trouble neurologique"
    AUTRE = "Autre"

class BloodType(Enum):
    A_POSITIVE = 'A+'
    A_NEGATIVE = 'A-'
    B_POSITIVE = 'B+'
    B_NEGATIVE = 'B-'
    AB_POSITIVE = 'AB+'
    AB_NEGATIVE = 'AB-'
    O_POSITIVE = 'O+'
    O_NEGATIVE = 'O-'

class Gender(Enum):
    MALE = 'Male'
    FEMALE = 'Female'

class Specialite(Enum):
    CARDIOLOGIE = 'Cardiologie'
    DERMATOLOGIE = 'Dermatologie'
    GASTRO_ENTEROLOGIE = 'Gastro-entérologie'
    NEUROLOGIE = 'Neurologie'
    PEDIATRIE = 'Pédiatrie'
    PSYCHIATRIE = 'Psychiatrie'
    RADIOLOGIE = 'Radiologie'
    CHIRURGIE = 'Chirurgie'
    AUTRE = 'Autre'


class TypeRadiologie(Enum):
    RADIOGRAPHIE = "Radiographie"
    SCAN = "Tomodensitométrie (TDM)"
    IRM = "Imagerie par Résonance Magnétique (IRM)"
    TEP = "Tomographie par Émission de Positons (TEP)"
    ÉCHOGRAPHIE = "Échographie"
    MAMMOGRAPHIE = "Mammographie"
    FLUOROSCOPIE = "Fluoroscopie"
    MÉDECINE_NUCLÉAIRE = "Imagerie en Médecine Nucléaire"
    AUTRE = "Autre"


class TypeOperation(Enum):
    CHIRURGIE_CARDIAQUE = "Chirurgie cardiaque"
    CHIRURGIE_ORTHOPEDIQUE = "Chirurgie orthopédique"
    CHIRURGIE_ESTHETIQUE = "Chirurgie esthétique"
    CHIRURGIE_DIGESTIVE = "Chirurgie digestive"
    CHIRURGIE_VASCULAIRE = "Chirurgie vasculaire"
    CHIRURGIE_NEUROLOGIQUE = "Chirurgie neurologique"
    CHIRURGIE_UROLOGIQUE = "Chirurgie urologique"
    CHIRURGIE_GYNECOLOGIQUE = "Chirurgie gynécologique"
    CHIRURGIE_THORACIQUE = "Chirurgie thoracique"
    CHIRURGIE_OPHTALMOLOGIQUE = "Chirurgie ophtalmologique"
    AUTRE = "Autre"


class AnalyseMedicale(Enum):
    HEMATOLOGIE = "Hématologie"
    BIOCHIMIE = "Biochimie"
    MICROBIOLOGIE = "Microbiologie"
    IMMUNOLOGIE = "Immunologie"
    GENETIQUE = "Génétique"
    RADIOLOGIE = "Radiologie"
    ANATOMOPATHOLOGIE = "Anatomopathologie"
    CYTOLOGIE = "Cytologie"
    VIROLOGIE = "Virologie"
    PARASITOLOGIE = "Parasitologie"
    TOXICOLOGIE = "Toxicologie"

class TypeDoc(Enum):
    RADIO = "Radio",
    ANALYSE = "Analyse",
    
class SituationMatrimoniale(Enum):
    CELIBATAIRE = "Célibataire"
    MARIE = "Marié(e)"
    DIVORCE = "Divorcé(e)"
    VEUF = "Veuf/Veuve"
