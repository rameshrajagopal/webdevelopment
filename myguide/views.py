from __future__ import absolute_import
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from braces import views

from .forms import RegistrationForm, LogginForm
from talks.models import TalkList

class HomePageView(generic.TemplateView):
    template_name = 'home.html'

class SignUpView(views.AnonymousRequiredMixin, 
                 views.FormValidMessageMixin, 
                 generic.CreateView):
    form_class = RegistrationForm
    form_valid_message = "Thanks for signing up. Go ahead and login"
    model = User
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        resp = super(SignUpView, self).form_valid(form)
        TalkList.objects.create(user=self.object, name='To Attend')
        return resp

class LoginView(views.AnonymousRequiredMixin, 
                views.FormValidMessageMixin, 
                generic.FormView):
    form_class = LogginForm
    form_valid_message = "You are logged in"
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

def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('home'))
