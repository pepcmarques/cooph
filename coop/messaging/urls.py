from django.urls import path

from coop.messaging.views import Messaging, MessagesList

app_name = 'messaging'

urlpatterns = [
    path('', Messaging.as_view(), name='msg'),
    path('list/<int:user_id>/', MessagesList.as_view(), name='msg_list'),
]
