# coding=utf-8
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.utils import timezone
from datetime import time, datetime, timedelta
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.renderers import JSONRenderer
from .models import LogSources, Events, Ips, PacketEventsInformation, PacketAdditionalInfo
from iptables import Iptables
from rest_framework import generics
from serializers import EventsSerializer


# Class

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class EventsInformation(generics.RetrieveUpdateDestroyAPIView):

    # Desde esta clase podemos mostrar la api rest visual. Con cada método tenemos acceso a diferente
    # informacion mostrada en formato json.

    queryset = Events.objects.all()
    serializer_class = EventsSerializer

    @csrf_exempt
    def events_list(self, request, format=None):
        """
        Lista todos los eventos de la bd en formato JSON.
        :param request:
        :param format:
        :return:
        """

        if request.method == 'GET':
            serializer = EventsSerializer(Events.objects.all(), many=True)
            return JSONResponse(serializer.data)

    @csrf_exempt
    def event_detail(self, request, pk, format=None):
        """
        Lista el evento mediante su identificador, si se encuentra en la bd,
        en formato JSON
        :param pk:
        :param request:
        :param format:
        :return:
        """

        try:
            details = Events.objects.get(pk=pk)
        except Events.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = EventsSerializer(details)
            return JSONResponse(serializer.data)

    @csrf_exempt
    def events_source_per_hour(self, request, id_source, format=None):
        """
        Lista el número de eventos de cada hora del día para mostrarlos en las gráficas
        :param request:
        :param id_source:
        :param format:
        :return:
        """

        try:
            events_source = Events.objects.filter(ID_Source=id_source)
        except Events.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = EventsSerializer(events_source, many=True)
            return JSONResponse(serializer.data)

    @csrf_exempt
    def events_source_last_day(self, request, id_source, format=None):
        """
        Lista todo los eventos de cada hora para una source en las últimas 24 horas
        :param request:
        :param id_source:
        :param format:
        :return:
        """

        try:
            events_source_last_day = Events.objects.filter(ID_Source=id_source)
        except Events.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            today = timezone.now()
            yesterday = today - timedelta(hours=24)

            events_per_hour = {}
            # Inserto las horas en las que las franjas de tiempo entre hoy y ayer hubo algún evento

            for it in events_source_last_day:
                if it.Timestamp < today:
                    if not it.Timestamp < yesterday:
                        hour = timezone.localtime(it.Timestamp).hour
                        try:
                            events_in_hour = events_per_hour['hour']
                        except KeyError:
                            events_in_hour = 0

                        events_per_hour = {hour: events_in_hour + 1}

            serializer = EventsSerializer(events_source_last_day, many=True)
            return JSONResponse(serializer.data)


# Methods


def index(request):

    test = Iptables(args=(1,),
                    source={'T': 'Firewall', 'M': 'iptables', 'P': '/var/log/iptables.log',
                            'C': './secapp/kernel/conf/iptables-conf.conf'})
    test.start()
    latest_source_list = LogSources.objects.order_by('id')[:3]
    context = {'latest_source_list': latest_source_list}
    if request.GET.get('run-btn'):
        hello = int(request.GET.get('textbox'))
        context.update({'hello': hello})

    return render(request, 'secapp/index.html', context)


def events(request, id_log_source):

    log_source = get_object_or_404(LogSources, pk=id_log_source)
    events_list = get_list_or_404(Events, ID_Source_id=id_log_source)
    event = get_object_or_404(Events, pk=id_log_source)
    context = {'event': event, 'events_list': events_list, 'log_source': log_source}

    if request.method == 'POST' and request.is_ajax():
        data = {"event": event}
        return JsonResponse(data)

    return render(request, 'secapp/events.html', context)


@csrf_protect
def event_information(request, id_log_source, id_event):
    # response = "You're looking at the log_source of event %s. "
    # return HttpResponse(response % id_source)

    log_source = get_object_or_404(LogSources, pk=id_log_source)
    event = get_object_or_404(Events, pk=id_event)
    packet_event_information = get_object_or_404(PacketEventsInformation, pk=id_event)
    context = {
        'log_source': log_source,
        'event': event,
        'packet_event_information': packet_event_information,
    }
    return render(request, 'secapp/event_information.html', context)


def additional_info(request, id_log_source, id_event):
    """

    :param id_event:
    :param request:
    :param id_log_source:
    """

    log_source = get_object_or_404(LogSources, pk=id_log_source)
    event = get_object_or_404(Events, pk=id_event)
    packet_event_information = get_object_or_404(PacketEventsInformation, pk=id_event)
    packet_additional_info = get_list_or_404(PacketAdditionalInfo, ID_Packet_Events=packet_event_information)
    context = {
        'log_source': log_source,
        'event': event,
        'packet_additional_info': packet_additional_info,
    }

    return render(request, 'secapp/additional_info.html', context)




