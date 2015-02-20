from django.conf.urls import patterns, include, url
from lists.views import HomePageView

urlpatterns = patterns('',
                       url(r'^$', HomePageView.as_view(), name='home'),
                       url(r'^accounts/', include('accounts.urls')),
                       url(r'^lists/', include('lists.urls')),
                       )
