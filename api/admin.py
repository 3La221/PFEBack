from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Consultation)
admin.site.register(Labo)
admin.site.register(DocumentMedicale)
admin.site.register(MedicamentDetails)
admin.site.register(Medicament)
admin.site.register(Maladie)
admin.site.register(Allergie)