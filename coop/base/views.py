from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from .decorators import superuser_only

from .forms import CooperativeForm, UnitForm


@method_decorator(superuser_only, name='dispatch')
class CreateCooperative(CreateView):
    form_class = CooperativeForm
    template_name = 'cooperative.html'
    success_url = '/'


class CreateUnit(CreateView):
    form_class = UnitForm
    template_name = 'unit.html'
    success_url = '/'
