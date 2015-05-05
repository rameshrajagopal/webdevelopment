from __future__ import absolute_import
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.core.urlresolvers import reverse_lazy

from .forms import RegistrationForm, LogginForm

class HomePageView(generic.TemplateView):
    template_name = 'home.html'

class SignUpView(generic.CreateView):
    form_class = RegistrationForm
    model = User
    template_name = 'accounts/signup.html'

class LoginView(generic.FormView):
    form_class = LogginForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        user = form.cleaned_data['username']
        pwd  = form.cleaned_data['password']
        user = authenticate(username=user, password=pwd)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)

class LogoutView(generic.RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
