from django.urls import path
from . import views

urlpatterns = [

    path('',views.home1, name='home1'),
    #path('', views.home, name='home'),
    path('apply/', views.apply_connection, name='apply_connection'),
    path('connections/', views.connection_list, name='connection_list'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('customer_registration/', views.customer_registration, name='customer_registration'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('connection_edit/<int:connection_id>/', views.connection_edit, name='connection_edit'),
]
