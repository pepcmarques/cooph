# accounts/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import CreateView, FormView
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url

from django.urls import reverse

from coop.accounts.models import User
from coop.accounts.forms import LoginForm, UsersForm, UsersUpdateForm, SignupForm


class LoginView(FormView):
    form_class = LoginForm
    success_url = "/"
    template_name = 'login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect('/')


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'signup.html'
    success_url = '/accounts/login'


def profile(request, user_id):
    return update_user(request, user_id)


def list_users(request):
    users = User.objects.order_by('email')
    return render(request, 'users.html', {'users': users})


@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    form = UsersForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_users')
    return render(request, 'user-form.html', {'form': form})


def update_user(request, user_id):
    if not request.user.is_superuser:
        if request.user.id != user_id:
            return redirect('home')
    user = User.objects.get(id=user_id)
    form = UsersUpdateForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect(reverse('home'))
    return render(request, 'user-form.html', {'form': form, 'user': user})


@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('list_users')
    return render(request, 'user-delete-confirm.html', {'user': user})
