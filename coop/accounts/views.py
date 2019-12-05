# accounts/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.views.generic import FormView
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url, urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse

from coop.settings import SYSTEM_NAME
from coop.accounts.models import User
from coop.accounts.forms import LoginForm, UsersForm, UsersUpdateForm, SignupForm
from coop.accounts.tokens import account_activation_token


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


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your {0} account.'.format(SYSTEM_NAME)
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'home.html', {'messages': ['Please confirm your email address to complete '
                                                            'the registration']})
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request,  'home.html',
                      {'messages': ["Thank you for your email confirmation. <p/>Now you can login your account."]})
    else:
        return render(request,  'home.html', {'messages': ['Activation link is invalid!']})


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
        return redirect(reverse('base:home'))
    return render(request, 'user-form.html', {'form': form, 'user': user})


@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('list_users')
    return render(request, 'user-delete-confirm.html', {'user': user})
