from django.conf.urls import url

from . import views

urlpatterns = [
    # Index view
    url(r'^$', views.index, name='index'),

    # Events description
    url(r'^(?P<id_event>[0-9]+)/$', views.events, name='events'),

    # Log sources description
    url(r'^(?P<id_source>[0-9]+)/sources/$', views.log_sources, name='log_sources'),

    # Ips description
    url(r'^(?P<id_ip>[0-9]+)/ips/$', views.ips, name='ips'),
]
