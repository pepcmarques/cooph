from django.views.generic import CreateView

from .forms import CooperativeForm


class CreateCooperative(CreateView):
    form_class = CooperativeForm
    template_name = 'cooperative.html'
    success_url = '/'
