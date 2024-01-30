
from django.urls import path
from . import views

urlpatterns = [



    # urls del home
    path('', views.HomeViews.as_view(), name="home"),
    path('perfil', views.PerfilViews.as_view(), name="perfil"),




]
