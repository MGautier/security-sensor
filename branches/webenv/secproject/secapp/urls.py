from django.conf.urls import url

from . import views

app_name = 'secapp'
urlpatterns = [
    # Index view
    url(r'^$', views.index, name='index'),

    # Events description
    url(r'^event/(?P<id_event>[0-9]+)/$', views.events, name='events'),

    # Log sources description
    url(r'^event/(?P<id_source>[0-9]+)/sources/$', views.sources, name='sources'),

    # Ips description
    url(r'^event/(?P<id_ip>[0-9]+)/ips/$', views.ips, name='ips'),
]
