# vistas genericas
from django.views.generic import TemplateView
from django.views.generic import ListView


# para decorar y solo poder acceder si el usuario esta logueado
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# modelo user


class HomeViews(TemplateView):
    template_name = 'home/home.html'


@method_decorator(login_required, name='dispatch')
class PerfilViews(TemplateView):
    template_name = 'home/perfil.html'


class ListarRegistros(ListView):
    template_name = 'home/listar-usuarios.html'
