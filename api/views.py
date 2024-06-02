from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from .serializers import *
from .permissions import *
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .utils import get_medicaments_data,add_maladies_data,add_allergies_data
from django.http import JsonResponse




@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        
        serializer = PatientSerializer(data=request.data) 

        if serializer.is_valid():
            user = serializer.save()
            tokens = RefreshToken.for_user(user)
            return Response({
                'id':user.id,
                'refresh': str(tokens),
                'access': str(tokens.access_token),
                'role' : "P"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def register_doctor(request):
    if request.method == 'POST':
        print(request.data)
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = RefreshToken.for_user(user)
            return Response({
                "message":"Now you have to wait for the admin to validate your account",
                "id":user.id
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_labo(request):
    if request.method == 'POST':
        serializer = LaboSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = RefreshToken.for_user(user)
            return Response({
               "message":"Now you have to wait for the admin to validate your account",
               "id":user.id
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def register_centre(request):
    if request.method == 'POST':
        serializer = CentreSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = RefreshToken.for_user(user)
            return Response({
               "message":"Now you have to wait for the admin to validate your account",
               "id":user.id
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def superuser_login(request):
    if request.method == 'POST':
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_superuser:
                tokens = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(tokens),
                    "access": str(tokens.access_token),
                    "role":"A"
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Not a superuser."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data.get("email")
        password = request.data.get("password")
        # print("EMAIL",email)
        # print("PASSWORD",password)

        user = authenticate(email=email , password=password)
        
        # print("USER",user)
        
        if user :
            tokens = RefreshToken.for_user(user)

            if hasattr(user, 'patient'):
                role = 'P'

            elif hasattr(user, 'doctor'):
                if not user.doctor.valide:
                    return Response({'detail': 'Your account is not validated yet'}, status=status.HTTP_401_UNAUTHORIZED)
                role = 'D'
            elif hasattr(user, 'labo'):
                if not user.labo.valide:
                    return Response({'detail': 'Your account is not validated yet'}, status=status.HTTP_401_UNAUTHORIZED)
                role = 'L'
            elif hasattr(user,'centre'):
                if not user.centre.valide:
                    return Response({'detail': 'Your account is not validated yet'}, status=status.HTTP_401_UNAUTHORIZED)
                role = 'C'

                
            return Response({
                'id':user.id,
                'refresh':str(tokens),
                'access':str(tokens.access_token),
                'role' : role
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



# @api_view(['POST'])
# @permission_classes([IsAuthenticated , IsDoctor])
# def add_ordonance(request,id):
#     if request.method == "POST":
#         request.data['doctor'] = request.user.id 
#         request.data['patient'] = id
#         serializer = OrdonanceSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response("Ordonance Added !!", status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# @permission_classes([IsAuthenticated])
# @api_view(['GET'])
# def get_patient_ordonances(request,pk):
#     print("ID",pk)
#     print("REQ ID",request.user.id)
#     if request.method == "GET":
#         if  hasattr(request.user, 'doctor') or ( request.user.id == pk) :
#             patient = Patient.objects.get(id=pk)
#             ordonances = patient.ordonances.all()
#             print(ordonances)
#             serializer = OrdonanceSerializer(instance=ordonances,many=True)
#             return Response(serializer.data , status=status.HTTP_200_OK )
#         return Response("You can't access this data" , status=status.HTTP_401_UNAUTHORIZED)


@api_view(["DELETE"])
def delete_patient(request,id):
    try:
        password = request.data["password"]
        try:
            patient = Patient.objects.get(id=id)
            if not patient.check_password(password):
                return Response("Invalid Password !!", status=status.HTTP_401_UNAUTHORIZED)
            patient.delete()
            return Response("Patient Deleted !!", status=status.HTTP_201_CREATED)
        except Patient.DoesNotExist:
            return Response("Patient Not Found !!", status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return Response("Password Required !!", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def does_exist(request):
    try:
        carte_id = request.data["carte_id"]
        try :
            patient = Patient.objects.get(carte_id=carte_id)
            return Response({"message":"Patient Exist" , "exist":True , "id":patient.id } ,status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({"message":"Patient Doesn't Exist","exist":False},status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        id = request.data["id"]
        try:
            patient = Patient.objects.get(id=id)
            return Response({"message":"User Exist" , "exist":True , "id":patient.id } ,status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({"message":"User Doesn't Exist","exist":False},status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])

def get_patient_cardinfo(request,pk):
    if request.method == "GET":
        patient = Patient.objects.get(id=pk)
        serializer = PatientInfoSerializer(instance=patient,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['PUT'])
def edit_patient(request,id):
    if request.method == "PUT":
        patient = Patient.objects.get(id=id)
        serializer = PatientSerializer(instance=patient,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Patient Updated !!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_patient_details(request,pk):
    if request.method == "GET":
        patient = Patient.objects.get(id=pk) 
        serializer = PatientDetailsSerializer(instance=patient,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_doc(request,id):
    doc = DocumentMedicale.objects.get(id=id)
    doc.delete()
    return Response("Document Deleted !!", status=status.HTTP_201_CREATED)

@api_view(["DELETE"])
def delete_cons(rquest,id):
    cons = Consultation.objects.get(id=id)
    cons.delete()
    return Response("Consultation Deleted !!", status=status.HTTP_201_CREATED)
 
       
class MaladieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Maladie.objects.all()
    serializer_class = MaladieSerializer



class MaladieRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Maladie.objects.all()
    serializer_class = MaladieSerializer

class MedicamentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Medicament.objects.all()
    serializer_class = MedicamentSerializer

class MedicamentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicament.objects.all()
    serializer_class = MedicamentSerializer

class AllergieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Allergie.objects.all()
    serializer_class = AllergieSerializer





@api_view(["GET"])
def consultation(request,id):
    consultation = Consultation.objects.get(id=id)
    serializers = ConsultationSerializer(instance=consultation,many=False)
    return Response(serializers.data,status=status.HTTP_200_OK)

    
    
@api_view(["POST"])
def demande_document(request,id):
    request.data["patient"] = id
    print("USER",request.user.id)
    request.data["doctor"] = request.user.id
    serializer = DocumentMedicaleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response("Document Demande Added !!", status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST","GET","PUT"])
def add_document_doctor(request,id):
    if request.method == "POST":
        request.data["patient"] = id
        request.data["doctor"] = request.user.id
        serializer = DocumentMedicaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Document Added !!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST","GET","PUT"])
def add_document(request,id):
    if request.method == "POST":
        request.data["patient"] = id
        try:
            if request.data["type_doc"] == "C":
                request.data["doctor"] = request.user.id
            else:  
                request.data["labo"] = request.user.id
        except KeyError:
            request.data["labo"] = request.user.id
        serializer = DocumentMedicaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Document Added !!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        patient = Patient.objects.get(id=id)
        documents = patient.documents.all()
        serializer = DocumentMedicaleSerializer(instance=documents,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(["GET"])
def get_documents(request,id):
    patient = Patient.objects.get(id=id)
    documents = patient.documents.all()
    serializer = DocumentMedicaleSerializer(instance=documents,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)




@api_view(["GET"])
def radios(request,id):
    patient = Patient.objects.get(id=id)
    documents = patient.documents.filter(type_doc="R")
    serializer = DocumentMedicaleSerializer(instance=documents,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["GET"])
def analyses(request,id):
    patient = Patient.objects.get(id=id)
    documents = patient.documents.filter(type_doc="A")
    serializer = DocumentMedicaleSerializer(instance=documents,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["GET"])
def chirurgies(request,id):
    if request.method == "GET":
        patient = Patient.objects.get(id=id)
        documents = patient.documents.filter(type_doc="C")
        serializer = DocumentMedicaleSerializer(instance=documents,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(["PUT","GET"])
def medicale_doc(request,id):
    doc = DocumentMedicale.objects.get(id=id)
    if request.method == "GET":
        serializer = DocumentMedicaleSerializer(instance=doc,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)
    if request.method == "PUT":
        doc.demande = False 
        profile = Profile.objects.get(id=request.user.id)
        doc.doctor = profile
        try:
            doc.note = request.data["note"]
        except KeyError:
            pass
        doc.save()
        return Response("Document Updated !!", status=status.HTTP_201_CREATED)


@api_view(["POST","GET"])
def add_consultation(request,id):
    if request.method == "POST":
        request.data["patient"] = id
        request.data["doctor"] = request.user.id
        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Consultation Added !!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        patient = Patient.objects.get(id=id)
        consultations = patient.consultations.all()
        serializer = ConsultationSerializer(instance=consultations,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["POST"])
def add_maladie(request,id):
    patient = Patient.objects.get(id=id)
    try:
        maladie = Maladie.objects.get(id=request.data["maladie"])
    except Maladie.DoesNotExist:
        return Response("Maladie not found",status=status.HTTP_404_NOT_FOUND)
    
    patient.maladies.add(maladie)
    return Response("Maladie Added !!", status=status.HTTP_201_CREATED)

@api_view(["POST","DELETE"])
def add_antec(request,id):
    if request.method == "DELETE":
        patient = Patient.objects.get(id=id)
        antecedent = Antecedent.objects.get(id=request.data["antecedent"])
        patient.antecedents.remove(antecedent)
        return Response("Antecedent Removed !!", status=status.HTTP_201_CREATED)
    patient = Patient.objects.get(id=id)
    antecedent = Antecedent.objects.create(**request.data)
    
    patient.antecedents.add(antecedent)
    return Response("Antecedent Added !!", status=status.HTTP_201_CREATED)

def data(request):
    # get_medicaments_data()
    # add_maladies_data()
    add_allergies_data()
    
    return JsonResponse({"data":"Data Added"})

@api_view(["POST","DELETE"])
def add_allergie(request,id):
    if request.method == "DELETE":
        patient = Patient.objects.get(id=id)
        allergie = Allergie.objects.get(id=request.data["allergie"])
        patient.allergies.remove(allergie)
        return Response("Allergie Removed !!", status=status.HTTP_201_CREATED)
    patient = Patient.objects.get(id=id)
    
    allergie , created = Allergie.objects.get_or_create(name=request.data["name"])
    
    if created or allergie.affiche != request.data["affiche"]:
        allergie.affiche = request.data["affiche"]
        allergie.save()
    
    
    patient.allergies.add(allergie)
    return Response("Allergie Added !!", status=status.HTTP_201_CREATED)


@api_view(["POST"])
def valider_account(request,id):
    user = Profile.objects.get(id=id)
    if hasattr(user, 'doctor'):
        user.doctor.valide = True
        user.doctor.save()
    elif hasattr(user, 'labo'):
        user.labo.valide = True
        user.labo.save()
    return Response("Account Validated !!", status=status.HTTP_201_CREATED)

@api_view(["DELETE"])
def non_valide(request,id):
    user = Profile.objects.get(id=id)
    if hasattr(user, 'doctor'):
        user.doctor.delete()
    elif hasattr(user, 'labo'):
        user.labo.delete()
    elif hasattr(user,'centre'):
        user.centre.delete()
    return Response("Account Deleted !!", status=status.HTTP_201_CREATED)

class LaboListCreateAPIView(generics.ListCreateAPIView):
    queryset = Labo.objects.all()
    serializer_class = LaboInfoSerializer
    

class LaboRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Labo.objects.all()
    serializer_class = LaboInfoSerializer

class DoctorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorInfoSerializer

class DoctorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorInfoSerializer
    
    
@api_view(["GET"])
def get_non_valide(request):
    doctors = Doctor.objects.filter(valide=False)
    labos = Labo.objects.filter(valide=False)
    centres = Centre.objects.filter(valide=False)
    serializer = DoctorInfoSerializer(instance=doctors,many=True)
    serializer2 = LaboInfoSerializer(instance=labos,many=True)
    serializer3 = CentreSerializer(instance=centres,many=True)
    
    return Response({
        "doctors":serializer.data,
        "labos":serializer2.data,
        "centres":serializer3.data
    },status=status.HTTP_200_OK)