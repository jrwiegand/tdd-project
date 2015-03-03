from django.conf.urls import patterns, url

login = 'accounts.views.persona_login'
logout = 'django.contrib.auth.views.logout'

urlpatterns = patterns('',
   url(r'^login$', login, name='persona_login'),
   url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
)
