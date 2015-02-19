from django.conf.urls import patterns, url
from .views import NewListView, ViewAndAddToList

urlpatterns = patterns('',
    url(r'^(\d+)/$', ViewAndAddToList.as_view(), name='view_list'),
    url(r'^new$', 'lists.views.new_list', name='new_list'),
    url(r'^users/(.+)/$', 'lists.views.my_lists', name='my_lists'),
    url(r'^(\d+)/share$', 'lists.views.share_list', name='share_list'),
)
