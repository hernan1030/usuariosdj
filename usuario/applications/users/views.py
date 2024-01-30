# recargar la pagina
from typing import Any
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# Para envio de email de prueba
from django.core.mail import send_mail


# para decorar y solo poder acceder si el usuario esta logueado
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# vistas genericas
from django.views.generic.edit import FormView
from django.views.generic import View

# autenticacion
from django.contrib.auth import authenticate, login, logout


# traer el formulario
from .forms import RegisterForms, LoginForms, UpdateForms, CodeRegistro

# modelo user
from .models import User


# funciones esta de archivo funtion.py
from .funtions import code_numrandom

# Create your views here.


# Vista para el registro de usuarios
class RegisterViews(FormView):
    template_name = 'usuarios/register.html'
    form_class = RegisterForms
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Generar un código aleatorio para el usuario
        codigo = code_numrandom()

        # Crear el usuario con el código aleatorio
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            coderandom=codigo


        )
        # Guardar campos adicionales del usuario
        usuario.nombres = form.cleaned_data['nombres'].lower(),
        usuario.apellido = form.cleaned_data['apellido'].lower(),
        usuario.genero = form.cleaned_data['genero']
        usuario.save()  # guardar en el User con estos campos adicionales

        # Variables para envio de email
        asunto = 'Confirmacion de email'
        mensaje = f'Codigo de verificacion de registro: {codigo}'
        email_remitente = 'garciaruizhernan9@gmail.com'

        # Enviar correo electrónico de confirmación
        send_mail(
            asunto, mensaje, email_remitente, [form.cleaned_data['email'],]
        )

        return HttpResponseRedirect(reverse_lazy('confi_email', kwargs={'pk': usuario.pk}))


# Vista para el inicio de sesión de usuarios
class LoginUser(FormView):
    template_name = 'usuarios/login.html'
    form_class = LoginForms
    success_url = reverse_lazy('perfil')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        login(self.request, user)

        return super().form_valid(form)


# Vista para el cierre de sesión de usuarios
@method_decorator(login_required, name='dispatch')
class LogoutViews(View):

    def get(self, request, *args, **kwars):

        logout(request)

        return HttpResponseRedirect(reverse('home'))


# Vista para actualizar la contraseña del usuario
@method_decorator(login_required, name='dispatch')
class UpdatePassword(FormView):
    template_name = 'usuarios/password-change.html'
    form_class = UpdateForms
    success_url = reverse_lazy('perfil')

    def form_valid(self, form):
        usuario = self.request.user

        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )
        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)

        return super(UpdatePassword, self).form_valid(form)


# Vista para confirmar el código de verificación del correo electrónico
class ConfirmacionCodigoViews(FormView):
    template_name = 'usuarios/confirmacion-email.html'
    form_class = CodeRegistro
    success_url = reverse_lazy('login')

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()
        # Obtener pk de los argumentos de la URL
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        # Marcar al usuario como activo
        User.objects.filter(
            id=self.kwargs['pk']

        ).update(
            is_active=True
        )

        return super().form_valid(form)
