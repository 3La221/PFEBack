from django.urls import path,include
from . import views 

from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenRefreshView

# Use TokenRefreshView provided by Simple JWT
refresh_jwt_token = TokenRefreshView.as_view()

urlpatterns = [
    
    #Authentication 
    path("register/", views.register , name="register"),
    path("register/doctor/", views.register_doctor , name="register-doctor"),
    path("register/labo/", views.register_labo , name="register-labo"),
    
    path("login/", views.login , name="login"),
    
    path("login/superAdmin",views.superuser_login , name="super_login"),
    
    path('token/refresh/', refresh_jwt_token, name='token_refresh'),

    
    #Patient Info
    path("patient/<str:pk>/",views.get_patient_details,name="patient-details"),
    path("patient/card/<str:pk>", views.get_patient_cardinfo, name="paitent-info"),
    # path("add_ordonance/<str:id>/", views.add_ordonance, name="add-ordonance"),
    # path("ordonances/<str:pk>/" , views.get_patient_ordonances ,name="patient-ordonances" ),    

    #CRUD
    path('maladies/', views.MaladieListCreateAPIView.as_view(), name='maladie-list-create'),
    path('maladies/<str:pk>/', views.MaladieRetrieveUpdateDestroyAPIView.as_view(), name='maladie-detail'),
    path('medicaments/', views.MedicamentListCreateAPIView.as_view(), name='medicament-list-create'),
    path('medicaments/<str:pk>/', views.MedicamentRetrieveUpdateDestroyAPIView.as_view(), name='medicament-detail'),
    path("allergies/",views.AllergieListCreateAPIView.as_view(),name="allergies"),

    
    path("doctor/add_document/<str:id>",views.add_document_doctor,name="add-document"),
    path('add_document/<str:id>',views.add_document,name="add-document"),
    path('deamnde_document/<str:id>',views.demande_document,name="demande-document"),
    path("documents/<str:id>",views.get_documents,name="documents"),
    path('add_consultation/<str:id>',views.add_consultation,name="add-consultation"),
    path('medical_doc/<str:id>',views.medicale_doc,name="medical-doc"),
    path('radios/<str:id>',views.radios,name="radios"),
    path('analyses/<str:id>',views.analyses,name="analyses"),
    path('chirurgies/<str:id>',views.chirurgies,name="chirurgies"),
        
    path('consultation/<str:id>/',views.consultation,name="consultations"),
    path("add_maladie/<str:id>/",views.add_maladie,name="add-maladie"),
    path("add_antecedent/<str:id>/",views.add_antec,name="add-antecd"),
    path("add_allergie/<str:id>/",views.add_allergie,name="add-allergie"),
    
    path("validate/<str:id>/",views.valider_account,name="validate-account"),
    
    path("doctor/",views.DoctorListCreateAPIView.as_view(),name="doctor-list-create"),
    path("doctor/<str:pk>/",views.DoctorRetrieveUpdateDestroyAPIView.as_view(),name="doctor-detail"),
    
    path("labo/",views.LaboListCreateAPIView.as_view(),name="labo-list-create"),
    path("labo/<str:pk>/",views.LaboRetrieveUpdateDestroyAPIView.as_view(),name="labo-detail"),
    
    path("non_valide/",views.get_non_valide,name="non-valide"),
    path("refuse/<str:id>/",views.non_valide,name="refuse"),
    path("data/",views.data,name="data"),
    
    path("edit/<str:id>/",views.edit_patient,name="edit"),
    path("delete/<str:id>/",views.delete_patient,name="delete"),
    
    path("delete_doc/<str:id>/",views.delete_doc,name="delete-doc"),
    path("delete_cons/<str:id>/",views.delete_cons,name="delete-medic"),
    
    path("exist/",views.does_exist,name="exist")
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
