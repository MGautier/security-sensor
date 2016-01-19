from django.conf.urls import url

from . import views

app_name = 'secapp'
urlpatterns = [
    # Index view
    url(r'^$', views.index, name='index'),

    # List of events for a Log Source
    url(r'^(?P<id_log_source>[0-9]+)/event/$', views.events, name='events'),

    # Packet of an event (for a Log Source)
    url(r'^(?P<id_log_source>[0-9]+)/event/(?P<id_event>[0-9]+)$', views.event_information,
        name='event_information'),

    # Additional information about a packet event
    url(r'^(?P<id_log_source>[0-9]+)/event/(?P<id_event>[0-9]+)/additional_info/$',
        views.additional_info,
        name='additional_info'),

]
