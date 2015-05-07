from django.views import generic
from django.http import HttpResponse

from . import models
from . import forms
from braces import views

# Create your views here.
class RestrictToUserMixin(object):
    def get_queryset(self):
        queryset = super(RestrictToUserMixin, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

class TalkListDetailView(RestrictToUserMixin,
#        views.PrefetchRelatedMixin,
        views.LoginRequiredMixin,
        generic.DetailView):
    model = models.TalkList
    prefetch_related = ('talks',)


class TalkListListView(RestrictToUserMixin,
            views.LoginRequiredMixin,
            generic.ListView):
    model = models.TalkList

class TalkListCreateView(
     views.LoginRequiredMixin,
     views.SetHeadlineMixin,
     generic.CreateView
 ):
     form_class = forms.TalkListForm
     headline = 'Create'
     model = models.TalkList

     def form_valid(self, form):
         self.object = form.save(commit=False)
         self.object.user = self.request.user
         self.object.save()
         return super(TalkListCreateView, self).form_valid(form)

class TalkListUpdateView(
        RestrictToUserMixin,
        views.LoginRequiredMixin,
        views.SetHeadlineMixin,
        generic.UpdateView
    ):
        form_class = forms.TalkListForm
        headline = 'update'
        model = models.TalkList

class TalkListRemoveView(
        views.LoginRequiredMixin,
        generic.ListView
    ):
       model = models.TalkList
