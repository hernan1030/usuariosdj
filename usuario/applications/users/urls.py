
from django.urls import path
from . import views

urlpatterns = [



    # urls para registrar usuarios
    path('register-user', views.RegisterViews.as_view(), name="register-user"),
    path('login', views.LoginUser.as_view(), name="login"),
    path('logout', views.LogoutViews.as_view(), name="logout"),
    path('password-change', views.UpdatePassword.as_view(), name="password-change"),
    path('register-usere/confirmacion/<int:pk>/',
         views.ConfirmacionCodigoViews.as_view(), name="confi_email"),


]
