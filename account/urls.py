from django.urls import include, path
from account import views

urlpatterns = [
    path('login',views.user_login, name="user_login"),
    path('register',views.user_register, name="user_register"),
    path('change-password',views.change_password, name="change_password"),
    path('logout',views.user_logout, name="user_logout"),
    path('sifre-sifirlama/', views.sifre_sifirlama_talebi, name='sifre_sifirlama_talebi'),
    path('sifre-sifirlama/dogrulama/', views.sifre_sifirlama_dogrulama, name='sifre_sifirlama_dogrulama'),
    
]  