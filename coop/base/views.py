from django.views.generic import CreateView

from .forms import CooperativeForm, UnitForm


class CreateCooperative(CreateView):
    form_class = CooperativeForm
    template_name = 'cooperative.html'
    success_url = '/'


class CreateUnit(CreateView):
    form_class = UnitForm
    template_name = 'unit.html'
    success_url = '/'
