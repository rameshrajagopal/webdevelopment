
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .views import HomePageView, SignUpView, LoginView, logoutView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myguide.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^accounts/register/$', SignUpView.as_view(), name='signup'),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', logoutView, name='logout'),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^talks/', include('talks.urls', namespace='talks')),
    url(r'^admin/', include(admin.site.urls)),
)
