from django.contrib.auth.backends import BaseBackend
from .models import Profile,Medicament,Maladie
import openpyxl


class IDAuthenticationBackend(BaseBackend):
    def authenticate(self, request, id=None, password=None):
        try:
            user = Profile.objects.get(id=id)
            if user.check_password(password):
                return user
        except Profile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:
            return None


def get_medicaments_data():
    # med = Medicament.objects.all()
    # med.delete()
    workbook = openpyxl.load_workbook('./api/nomenclature2023.xlsx')
    
    start_row =14
    end_row = 4355 
    
    sheet = workbook.active
    for i in range(start_row,end_row):
        print(sheet[f'E{i}'].value)
        Medicament.objects.get_or_create(name=sheet[f'E{i}'].value)


def add_maladies_data():
    maladie_donnees = [
    {'name': 'Grippe', 'is_chronic': False, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'Rhume', 'is_chronic': False, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'COVID-19', 'is_chronic': False, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'Varicelle', 'is_chronic': False, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'Oreillons', 'is_chronic': False, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'Rougeole', 'is_chronic': False, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'Hépatite', 'is_chronic': True, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'Malaria', 'is_chronic': False, 'maladie_type': 'Parasitic', 'allergie': False},
    {'name': 'Tuberculose', 'is_chronic': True, 'maladie_type': 'Bacterial', 'allergie': False},
    {'name': 'Pneumonie', 'is_chronic': False, 'maladie_type': 'Bacterial', 'allergie': False},
    {'name': 'Bronchite', 'is_chronic': True, 'maladie_type': 'Bacterial', 'allergie': False},
    {'name': 'Asthme', 'is_chronic': True, 'maladie_type': 'Chronic', 'allergie': True},
    {'name': 'Diabète', 'is_chronic': True, 'maladie_type': 'Chronic', 'allergie': False},
    {'name': 'Hypertension', 'is_chronic': True, 'maladie_type': 'Chronic', 'allergie': False},
    {'name': 'SIDA', 'is_chronic': True, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'Cancer du poumon', 'is_chronic': True, 'maladie_type': 'Cancer', 'allergie': False},
    {'name': 'Cancer du sein', 'is_chronic': True, 'maladie_type': 'Cancer', 'allergie': False},
    {'name': 'Leucémie', 'is_chronic': True, 'maladie_type': 'Cancer', 'allergie': False},
    {'name': 'Lupus', 'is_chronic': True, 'maladie_type': 'Autoimmune', 'allergie': False},
    {'name': 'Arthrite', 'is_chronic': True, 'maladie_type': 'Autoimmune', 'allergie': False},
    {'name': 'Insuffisance cardiaque', 'is_chronic': True, 'maladie_type': 'Chronic', 'allergie': False},
    {'name': 'Alzheimer', 'is_chronic': True, 'maladie_type': 'Neurological', 'allergie': False},
    {'name': 'Parkinson', 'is_chronic': True, 'maladie_type': 'Neurological', 'allergie': False},
    {'name': 'Sclérose en plaques', 'is_chronic': True, 'maladie_type': 'Neurological', 'allergie': False},
    {'name': 'Migraine', 'is_chronic': True, 'maladie_type': 'Neurological', 'allergie': False},
    {'name': 'Sinusite', 'is_chronic': False, 'maladie_type': 'Bacterial', 'allergie': False},
    {'name': 'Gastro-entérite', 'is_chronic': False, 'maladie_type': 'Bacterial', 'allergie': False},
    {'name': 'Ulcer', 'is_chronic': False, 'maladie_type': 'Chronic', 'allergie': False},
    {'name': 'Anémie', 'is_chronic': True, 'maladie_type': 'Chronic', 'allergie': False},
    {'name': 'Choléra', 'is_chronic': False, 'maladie_type': 'Bacterial', 'allergie': False},
    {'name': 'Dengue', 'is_chronic': False, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'Ebola', 'is_chronic': False, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'Zika', 'is_chronic': False, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'HIV', 'is_chronic': True, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'H1N1', 'is_chronic': False, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'Grippe aviaire', 'is_chronic': False, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'Méningite', 'is_chronic': False, 'maladie_type': 'Bacterial', 'allergie': False},
    {'name': 'Syphilis', 'is_chronic': False, 'maladie_type': 'Bacterial', 'allergie': False},
    {'name': 'Gonorrhée', 'is_chronic': False, 'maladie_type': 'Bacterial', 'allergie': False},
    {'name': 'Chlamydia', 'is_chronic': False, 'maladie_type': 'Bacterial', 'allergie': False},
    {'name': 'Herpès', 'is_chronic': True, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'Maladie de Lyme', 'is_chronic': False, 'maladie_type': 'Bacterial', 'allergie': False},
    {'name': 'Paludisme', 'is_chronic': False, 'maladie_type': 'Parasitic', 'allergie': False},
    {'name': 'Coqueluche', 'is_chronic': False, 'maladie_type': 'Bacterial', 'allergie': False},
    {'name': 'Typhoïde', 'is_chronic': False, 'maladie_type': 'Bacterial', 'allergie': False},
    {'name': 'Rage', 'is_chronic': False, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'Tétanos', 'is_chronic': False, 'maladie_type': 'Bacterial', 'allergie': False},
    {'name': 'Polio', 'is_chronic': False, 'maladie_type': 'Viral', 'allergie': False},
    {'name': 'Diphtérie', 'is_chronic': False, 'maladie_type': 'Bacterial', 'allergie': False}
]
    
    for m in maladie_donnees:
        maladie = Maladie.objects.create(name=m['name'],isChronic=m['is_chronic'],maladie_type=m['maladie_type'],allergie=m['allergie'])
        maladie.save()