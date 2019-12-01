from django.urls import path, include

from coop.accounts.views import SignupView, update_user, delete_user
from coop.core.views import home


urlpatterns = [
        path('signup/', SignupView.as_view(), name='signup'),
        path('profile/<int:user_id>', update_user, name='profile'),
        path('create/', home, name='create_user'),
        path('update/<int:user_id>/', update_user, name='update_user'),
        path('delete/<int:user_id>/', delete_user, name='delete_user'),
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