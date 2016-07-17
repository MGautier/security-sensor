from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# Author: Moises Gautier Gomez
# Proyecto fin de carrera - Ing. en Informatica
# Universidad de Granada

app_name = 'secapp'
urlpatterns = [
    # Vista Index
    url(r'^$', views.index, name='index'),

    # Listado de eventos segun la fuente (Source)

    url(r'^(?P<id_log_source>[0-9]+)/event/$', views.events, name='events'),

    # Informacion del paquete asociado a un evento segun la fuente

    url(r'^(?P<id_log_source>[0-9]+)/event/(?P<id_event>[0-9]+)$', views.event_information,
        name='event_information'),

    # Informacion adicional de un paquete asociado a un evento

    url(r'^(?P<id_log_source>[0-9]+)/event/(?P<id_event>[0-9]+)/additional_info/$',
        views.additional_info,
        name='additional_info'),

    # Listado de eventos en formato json almacenados en el sistema para cualquier tipo de fuente (source)

    url(r'^api/events/$', views.EventsInformation().events_list, name='events_list'),

    # Listado de eventos en formato json almacenados en el sistema para una fuente determinada

    url(r'^api/events/by_source/(?P<pk>[0-9]+)/$', views.EventsInformation().events_by_source,
        name='events_by_source'),

    # Evento en formato json almacenado en el sistema para una fuente determinada

    url(r'^api/events/by_source/(?P<pk>[0-9]+)/(?P<fk>[0-9]+)/$', views.EventsInformation().events_by_source_detail,
        name='events_by_source_detail'),

    # Descripcion adicional de un evento en formato json

    url(r'^api/events/(?P<pk>[0-9]+)/additional$', views.EventsInformation().events_detail_additional,
        name='event_detail_additional'),

    # Descripcion detallada de un evento en formato json

    url(r'^api/events/(?P<pk>[0-9]+)/json$', views.EventsInformation().event_detail, name='event_detail'),

    # Descripcion detalla de un evento en formato restfull (api django-rest)

    url(r'^api/events/(?P<pk>[0-9]+)/$', views.EventsInformation.as_view()),

    # Lista el numero de eventos de una hora del dia para mostrarlos en las graficas

    url(r'^api/events/hour/(?P<pk>[0-9]+)/$', views.EventsInformation().events_source_in_hour,
        name='events_source_in_hour'),

    # Lista todos los eventos almacenados para un dia

    url(r'^api/events/day/(?P<pk>[0-9]+)/$', views.EventsInformation().events_source_in_day,
        name='events_source_in_day'),

    # Lista todos los eventos de cada hora para una source en las ultimas 24 horas

    url(r'^api/events/day/(?P<pk>[0-9]+)/(?P<year>[0-9][0-9][0-9][0-9]+)-(?P<month>[0-9][0-9]+)-(?P<day>[0-9][0-9]+)/$',
        views.EventsInformation().events_list_in_day, name='events_list_in_day'),

    # Lista todos los eventos almacenados para la semana actual para una determinada fuente

    url(r'^api/events/week/(?P<pk>[0-9]+)/$', views.EventsInformation().events_source_in_week,
        name='events_source_in_week'),

    # Lista todos los eventos almacenados para el mes actual para una determinada fuente
    url(r'^api/events/month/(?P<pk>[0-9]+)/$', views.EventsInformation().events_source_in_month,
        name='events_source_in_month'),

    # Lista todos los eventos almacenados para el year actual para una determinada fuente

    url(r'^api/events/year/(?P<pk>[0-9]+)/$', views.EventsInformation().events_source_in_year,
        name='events_source_in_year'),

    # Lista todos los evento almacenados para el dia anterior a hoy para una determinada fuente

    url(r'^api/events/last_day/(?P<pk>[0-9]+)/$', views.EventsInformation().events_source_last_day,
        name='events_source_last_day'),

    # Lista de todas las entradas de la tabla visualizations en formato json.

    url(r'^api/visualizations/$', views.VisualizationsInformation().list_of_visualizations,
        name='visualizations_list'),

    # Lista de todas las entradas de la tabla visualizations en formato json para la semana actual

    url(r'^api/visualizations/week/$', views.VisualizationsInformation().list_of_visualizations_week,
        name='visualizations_list_week'),

    # Lista de todas las entradas de eventos por dia almacenados para mostrar en la grafica principal

    url(r'^api/visualizations/chart/$', views.VisualizationsInformation().visualizations_chart,
        name='visualizations_chart')

]

urlpatterns = format_suffix_patterns(urlpatterns)
