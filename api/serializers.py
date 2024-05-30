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
        fields = '__all__'
        
class MedicamentSerializer(ModelSerializer):
    class Meta:
        model = Medicament
        fields = '__all__'
        
        
class MaladieSerializer(ModelSerializer):
    class Meta:
        model = Maladie
        fields = '__all__'

class OrdonanceSerializer(ModelSerializer):
    medicaments = MedicamentDetailsSerializer(many=True)
    
    class Meta:
        model = Ordonance
        fields = ['medicaments']
    



class MaladieDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maladie
        fields = ['id','name','isChronic','maladie_type']

class ConsultationSerializer(ModelSerializer):
    ordonance = OrdonanceSerializer()
    class Meta:
        model = Consultation
        fields = ['id','patient','doctor','maladie','note','date','maladie','ordonance']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            doctor = Doctor.objects.get(id=instance.doctor.id)
            representation['doctor'] = f'Dr.{doctor.first_name} {doctor.last_name}'  # Concatenate first_name and last_name
        except:
            pass
        representation['date'] = instance.date.strftime('%Y-%m-%d')
        try :
            maladie = Maladie.objects.get(id=instance.maladie.id)
            representation['maladie'] = MaladieSerializer(maladie).data
        except:
            pass
        
        return representation
    
    
    def create(self, validated_data):
        patient = validated_data['patient']
        doctor = validated_data['doctor']
        maladie = validated_data['maladie']
        ordonance_data = validated_data.pop('ordonance')
        
        
        consultation = Consultation.objects.create(**validated_data)
        
        patient.maladies.add(maladie)
        
        
        ordonance = Ordonance.objects.create(consultaion = consultation)
        medicaments = ordonance_data['medicaments']
        
        for medicament in medicaments:
            MedicamentDetails.objects.create(ordonance = ordonance , **medicament)
    
        
        return consultation

class PatientDetailsSerializer(ModelSerializer):
    maladies = MaladieDSerializer(many=True)
    antecedents = MaladieDSerializer(many=True)
    radios = serializers.SerializerMethodField()
    analyses = serializers.SerializerMethodField()
    chirurgies = serializers.SerializerMethodField()
    allergies = AllergieSerializer(many=True)
    consultations = ConsultationSerializer(many=True)
    
    
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
    antecedents = MaladieDSerializer(many=True)
    maladies = serializers.SerializerMethodField()
    allergies =AllergieSerializer(many=True)

    
    def get_maladies(self, obj):
        chronic_maladies = obj.maladies.filter(isChronic=True)
        return MaladieDSerializer(chronic_maladies, many=True).data

    
    class Meta:
        model = Patient
        fields = ['id','first_name','last_name' ,'carte_id', 'birth_date', 'numero_tel',
                'blood_type', 'gender', 'emergency_number','address','nbr_children',
                'married', 'maladies','antecedents','allergies']
        


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
            certeficat=validated_data['certeficat']
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
            name = validated_data['name']
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
        try:
            doctor = Doctor.objects.get(id=instance.doctor.id)
            representation['doctor'] = f'Dr.{doctor.first_name} {doctor.last_name}'  # Concatenate first_name and last_name
        except:
            pass
        representation['date'] = instance.date.strftime('%Y-%m-%d')
        

        return representation


class LaboInfoSerializer(ModelSerializer):
    class Meta:
        model = Labo
        fields = ['id','name','labo_number','address','valide','email','certeficat']
        

class DoctorInfoSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id','first_name','last_name','specialite','email','certeficat','valide','carte_id']
        
    


# class OrdonanceSerializer(ModelSerializer):
    
#     medicaments = MedicamentDetailsSerializer(many=True)  
#     documents = DocumentMedicaleSerializer(many=True)
    
#     class Meta:
#         model = Ordonance
#         fields = ['documents','medicaments']

#     def create(self, validated_data):
#         medicaments_data = validated_data.pop('medicaments',[])
#         documents_data = validated_data.pop('documents',[])
        
#         ordonance = Ordonance.objects.create(**validated_data)
        
#         for medicament_data in medicaments_data:
#             MedicamentDetails.objects.create(ordonance = ordonance , **medicament_data)
        
        
#         for document in documents_data:
#             DocumentMedicale.objects.create(ordonance = ordonance , **document)        
#         return ordonance

