"""cancer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [


    path("", views.index, name="Index"),
    path("Index", views.index, name="Index"),
    path("index", views.index, name="index"),
    path('Login/',  views.Login,  name="Login"),
    path('Logout/',  views.Logout,  name="Logout"),
    path('privacy/',  views.privacy,  name="privacy"),
    path('profile/', views.profile, name="profile"),
    path('AdminHome/',  views.AdminHome,  name="AdminHome"),
    path('adminhead/',  views.adminhead,  name="adminhead"),
    path('Add_pharma/', views.Add_pharma, name="Add_pharma"),
    path('deletePhrama/', views.deletePhrama, name="deletePhrama"),
    path('Add_med/', views.Add_med, name="Add_med"),
    path('remove_med', views.remove_med,name="remove_med"),
    path('list_pharma/', views.list_pharma, name="list_pharma"),
    path("forgot", views.forgot, name="forgot"),
    path("manufacture",views.manufacture,name="manufacture"),
    path ('manufactuer/',views.manufactuer,name="manufactuer"),
    path ('list_manu/',views.list_manu,name="list_manu"),
    path ('distributor/',views.distributor,name="distributor"),
    path ('hospital/',views.hospital,name="hospital"),
    path ('list_dist/',views.list_dist,name="list_dist"),
    path ('list_hosp/',views.list_hosp,name="list_hosp"),
    path("approve_manufacturer/<int:manufacturer_id>/",views.approve_manufacturer,name="approve_manufacturer"),
    path("reject_manufacturer/<int:manufacturer_id>/",views.reject_manufacturer,name="reject_manufacturer"),
    path("approve_distributor/<int:distributor_id>/",views.approve_distributor,name="approve_distributor"),
    path("reject_distributor/<int:distributor_id>/",views.reject_distributor,name="reject_distributor"),
    path("approve_hospital/<int:hospital_id>/",views.approve_hospital,name="approve_hospital"),
    path("reject_hospital/<int:hospital_id>/",views.reject_hospital,name="reject_hospital"),
    path("staffhead",views.staffhead,name="staffhead"),
    path("disthead",views.disthead,name="disthead"),
    path("hosphead",views.hosphead,name="hosphead"),
    path('vaccine_request/', views.vaccine_request, name='vaccine_request'),
    path('vaccine_request_submit/', views.vaccine_request_submit, name='vaccine_request_submit'),
     path('list_request/', views.list_request, name='list_request'), 
    path('list_request_manu/', views.list_request_manu, name='list_request_manu'), 
     path('approve_vaccine_request/<int:vaccine_id>/', views.approve_vaccine_request, name='approve_vaccine_request'),
    path('reject_vaccine_request/<int:vaccine_id>/', views.reject_vaccine_request, name='reject_vaccine_request'),
    path('mark_as_completed/<int:medicine_id>/', views.mark_as_completed, name='mark_as_completed'),
     path('allot_vaccine_request/', views.allot_vaccine_request, name='allot_vaccine_request'),
    path('manage_authorization_requests/', views.manage_authorization_requests, name='manage_authorization_requests'),
    path('list_vaccine_requests/', views.list_vaccine_requests, name='list_vaccine_requests'),
    path('book_vaccine_request/', views.book_vaccine_request, name='book_vaccine_request'),
    path('get_vaccine_details/', views.get_vaccine_details, name='get_vaccine_details'),
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)