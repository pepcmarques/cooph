from django.urls import path

from .views import CreateCooperative, CreateUnit

urlpatterns = [
    path('create/', CreateCooperative.as_view(), name='create_coop'),
    path('unit/create/', CreateUnit.as_view(), name='create_unit')
]
