from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import uuid
from . managers import ProfileManager
from .enums import *
import qrcode
from django.contrib.auth.hashers import make_password
from PIL import Image



def generate_short_id():
    return str(uuid.uuid4())[:8]

class Profile(AbstractUser):
    username = None
    id = models.CharField(primary_key=True, default=generate_short_id, editable=False, max_length=8)
    email = models.EmailField(max_length=255, unique=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    
    USERNAME_FIELD = "email"
    
    PASSWORD_FIELD = 'password'

    REQUIRED_FIELDS = []
    
    objects = ProfileManager()
    
    
class Patient(Profile):
    carte_id = models.CharField(max_length=255, unique=True,blank=True,null=True)
    img = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    birth_date = models.DateField(null = True)
    numero_tel = models.CharField(max_length=20, blank=True, null=True)
    blood_type = models.CharField(max_length=3, choices=[(tag.value, tag.name) for tag in BloodType],null=True , blank = True)
    gender = models.CharField(max_length=10, choices=[(tag.value, tag.name) for tag in Gender],null=True , blank = True)
    emergency_number = models.CharField(max_length=20, blank=True, null=True)
    married = models.CharField(max_length=20, choices= [(tag.value , tag.name) for tag in SituationMatrimoniale ] , null =True , blank = True , default= SituationMatrimoniale.CELIBATAIRE)
    nbr_children = models.IntegerField(default=0)
    antecedents = models.ManyToManyField("Antecedent",blank=True,related_name="antecedents")
    allergies = models.ManyToManyField("Allergie",blank=True)
    etat_carte = models.IntegerField(default=0) # 0 non demande / 1 demande / 2 donne
    
    @property
    def can_demande(self):
        return self.etat_carte == 0
    
    
    REQUIRED_FIELDS = ["carte_id"]

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        
    def __str__(self) -> str:
        return  f'{self.first_name} {self.last_name}'
    
    
    def save(self, *args, **kwargs):
        data = f"{self.id}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((200,200))
        background = Image.open('./media/1.jpg')
        qr_position = (background.width - img.width - 150, background.height - img.height - 200)  # Adjust the position as needed
        background.paste(img, qr_position)
        
        
        
        background_path =f"./media/{self.id}CARD.png"
        background.save(background_path)
        
        
        
        
        super().save(*args, **kwargs)

class Doctor(Profile):
    carte_id = models.CharField(max_length=255, unique=True)
    valide = models.BooleanField(default=False)
    certeficat = models.ImageField(upload_to='certeficats/', blank=True, null=True)
    labo_number  = models.CharField(max_length=10, blank=True, null=True)
    specialite = models.CharField(max_length=50, choices=[(tag.value, tag.name) for tag in Specialite] , default = Specialite.AUTRE)
    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
        
    def __str__(self) -> str:
        return  f'Dr.{self.first_name} {self.last_name}'
    

class Labo(Profile):
    name = models.CharField(max_length=100, blank=True, null=True)
    certeficat = models.ImageField(upload_to='certeficats/', blank=True, null=True)
    valide = models.BooleanField(default=False)
    labo_number  = models.CharField(max_length=10, blank=True, null=True)
    
    
    class Meta:
        verbose_name = "Labo"
        verbose_name_plural = "Labos"
        
    def __str__(self) -> str:
        return  f'{self.name} Labo'

class Centre(Labo):
    def __str__(self) -> str:
        return  f'{self.name} Centre'
    
    

class Antecedent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100,blank=True,null= True)
    membre = models.CharField(max_length=100,blank=True,null= True)
    cateogry = models.CharField(max_length=80,blank=True,null= True)
    
    def __str__(self) -> str:
        return self.name

class Consultation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(default=timezone.now)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name ="consultations")
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name ="consultations")
    note = models.TextField(blank=True, null = True)
    maladie = models.OneToOneField("MaladieP",related_name ="consultation" ,
                                on_delete=models.CASCADE,null=True,blank=True)
    
    
    def __str__(self) -> str:
        return f'{self.patient} - {self.doctor} - {self.date} Consultaion'


class MaladieP(models.Model):
    maladie = models.ForeignKey("Maladie",on_delete=models.CASCADE)
    affiche = models.BooleanField(default=True)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name ="maladies",null=True ,blank=True)
    
    def __str__(self) -> str:
        return f'{self.maladie} {self.patient}'
    


class Maladie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100,blank=True,null= True)
    isChronic = models.BooleanField(default=False)
    maladie_type = models.CharField(max_length=80,choices=[(tag.name,tag.value) for tag in TypeMaladie])
    
    def __str__(self) -> str:
        return self.name
    
class Allergie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100,blank=True,null= True,unique=True)
    affiche = models.BooleanField(default=True)
    def __str__(self) -> str:
        return self.name

class Medicament(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)    
    
    def __str__(self) -> str:
        return self.name
    
class MedicamentDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qte = models.IntegerField(default=1)
    duree = models.IntegerField(default=7)
    # isChronic = models.BooleanField(default=False)
    medicament = models.ForeignKey(Medicament,null=True,blank=True , on_delete=models.CASCADE)
    consultation = models.ForeignKey(Consultation , on_delete = models.CASCADE , null = True , blank =True,related_name="medicaments")
    def __str__(self) -> str:
        return f'{self.medicament} - {self.consultation}'

class DocumentMedicale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, blank=True, null=True)
    radio_type = models.CharField(max_length=50 , blank=True, null=True)
    radio_category = models.CharField(max_length=50,blank=True, null=True)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name ="documents")
    # labo = models.ForeignKey(Labo,on_delete=models.CASCADE,related_name ="documents",null=True,blank=True)
    doctor = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name ="documents_as_medic",null=True,blank=True)
    document = models.FileField(upload_to='documents/',null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)
    note = models.TextField(null=True , blank =True)
    demande = models.BooleanField(default=True)
    type_doc = models.CharField(max_length=5,default="R")
        
    
    def __str__(self) -> str:
        return f'{self.nom} - {self.patient}'
    

