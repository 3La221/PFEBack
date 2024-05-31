from django.contrib import admin
from .models import *
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if 'password' in form.cleaned_data:
            obj.set_password(form.cleaned_data['password'])
        else:
            if change:  # if this is an update
                obj = Profile.objects.get(id=obj.id)
                obj.password = obj.password
        obj.save()

admin.site.register(Profile, ProfileAdmin)

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Consultation)
admin.site.register(Labo)
admin.site.register(DocumentMedicale)
admin.site.register(MedicamentDetails)
admin.site.register(Medicament)
admin.site.register(Maladie)
admin.site.register(Allergie)
