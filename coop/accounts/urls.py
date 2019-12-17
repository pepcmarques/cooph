from django.urls import path
from django.views.generic import TemplateView

from coop.accounts.views import signup, update_user, delete_user, LoginView, activate, forgotten_password
from coop.core.views import home

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', signup, name='signup'),
    path('activate/<str:uidb64>/<str:token>', activate, name='activate'),
    path('profile/<int:user_id>', update_user, name='profile'),
    path('create/', home, name='create_user'),
    path('update/<int:user_id>/', update_user, name='update_user'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),
    path('forgotten/', forgotten_password, name='forgotten'),
    path('forgotten/done/', TemplateView.as_view(template_name='forgotten_password_done.html'),
         name='forgotten_password_done'),
]

"""
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
"""
