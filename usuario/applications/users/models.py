from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# Create your models here.
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICE = (
        ("M", "MASCULINO"),
        ("F", "FEMENINO"),
        ("O", "OTRO"),
    )

    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField()
    nombres = models.CharField(max_length=30, blank=True)
    apellido = models.CharField(max_length=30, blank=True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICE, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False, blank=True)
    coderandom = models.CharField(max_length=6, blank=True)

    objects = UserManager()

    # este es el que se pedira para crear usuario como principal
    USERNAME_FIELD = "username"
    # este capo como no lo tengo como blank true , lo debo poner aqui para que sea solicitdo
    REQUIRED_FIELDS = ["email"]

    def __str__(self) -> str:
        return self.username
