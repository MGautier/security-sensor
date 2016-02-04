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
    def events_source_in_hour(self, request, pk, format=None):
        """
        Lista el número de eventos de una hora del día para mostrarlos en las gráficas. La franja de tiempo ira desde
        la hora actual hasta una hora menos de la actual.
        :param request:
        :param pk:
        :param format:
        :return:
        """

        try:
            events_source = Events.objects.filter(ID_Source=pk)
        except Events.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            today = timezone.localtime(timezone.now())
            last_hour = today - timedelta(hours=1)

            events_per_hour = {}

            for it in events_source:
                if it.Timestamp >= last_hour:
                    if it.Timestamp < today:
                        try:
                            events_in_hour = events_per_hour[today.hour]
                        except KeyError:
                            events_in_hour = 0

                        events_per_hour = {today.hour: events_in_hour + 1}

            return JSONResponse(events_per_hour)

    @csrf_exempt
    def events_source_last_day(self, request, pk, format=None):
        """
        Lista todo los eventos de cada hora para una source en las últimas 24 horas
        :param request:
        :param pk:
        :param format:
        :return:
        """

        try:
            events_source_last_day = Events.objects.filter(ID_Source=pk)
        except Events.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            today = timezone.localtime(timezone.now())
            yesterday = today - timedelta(hours=24)

            list = []
            events_per_hour = {}

            # Inserto las horas en las que las franjas de tiempo entre hoy y ayer hubo algún evento
            for it in events_source_last_day:

                local_time = timezone.localtime(it.Timestamp)
                # Saco la hora local del Timestamp insertado en la bd. Comparo las horas antes de la actual
                # y despues de 24 horas antes de la actual

                if local_time <= today:
                    if local_time >= yesterday:
                        hour = local_time.hour
                        # Compruebo si hay algún registro de una hora similar en el diccionario, para crear
                        # un nuevo registro o no. Luego asigno este diccionario a una lista y dado que
                        # en la lista introduzo una instancia u objeto diccionario, cuando fuera de ella se
                        # modifique, también lo hará internamente:
                        # dic = {"ex": 1}
                        # list.append(dic) list -> [{"ex": 1}]
                        # dic['ex'] = 2
                        # list -> [{"ex": 2}]
                        try:
                            events_in_hour = events_per_hour[hour]
                        except KeyError:
                            if events_per_hour:
                                list.append(events_per_hour)
                            events_per_hour = {hour: 0}
                            events_in_hour = 0

                        events_per_hour[hour] = events_in_hour + 1

            list.append(events_per_hour)
            # Asigno el último registro ya que no da la vuelta al bucle de nuevo y quedaría sin asignar
            # a la lista

            return JSONResponse([result for result in list])


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




