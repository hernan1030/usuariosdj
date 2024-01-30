from django.db import models

from django.contrib.auth.models import BaseUserManager

# Con este manager modifico la creacion de usuarios en django con nuevos campos


class UserManager(BaseUserManager, models.Manager):

    # este metodos es generico y puedo puedo utilizar para create_user como para create_superuser
    def _create_user(self, username, email, password, is_staff, is_superuser, is_active, coderandom, **extra_field):

        if not username:
            raise ValueError("El usuario es obligatorio")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            coderandom=coderandom,
            **extra_field,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username,  email,  password=None,  **extra_field):
        user = self._create_user(
            username,
            email,
            password,
            False,
            False,
            False,
            **extra_field
        )

        return user

    def create_superuser(self, username, email, password=None, **extra_field):

        user = self._create_user(
            username,
            email,
            password,
            True,
            True,
            True,
            **extra_field
        )

        return user

    def codigo_validacio(self, id_user, cod_registro):
        filtrar = self.filter(id=id_user, coderandom=cod_registro).exists()

        return filtrar
