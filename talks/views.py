from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

from braces import views
from . import models

# Create your views here.
class TalkListDetailView(generic.View):
    def get(self, *args, **kwargs):
        return HttpResponse("A Talk list")

class TalkListListView(views.LoginRequiredMixin, generic.ListView):
    model = models.TalkList

    def get_queryset(self):
        return self.request.user.lists.all()
