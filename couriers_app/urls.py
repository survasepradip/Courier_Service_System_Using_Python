from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [

    # Customer Urls

    path('', views.index, name='index'),
    path('customer-register', views.cust_register, name='customer-register'),
    path('customer-login', views.cust_login, name='customer-login'),
    path('customer-dashboard', views.cust_dashboard, name='customer-dashboard'),


    path('track-package', views.track_package, name='track-package'),
    
    path('create-parcel', views.cust_create_parcel, name='create-parcel'),
    path('parcel-payment', views.final_package_booking, name='parcel-payment'),
    path('payment-success', views.payment_success, name='payment-success'),
    path('my-parcels', views.cust_parcels, name='my-parcels'),
    path('my-profile', views.cust_profile, name='my-profile'),
    path('logout', views.cust_logout, name='logout'),



    # Depot-Employee Urls
    
    path('depot-login', views.depot_login, name='depot-login'),
    path('depot-dash', views.depot_dashboard, name='depot-dash'),
    path('depot-package', views.depot_package, name='depot-package'), 

    path('depot-edit-package/<int:id>/', views.depot_edit_packages, name='depot-edit-package'), 


    # Company Urls

    path('create-company', views.company_create, name='create-company'),
    path('company-login', views.company_login, name='company-login'),
    path('company-dashboard', views.company_dash, name='company-dashboard'),
    
    path('create-depot', views.comp_create_depot, name='create-depot'),
    path('our-depot', views.comp_depot, name='our-depot'),
    path('add-employee', views.comp_create_emp, name='add-employee'),
    path('make-depot-admin/<int:id>/', views.make_depot_admin, name='make-depot-admin'), 
    path('see-packages/<int:id>/', views.comp_see_packages, name='see-packages'),
    path('edit-package/<int:id>/', views.comp_edit_packages, name='edit-package'),
    path('our-employee/<int:id>/', views.comp_employees,name='our-employee'),













]