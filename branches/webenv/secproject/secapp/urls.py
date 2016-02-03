from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
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

    url(r'^api/events/(?P<pk>[0-9]+)/json$', views.EventsInformation().event_detail, name='event_detail'),

    url(r'^api/events/(?P<pk>[0-9]+)/$', views.EventsInformation.as_view()),

    url(r'^api/events/$', views.EventsInformation().events_list, name='events_list'),

    url(r'^api/events/hour/(?P<pk>[0-9]+)/$', views.EventsInformation().events_source_in_hour,
        name='events_source_in_hour'),

    url(r'^api/events/last_day/(?P<pk>[0-9]+)/$', views.EventsInformation().events_source_last_day,
        name='events_source_last_day'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
