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
    
    path('token/refresh/', refresh_jwt_token, name='token_refresh'),

    
    #Patient Info
    path("patient/<str:pk>/",views.get_patient_details,name="patient-details"),
    
    # path("add_ordonance/<str:id>/", views.add_ordonance, name="add-ordonance"),
    # path("ordonances/<str:pk>/" , views.get_patient_ordonances ,name="patient-ordonances" ),    

    #CRUD
    path('maladies/', views.MaladieListCreateAPIView.as_view(), name='maladie-list-create'),
    path('maladies/<str:pk>/', views.MaladieRetrieveUpdateDestroyAPIView.as_view(), name='maladie-detail'),
    path('medicaments/', views.MedicamentListCreateAPIView.as_view(), name='medicament-list-create'),
    path('medicaments/<str:pk>/', views.MedicamentRetrieveUpdateDestroyAPIView.as_view(), name='medicament-detail'),
    
    
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
    
    
    path("data/",views.data,name="data")
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
