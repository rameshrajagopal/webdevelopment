from __future__ import absolute_import

from django.conf.urls import patterns, url, include
from . import views

list_patterns = patterns(
        '',
        url(r'^$', views.TalkListListView.as_view(), name='list'),
        url(r'^d/(?P<slug>[-\w]+)/$', views.TalkListDetailView.as_view(), name='detail'),
        url(r'^create/$', views.TalkListCreateView.as_view(), name='create'),
        url(r'^e/(?P<slug>[-\w]+)/$', views.TalkListUpdateView.as_view(), name='update'),
        url(r'^r/(?P<slug>[-\w]+)/$', views.TalkListRemoveView.as_view(), name='remove'),
        )

urlpatterns = patterns(
        '',
        url(r'^lists/', include(list_patterns, namespace='lists')),
        )
