from __future__ import absolute_import

from django.conf.urls import patterns, url, include
from . import views

list_patterns = patterns(
        '',
        url(r'^$', views.TalkListListView.as_view(), name='list'),
        url(r'^d/(?P<slug>[-\w]+)/$', views.TalkListDetailView.as_view(),
            name='detail'),
        )
urlpatterns = patterns(
        '',
        url(r'^lists/', include(list_patterns, namespace='lists')),
        )
