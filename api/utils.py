from django.contrib.auth.backends import BaseBackend
from .models import Profile,Medicament
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
