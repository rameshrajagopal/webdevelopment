from django.views import generic
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db.models import Count
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

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
        views.PrefetchRelatedMixin,
        generic.DetailView):
    form_class = forms.TalkForm
    http_method_names = ['get', 'post']
    model = models.TalkList
    prefetch_related = ('talks',)

    def get_context_data(self, *args, **kwargs):
        context = super(TalkListDetailView, self).get_context_data(*args,
                **kwargs)
        context.update({'form': self.form_class(self.request.POST or None)})
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = self.get_object()
            talk = form.save(commit=False)
            talk.talk_list = obj
            talk.save()
        else:
             return self.get(request, *args, **kwargs)
        return redirect(obj)

class TalkListListView(RestrictToUserMixin,
            views.LoginRequiredMixin,
            generic.ListView):
    model = models.TalkList
    def get_queryset(self):
        queryset = super(TalkListListView, self).get_queryset()
        queryset = queryset.annotate(talk_count=Count('talks'))
        return queryset

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

class TalkListRemoveTalkView(
        views.LoginRequiredMixin,
        generic.RedirectView
    ):
        model = models.Talk

        def get_redirect_url(self, *args, **kwargs):
            return self.talklist.get_absolute_url()

        def get_object(self, pk, talklist_pk):
            try:
                talk = self.model.objects.get(
                        pk=pk,
                        talk_list_id=talklist_pk,
                        talk_list__user = self.request.user
                        )
            except models.Talk.DoesNotExist:
                raise Http404
            else:
                return talk

        def get(self, request, *args, **kwargs):
            self.object = self.get_object(kwargs.get('pk'), 
                                          kwargs.get('talklist_pk'))
            self.talklist = self.object.talk_list
            messages.success(
                    request, 
                    u'{0.name} was removed from {1.name}'.format(
                        self.object, self.talklist))
            self.object.delete()
            return super(TalkListRemoveTalkView, self).get(request, *args,
                    **kwargs)

class TalkListScheduleView(            
        RestrictToUserMixin,
        views.PrefetchRelatedMixin,
        generic.DetailView
    ):
        model = models.TalkList
        prefetch_related = ('talks', )
        template_name ='talks/schedule.html'

class TalkListRemoveView(
        views.LoginRequiredMixin,
        generic.RedirectView
    ):
        model = models.TalkList
        url = reverse_lazy('talks:lists:list')

        def get_object(self, slug):
            try:
                talklist_obj = self.model.objects.get(slug=slug,
                        user=self.request.user)
            except models.TalkList.DoesNotExist:
                raise Http404
            else:
                return talklist_obj
            
        def get(self, request, *args, **kwargs): 
            self.object = self.get_object(kwargs.get('slug'))
            messages.success(request, 
                    u'{0.name} was removed from the list'.format(self.object))
            self.object.delete()
            return super(TalkListRemoveView, self).get(request, *args,
                    **kwargs)

class TalksListView(views.LoginRequiredMixin,
                    generic.ListView
    ):
        model = models.Talk

        def get_queryset(self, *args, **kwargs):
            queryset = super(TalksListView, self).get_queryset()
            return queryset

class TalksDetailView(views.LoginRequiredMixin, 
                    generic.DetailView
    ):
        model = models.Talk
        template_name = 'talks/talk_detail.html'

        def get_queryset(self): 
            print('queryset')
            self.queryset =  self.model.objects.filter(talk_list__user=self.request.user)
            return self.queryset

        def get(self, request, *args, **kwargs): 
            print('get')
            self.queryset = self.get_queryset()
            print(self.queryset)
            print(kwargs.get('slug'))
            self.object = self.queryset.filter(slug=kwargs.get('slug'))
            print(self.object)
            return super(TalksDetailView, self).get(request, *args,
                    **kwargs)
