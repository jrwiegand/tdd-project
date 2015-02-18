from django.conf.urls import patterns, url
from .views import NewListView

urlpatterns = patterns('',
    url(r'^(\d+)/$', 'lists.views.view_list', name='view_list'),
    url(r'^new$', NewListView.as_view(), name='new_list'),
    url(r'^users/(.+)/$', 'lists.views.my_lists', name='my_lists'),
    url(r'^(\d+)/share$', 'lists.views.share_list', name='share_list'),
)
