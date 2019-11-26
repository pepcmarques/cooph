from django.urls import path

from .views import CreateCooperative

urlpatterns = [
    path('create/', CreateCooperative.as_view(), name='name_here'),
]
