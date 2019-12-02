from django.urls import path

from coop.core.views import home
from .views import CreateCooperative, CreateUnit

app_name = 'base'

urlpatterns = [
    path('', home, name='home'),
    path('coop/create/', CreateCooperative.as_view(), name='create_coop'),
    path('coop/unit/create/', CreateUnit.as_view(), name='create_unit')
]
