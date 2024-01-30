from django import forms

# modelos
from .models import User

# para verificar si es un usuario auntenticado
from django.contrib.auth import authenticate


# Importaciones para validar contraseña
from django.contrib.auth.password_validation import validate_password, CommonPasswordValidator, NumericPasswordValidator
from django.core.exceptions import ValidationError


# Clase base para validar contraseñas
class Validador_de_Contraseñas(forms.Form):

    # Método para validar la contraseña
    def clean_password2(self):

        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password1:
            try:
                validate_password(password1)
                validate_password(password2)
                CommonPasswordValidator().validate(password1)
                NumericPasswordValidator().validate(password1)
            except forms.ValidationError as e:
                msg = f'La contraseña no es valida por lo motivos, {e}'
                self.add_error('password1', msg)


# Clase para validar si el correo existe en la base de datos
class Validador_email(forms.Form):

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya existe , prueba con otro")
        return email


# Formulario de registro de usuarios
class RegisterForms(Validador_email, forms.ModelForm):

    password1 = forms.CharField(label='', required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Contraseña1'}))

    password2 = forms.CharField(label='', required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Contraseña2'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'nombres', 'apellido', 'genero']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'genero': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Genero'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        }

        labels = {
            'username': '', 'email': '', 'nombres': '', 'apellido': '', 'genero': ''
        }

    # Método para validar la contraseña en el formulario de registro

    def clean_password2(self):
        p1 = self.cleaned_data['password1']
        p2 = self.cleaned_data['password2']

        try:
            validate_password(p1)
            validate_password(p2)
            CommonPasswordValidator().validate(p1)
            NumericPasswordValidator().validate(p1)

        except ValidationError as e:
            msg = f'La contraseña no es valida, {",".join(e)}'
            self.add_error('password1', msg)
        if p1 != p2:
            self.add_error(
                'password2', 'Las contraseñas no coinciden ')


# Formulario de inicio de sesión de usuarios
class LoginForms(forms.Form):

    username = forms.CharField(label='',
                               required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField(label='', required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

    # Método para limpiar y validar los datos del formulario de inicio de sesión
    def clean(self):
        clean = super(LoginForms, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError(
                'Es usuario no existe, prueba de nuevo ')
        else:
            return clean


# Formulario para actualizar la contraseña del usuario
class UpdateForms(Validador_de_Contraseñas, forms.Form):

    password1 = forms.CharField(label='', required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Contraseña actual'}))

    password2 = forms.CharField(label='', required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Contraseña Nueva'}))


# Formulario para el código de confirmación del registro del usuario
class CodeRegistro(forms.Form):

    codigoregistro = forms.CharField(label='', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Ingresa codigo'}))

    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(CodeRegistro, self).__init__(*args, **kwargs)

    def clean_codigoregistro(self):
        codigo = self.cleaned_data['codigoregistro']

        if len(codigo) != 6:
            raise ValidationError(
                f'El codigo es incorrecto, solo tiene {len(codigo)} y debe ser 6 ')

        if not User.objects.codigo_validacio(self.id_user, codigo):
            raise forms.ValidationError('El codigo es incorrecto...')
