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

class PatientDetailsSerializer(ModelSerializer):

    class Meta:
        model = Patient
        fields = ['id','img' ,'carte_id', 'birth_date', 'numero_tel', 'blood_type', 'gender',
                'emergency_number', 'married', 'maladies', 'consultations','nbr_children', 'address',
                'documents','first_name','last_name'
                ]


class PatientInfoSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id','first_name','last_name' ,'carte_id', 'birth_date', 'numero_tel',
                'blood_type', 'gender', 'emergency_number','address','nbr_children'
                'married', 'maladies']

class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

    def create(self, validated_data):
        user =  Doctor.objects.create_user(**validated_data)
        return user

class LaboSerializer(ModelSerializer):
    class Meta:
        model = Labo
        fields = '__all__'

    def create(self, validated_data):
        user =  Labo.objects.create_user(**validated_data)
        return user
    
class DoctorInfoSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields =['id','specialite','first_name','last_name']

    def create(self, validated_data):
        user =  Doctor.objects.create_user(**validated_data)
        return user


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


class OrdonanceSerializer(ModelSerializer):
    medicaments = MedicamentDetailsSerializer(many=True)
    documents =DocumentMedicaleSerializer(many=True)
    
    class Meta:
        model = Ordonance
        fields = ['medicaments','documents']
    





class ConsultationSerializer(ModelSerializer):
    ordonance = OrdonanceSerializer()
    class Meta:
        model = Consultation
        fields = ['id','patient','doctor','maladie','note','date','maladie','ordonance']
    
    
    def create(self, validated_data):
        patient = validated_data['patient']
        doctor = validated_data['doctor']
        maladies = validated_data.pop('maladie',[])
        ordonance_data = validated_data.pop('ordonance')
        
        
        consultation = Consultation.objects.create(**validated_data)
        
        for maladie in maladies:
            consultation.maladie.add(maladie)
            patient.maladies.add(maladie)
        
        
        ordonance = Ordonance.objects.create(consultaion = consultation)
        medicaments = ordonance_data['medicaments']
        
        for medicament in medicaments:
            MedicamentDetails.objects.create(ordonance = ordonance , **medicament)
        
        documents = ordonance_data['documents']
        for document in ordonance_data['documents']:
            DocumentMedicale.objects.create(ordonance = ordonance ,doctor=doctor ,**document)
        
        return consultation