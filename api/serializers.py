from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from rest_framework import generics


# Create serializers for each class
class PatientSerializer(ModelSerializer):
    
    
    

    class Meta:
        model = Patient
        fields ='__all__'
        
    
        
    def create(self, validated_data):
        user = Patient.objects.create_user(**validated_data)
        return user

class MaladieDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maladie
        fields = ['id','name','isChronic','maladie_type']

class AllergieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergie
        fields = ['id','name','affiche']
        
class MedicamentDetailsSerializer(ModelSerializer):
    class Meta:
        model = MedicamentDetails
        fields = ['medicament','qte','duree']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            medicament = Medicament.objects.get(id=instance.medicament.id)
            representation['medicament'] = medicament.name
        except:
            pass
        return representation
        
class MedicamentSerializer(ModelSerializer):
    class Meta:
        model = Medicament
        fields = '__all__'
        
        
class MaladieSerializer(ModelSerializer):
    class Meta:
        model = Maladie
        fields = '__all__'

# class OrdonanceSerializer(ModelSerializer):
#     medicaments = MedicamentDetailsSerializer(many=True)
    
#     class Meta:
#         model = Ordonance
#         fields = ['medicaments']
    



class MaladieDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maladie
        fields = ['id','name','isChronic','maladie_type']

class MaladiePSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaladieP
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            maladie = Maladie.objects.get(id=instance.maladie.id)
            representation['maladie'] = maladie.name
        except:
            pass
        return representation


class ConsultationSerializer(ModelSerializer):
    # ordonance = OrdonanceSerializer()
    medicaments = MedicamentDetailsSerializer(many=True)
    maladie = MaladiePSerializer()
    class Meta:
        model = Consultation
        fields = ['id','patient','doctor','maladie','note','date','maladie','medicaments']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            doctor = Doctor.objects.get(id=instance.doctor.id)
            representation['doctor'] = f'Dr.{doctor.first_name} {doctor.last_name}'  # Concatenate first_name and last_name
        except:
            pass
        representation['date'] = instance.date.strftime('%Y-%m-%d')
        try :
            maladie = MaladieP.objects.get(id=instance.maladie.id)
            representation['maladie'] = MaladiePSerializer(maladie).data
        except:
            pass
        
        return representation
    
    
    # def update(self, instance, validated_data):
        
    #     print("UPDATTE")

        
    #     print("maladie",maladie)
    #     instance.note = note
    #     maladiep = MaladieP.objects.get(id=maladie["id"])
    #     maladiep.affiche = maladie["affiche"]
    #     maladiep.save()
        
        
    #     for medicament in medicaments:
    #         med = MedicamentDetails.objects.create(consultation = instance , **medicament)
    #         med.save()
        
        
        
            
        
        
    #     return instance
    
    def create(self, validated_data):
        patient = validated_data['patient']
        maladie = validated_data.pop('maladie',{})
        medicaments = validated_data.pop('medicaments',[])
        
        
        consultation = Consultation.objects.create(**validated_data)
        
        
        maladiep = MaladieP.objects.create(maladie=maladie["maladie"],affiche=maladie["affiche"],patient=patient)
        consultation.maladie = maladiep
        consultation.save()
        maladiep.save()
        for medicament in medicaments:
            MedicamentDetails.objects.create(consultation = consultation , **medicament)
    
        
        return consultation
    

class AntecedentSerializer(ModelSerializer):
    class Meta:
        model = Antecedent
        fields = ['id','name','membre','cateogry']
        


class PatientDetailsSerializer(ModelSerializer):
    maladies = serializers.SerializerMethodField()
    antecedents = AntecedentSerializer(many=True)
    radios = serializers.SerializerMethodField()
    analyses = serializers.SerializerMethodField()
    chirurgies = serializers.SerializerMethodField()
    allergies = AllergieSerializer(many=True)
    consultations = ConsultationSerializer(many=True)
    
    
    def get_maladies(self, obj):
        chronic_maladies = obj.maladies.filter(affiche=True)
        return MaladiePSerializer(chronic_maladies, many=True).data
    
    
    def get_chirurgies(self, obj):
        chirurgies = obj.documents.filter(type_doc='C')
        return DocumentMedicaleSerializer(chirurgies, many=True).data
    
    def get_radios(self, obj):
        radios = obj.documents.filter(type_doc='R')
        return DocumentMedicaleSerializer(radios, many=True).data
    
    def get_analyses(self,obj):
        analyses = obj.documents.filter(type_doc='A')
        return DocumentMedicaleSerializer(analyses, many=True).data
    
    
    class Meta:
        model = Patient
        fields = ['id','first_name','last_name','img',
                'carte_id', 'birth_date', 'numero_tel',
                'blood_type', 'gender',
                'emergency_number', 'married', 'maladies','allergies','antecedents',
                'radios',
                'analyses',
                'chirurgies',
                'consultations','nbr_children', 'address'
                
                ]


class PatientInfoSerializer(ModelSerializer):
    maladies = serializers.SerializerMethodField()
    allergies = serializers.SerializerMethodField()

    
    def get_maladies(self, obj):
        chronic_maladies = obj.maladies.filter(affiche=True)
        return MaladiePSerializer(chronic_maladies, many=True).data

    def get_allergies(self, obj):
        affiche_allergies = obj.allergies.filter(affiche=True)
        return AllergieSerializer(affiche_allergies, many=True).data
    
    
    class Meta:
        model = Patient
        fields = ['id','first_name','last_name' , 'birth_date',
                'blood_type', 'gender', 'emergency_number','address','nbr_children',
                'married', 'maladies','allergies']
        


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

    def create(self, validated_data):
        user = Doctor.objects.create_user(
            carte_id=validated_data['carte_id'],
            specialite=validated_data['specialite'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],  # Ensure to handle password hashing
            certeficat=validated_data['certeficat'],
            labo_number = validated_data['labo_number'],
            address = validated_data['address']
        )
        return user

class LaboSerializer(ModelSerializer):
    class Meta:
        model = Labo
        fields = '__all__'

    def create(self, validated_data):
        user = Labo.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],  # Ensure to handle password hashing
            certeficat=validated_data['certeficat'],
            labo_number = validated_data['labo_number'],
            name = validated_data['name'],
            address = validated_data['address']
        )
        return user

class CentreSerializer(ModelSerializer):
    class Meta:
        model = Centre
        fields = '__all__'

    def create(self, validated_data):
        user = Labo.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],  # Ensure to handle password hashing
            certeficat=validated_data['certeficat'],
            labo_number = validated_data['labo_number'],
            name = validated_data['name'],
            address = validated_data['address']
        )
        return user
    
class DoctorInfoSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields =['id','specialite','first_name','last_name']

    def create(self, validated_data):
        user =  Doctor.objects.create_user(**validated_data)
        return user





        



            
class DocumentMedicaleSerializer(ModelSerializer):
    # document = serializers.FileField()

    class Meta:
        model = DocumentMedicale
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        user = Profile.objects.get(id=representation["doctor"])
        if hasattr(user, 'doctor'):
            doctor = Doctor.objects.get(id=representation["doctor"])
            representation['doctor'] = f'Dr.{doctor.first_name} {doctor.last_name}'
        elif hasattr(user, 'labo'):
            labo = Labo.objects.get(id=representation["doctor"])
            representation['doctor'] = f'{labo.name} Labo'
        elif hasattr(user, 'centre'):
            centre = Centre.objects.get(id=representation["doctor"])
            representation['doctor'] = f'{centre.name} Centre'
            
        representation['date'] = instance.date.strftime('%Y-%m-%d')
        

        return representation


class CenterInfoSerializer(ModelSerializer):
    class Meta:
        model = Centre
        fields = ['id','name','labo_number','address','valide','email','certeficat']

class LaboInfoSerializer(ModelSerializer):
    class Meta:
        model = Labo
        fields = ['id','name','labo_number','address','valide','email','certeficat']
        

class DoctorInfoSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id','first_name','last_name','specialite','email','certeficat','valide','carte_id','labo_number','address']
        






