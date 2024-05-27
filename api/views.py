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
        try:
            role = request.data.pop("role")
            serializer = PatientSerializer(data=request.data) if role == "P" else (DoctorSerializer(data=request.data)
                                                                                if role == "D" else
                                                                                LaboSerializer(data=request.data)) 
        except KeyError:
            return Response("Please pass the role : D for Doctor P for Patient ...", status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            user = serializer.save()
            tokens = RefreshToken.for_user(user)
            return Response({
                'id':user.id,
                'refresh': str(tokens),
                'access': str(tokens.access_token),
                'role' : role
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
                'id':user.id,
                'refresh': str(tokens),
                'access': str(tokens.access_token),
                'role' : "Doctor"
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
                'id':user.id,
                'refresh': str(tokens),
                'access': str(tokens.access_token),
                'role' : "Labo"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        id = request.data.get("id")
        password = request.data.get("password")
        # print("EMAIL",email)
        print("PASSWORD",password)

        user = authenticate(id=id , password=password)
        
        # print("USER",user)
        
        if user :
            tokens = RefreshToken.for_user(user)

            if hasattr(user, 'patient'):
                role = 'Patient'

            elif hasattr(user, 'doctor'):
                if not user.doctor.valide:
                    return Response({'detail': 'Your account is not validated yet'}, status=status.HTTP_401_UNAUTHORIZED)
                role = 'Doctor'
            elif hasattr(user, 'labo'):
                if not user.labo.valide:
                    return Response({'detail': 'Your account is not validated yet'}, status=status.HTTP_401_UNAUTHORIZED)
                role = 'Labo'

                
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

@api_view(['GET'])

def get_patient_cardinfo(request,pk):
    if request.method == "GET":
        patient = Patient.objects.get(id=pk)
        serializer = PatientInfoSerializer(instance=patient,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def get_patient_details(request,pk):
    if request.method == "GET":
        patient = Patient.objects.get(id=pk) 
        serializer = PatientDetailsSerializer(instance=patient,many=False)
        # serializer = PatientInfoSerializer(instance=patient,many=False) if (request.user.id != pk and not hasattr(request.user, 'doctor') or (not request.user.is_authenticated) or not hasattr(request.user, 'labo') ) else PatientDetailsSerializer(instance=patient,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)

        
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

    
# @api_view(['POST','GET'])
# @permission_classes([IsAuthenticated , IsHospital])
# def get_doctors(request):
#     if request.method == "GET":
#         hospital = Hospital.objects.get(id=request.user.id)
#         doctors = hospital.doctors.all()
#         serializer = DoctorInfoSerializer(instance=doctors,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#     if request.method == "POST":
#         doctor_id = request.data["id"]
#         doctor = Doctor.objects.get(id=doctor_id)
#         doctor.hospitals.add(request.user.id) 
#         doctor.save()
#         return Response(f"{doctor} Added to your hospital",status= status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def consultation(request,id):
    consultation = Consultation.objects.get(id=id)
    serializers = ConsultationSerializer(instance=consultation,many=False)
    return Response(serializers.data,status=status.HTTP_200_OK)

    
    
@api_view(["POST"])
@permission_classes([IsAuthenticated,IsDoctor])
def demande_document(request,id):
    request.data["patient"] = id
    print("USER",request.user.id)
    request.data["doctor"] = request.user.id
    serializer = DocumentMedicaleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response("Document Demande Added !!", status=status.HTTP_201_CREATED)
    


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
@permission_classes([IsAuthenticated])
def radios(request,id):
    patient = Patient.objects.get(id=id)
    documents = patient.documents.filter(type_doc="R")
    serializer = DocumentMedicaleSerializer(instance=documents,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def analyses(request,id):
    patient = Patient.objects.get(id=id)
    documents = patient.documents.filter(type_doc="A")
    serializer = DocumentMedicaleSerializer(instance=documents,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
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
        request.data["demande"] = False
        serializer = DocumentMedicaleSerializer(instance=doc,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Document Updated !!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST","GET"])
@permission_classes([IsAuthenticated , IsDoctor])
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

@api_view(["POST"])
def add_antec(request,id):
    patient = Patient.objects.get(id=id)
    try:
        maladie = Maladie.objects.get(id=request.data["maladie"])
    except Maladie.DoesNotExist:
        return Response("Maladie not found",status=status.HTTP_404_NOT_FOUND)
    
    patient.antecedents.add(maladie)
    return Response("Antecedent Added !!", status=status.HTTP_201_CREATED)

def data(request):
    # get_medicaments_data()
    # add_maladies_data()
    #add_allergies_data()
    
    return JsonResponse({"data":"Data Added"})

@api_view(["POST"])
def add_allergie(request,id):
    patient = Patient.objects.get(id=id)
    allergie , _ = Allergie.objects.get_or_create(name=request.data["name"])
    
    patient.allergies.add(allergie)
    return Response("Allergie Added !!", status=status.HTTP_201_CREATED)