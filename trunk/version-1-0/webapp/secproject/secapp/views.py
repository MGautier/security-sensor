# coding=utf-8
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.utils import timezone
from datetime import time, datetime, timedelta, date
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.renderers import JSONRenderer
from .models import LogSources, Events, Ips, PacketEventsInformation, PacketAdditionalInfo, Visualizations
from iptables import Iptables
from rest_framework import generics
from serializers import EventsSerializer, VisualizationsSerializer
from calendar import Calendar
from types import *
import threading


# Class

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class VisualizationsInformation(generics.RetrieveAPIView):
    queryset = Visualizations.objects.all()
    serializer_class = VisualizationsSerializer
    http_method_names = ['get', 'post', ]

    @csrf_exempt
    def list_of_visualizations(self, request, format=None):
        """
        Lista de todas las entradas de la tabla visualizations en formato json. Esto me será útil para la generación
        de la tabla de eventos por día, de la cuál luego podré amplicar información con api/events o similares.
        :param request:
        :param pk:
        :param format:
        :return:
        """

        if request.method == 'GET':
            serializer = VisualizationsSerializer(Visualizations.objects.all(), many=True)
            return JSONResponse(serializer.data)

    @csrf_exempt
    def list_of_visualizations_week(self, request, format=None):
        """

        :param request:
        :param format:
        :return:
        """

        if request.method == 'GET':

            calendary = Calendar(0)
            today = timezone.localtime(timezone.now())
            week = []
            next_first_month_week = [] #Utilizo esta variable para almacenar la primera semana del siguiente mes
            events_day_week = []

            for it in calendary.monthdayscalendar(today.year, today.month):

                if it.count(today.day) == 1:
                    week = it

            for it in calendary.monthdayscalendar(today.year, today.month+1):

                if it.count(1) == 1:
                    next_first_month_week = it


            for it in week:
                if not it == 0:
                    date_week = datetime(today.year, today.month, it)
                    print "DATE_WEEK_ACTUAL:",date_week
                    try:
                        serializer = VisualizationsSerializer(Visualizations.objects.filter(Date=date_week), many=True)

                        if serializer.data:
                            for it_list in serializer.data:
                                events_day_week.append(it_list)

                    except Visualizations.DoesNotExist:
                        pass

            for it in next_first_month_week:
                if not it == 0:
                    date_week = datetime(today.year, today.month+1, it)
                    print "DATE_WEEK_NEXT_MONTH:",date_week
                    try:
                        serializer = VisualizationsSerializer(Visualizations.objects.filter(Date=date_week), many=True)

                        if serializer.data:
                            for it_list in serializer.data:
                                events_day_week.append(it_list)

                    except Visualizations.DoesNotExist:
                        pass

                    
        return JSONResponse([result for result in events_day_week])

    @csrf_exempt
    def visualizations_chart(self, request, format=None):
        """

        :param request:
        :param format:
        :return:
        """

        if request.method == 'GET':

            calendary = Calendar(0)
            today = timezone.localtime(timezone.now())
            week = []
            events_day_week = []
            events_per_day = {}
            list_events = []
            next_first_month_week = []

            for it in calendary.monthdayscalendar(today.year, today.month):

                if it.count(today.day) == 1:
                    week = it

            for it in calendary.monthdayscalendar(today.year, today.month+1):

                if it.count(1) == 1:
                    next_first_month_week = it


            for it in week:
                if not it == 0:
                    date_week = datetime(today.year, today.month, it)

                try:
                    serializer = VisualizationsSerializer(Visualizations.objects.filter(Date=date_week), many=True)

                    if serializer.data:
                        for it_list in serializer.data:
                            events_day_week.append(it_list)
                            try:

                                if events_per_day['day'] == it_list['Name_Day']:
                                    events_sum = it_list['Process_Events'] + events_per_day['events']
                                    events_per_day = {
                                        "events": events_sum,
                                        "day": it_list['Name_Day'],
                                        "date": it_list['Date'],
                                        "id_source": it_list['ID_Source']
                                    }
                                else:
                                    if events_per_day:
                                        list_events.append(events_per_day)

                                    events_per_day = {
                                        "events": it_list['Process_Events'],
                                        "day": it_list['Name_Day'],
                                        "date": it_list['Date'],
                                        "id_source": it_list['ID_Source']
                                    }
                            except KeyError:
                                events_per_day = {
                                    "events": it_list['Process_Events'],
                                    "day": it_list['Name_Day'],
                                    "date": it_list['Date'],
                                    "id_source": it_list['ID_Source']
                                }

                except Visualizations.DoesNotExist:
                    pass

            for it in next_first_month_week:
                if not it == 0:
                    date_week = datetime(today.year, today.month+1, it)

                    try:
                        serializer = VisualizationsSerializer(Visualizations.objects.filter(Date=date_week), many=True)

                        if serializer.data:
                            for it_list in serializer.data:
                                events_day_week.append(it_list)
                                try:

                                    if events_per_day['day'] == it_list['Name_Day']:
                                        events_sum = it_list['Process_Events'] + events_per_day['events']
                                        events_per_day = {
                                            "events": events_sum,
                                            "day": it_list['Name_Day'],
                                            "date": it_list['Date'],
                                            "id_source": it_list['ID_Source']
                                        }
                                    else:
                                        if events_per_day:
                                            list_events.append(events_per_day)

                                        events_per_day = {
                                            "events": it_list['Process_Events'],
                                            "day": it_list['Name_Day'],
                                            "date": it_list['Date'],
                                            "id_source": it_list['ID_Source']
                                        }
                                except KeyError:
                                    events_per_day = {
                                        "events": it_list['Process_Events'],
                                        "day": it_list['Name_Day'],
                                        "date": it_list['Date'],
                                        "id_source": it_list['ID_Source']
                                    }

                    except Visualizations.DoesNotExist:
                        pass
                

            list_events.append(events_per_day)

        return JSONResponse([result for result in list_events])


class EventsInformation(generics.RetrieveAPIView):
    # Desde esta clase podemos mostrar la api rest visual. Con cada método tenemos acceso a diferente
    # informacion mostrada en formato json.

    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    http_method_names = ['get', 'post', ]

    @csrf_exempt
    def events_by_source(self, request, pk, format=None):
        """

        :param request:
        :param pk:
        :param format:
        :return:
        """

        if request.method == 'GET':
            serializer = EventsSerializer(Events.objects.filter(ID_Source=pk), many=True)
            return JSONResponse(serializer.data)

    @csrf_exempt
    def events_by_source_detail(self, request, pk, fk, format=None):
        """

        :param request:
        :param pk:
        :param fk:
        :param format:
        :return:
        """

        if request.method == 'GET':
            return EventsInformation().event_detail(request, fk, format)

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
        :param pk: Identificador del Log_Source (1:Iptables ,...)
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

            list = []
            events_per_hour = {}

            for it in events_source:
                if it.Timestamp >= last_hour:
                    if it.Timestamp < today:
                        hour = timezone.localtime(it.Timestamp).hour
                        day = it.Timestamp.strftime("%Y-%m-%d")
                        events_in_hour = 0
                        try:
                            events_in_hour = events_per_hour[hour]
                        except KeyError:
                            if events_per_hour:
                                list.append(events_per_hour)
                            events_per_hour = {hour: 0, "day": day}

                        events_per_hour[hour] = events_in_hour + 1

            list.append(events_per_hour)

            return JSONResponse([result for result in list])

    @csrf_exempt
    def events_source_in_day(self, request, pk, format=None):
        """
        Lista todos los eventos de ese día
        :param request:
        :param pk:
        :param format:
        :return:
        """

        events_in_day = 0

        if type(pk) is DictType:
            _pk = pk['pk']
            day = pk['day']
            month = pk['month']
            year = pk['year']
            events_in_day = pk['events_db']
        else:
            _pk = pk

        if not events_in_day:
            try:
                events_in_day = Events.objects.filter(ID_Source=_pk)
            except Events.DoesNotExist:
                return HttpResponse(status=404)

        if request.method == 'GET':

            local_today = timezone.localtime(timezone.now())
            if type(pk) is DictType:
                today = datetime(year, month, day, tzinfo=timezone.get_current_timezone())
            else:
                today = datetime(local_today.year, local_today.month, local_today.day,
                                 tzinfo=timezone.get_current_timezone())

            list_hours = []
            events_per_hour = {}

            for it in events_in_day:
                local_timestamp = timezone.localtime(it.Timestamp)
                date_timestamp = datetime(
                    local_timestamp.year,
                    local_timestamp.month,
                    local_timestamp.day,
                    tzinfo=timezone.get_current_timezone()
                )
                hour = local_timestamp.hour

                if date_timestamp == today:
                    events_in_hour = 0
                    try:
                        events_in_hour = events_per_hour[hour]
                    except KeyError:
                        if events_per_hour:
                            list_hours.append(events_per_hour)
                        events_per_hour = {hour: 0, "day": today.strftime("%Y-%m-%d")}

                    events_per_hour[hour] = events_in_hour + 1

            list_hours.append(events_per_hour)

            if type(pk) is DictType:
                return [result for result in list_hours]
            else:
                return JSONResponse([result for result in list_hours])

    @csrf_exempt
    def events_source_in_week(self, request, pk, format=None):
        """
        Lista todos los eventos de la semana en la que nos encontramos
        :param request:
        :param pk:
        :param format:
        :return:
        """

        _pk = 0
        list_week = []
        list_events_week = []
        calendary = Calendar(0)
        today = timezone.localtime(timezone.now())
        year = today.year
        month = today.month
        events_in_week = 0

        if type(pk) is DictType:
            _pk = pk['pk']
            list_week = pk['list_week']
            month = pk['month']
            year = pk['year']
            events_in_week = pk['events_db']
        else:
            _pk = pk
            for it in calendary.monthdayscalendar(today.year, today.month):
                try:
                    if it.index(today.day):
                        list_week = it
                except ValueError:
                    pass

        if not events_in_week:
            try:
                events_in_week = Events.objects.filter(ID_Source=_pk)
            except Events.DoesNotExist:
                return HttpResponse(status=404)

        if request.method == 'GET':

            for it in list_week:
                if not it == 0:
                    dict_day = {'day': it, 'pk': _pk, 'year': year, 'month': month, 'events_db': events_in_week}
                    list_events_week.append(EventsInformation().events_source_in_day(request, dict_day))

            result = []  # Esta lista es para el uso interno de las otras funciones de la clase
            result_json = []  # Esta lista es para dar más información al json de la api
            count = 0
            for it in list_events_week:
                count += 1
                result_json.append({'day_week': count, 'events': it})
                for it_dict in it:
                    if it_dict:
                        result.append(it_dict)

            if type(pk) is DictType:
                return result
            else:
                return JSONResponse(result_json)

    @csrf_exempt
    def events_source_in_month(self, request, pk, format=None):
        """
        Lista todos los eventos de una source en el mes actual
        :param request:
        :param pk:
        :param format:
        :return:
        """

        list_events_month = []
        calendary = Calendar(0)
        today = timezone.localtime(timezone.now())
        year = today.year
        month = today.month
        events_in_month = 0

        if type(pk) is DictType:
            _pk = pk['pk']
            list_month = pk['list_month']
            month = pk['month']
            year = pk['year']
            events_in_month = pk['events_db']
        else:
            _pk = pk
            list_month = calendary.monthdayscalendar(today.year, today.month)

        if not events_in_month:
            try:
                events_in_month = Events.objects.filter(ID_Source=_pk)
            except Events.DoesNotExist:
                return HttpResponse(status=404)

        if request.method == 'GET':

            for it in list_month:
                dict_month = {'pk': _pk, 'list_week': it, 'year': year, 'month': month, 'events_db': events_in_month}
                list_events_month.append(EventsInformation().events_source_in_week(request, dict_month))

            result = []
            count = 0
            for it in list_events_month:
                count += 1
                result.append({'week': count, 'days': it})

            if type(pk) is DictType:
                return result
            else:
                return JSONResponse(result)

    @csrf_exempt
    def events_source_in_year(self, request, pk, format=None):
        """
        Lista los eventos de una source durante el año actual
        :param request:
        :param pk:
        :param format:
        :return:
        """

        calendary = Calendar(0)
        today = timezone.localtime(timezone.now())
        list_month_year = []
        year = today.year

        try:
            events_in_year = Events.objects.filter(ID_Source=pk)
        except Events.DoesNotExist:
            return HttpResponse(status=404)

        calendary_year = calendary.yeardayscalendar(today.year)
        # Esta variable almacena la información en 4 listas de la siguiente manera:
        # - Primera lista: 3 meses del año (Empezando en Enero)
        # - Segunda lista: 1 mes completo dividido en 4-6 listas de semanas (lista que se pasa a la funcion interna
        # de la clase events_source_in_month)
        # - Tercera lista: dias del mes por semana
        # - Cuarta lista: dias de la semana

        count_month = 0
        for it in calendary_year:
            for it_month in it:
                count_month += 1
                dict_year = {'pk': pk, 'list_month': it_month, 'year': year, 'month': count_month,
                             'events_db': events_in_year}
                list_month_year.append(EventsInformation().events_source_in_month(request, dict_year))

        result = []
        count = 0

        for it in list_month_year:
            count += 1
            result.append({'month': count, 'weeks': it})

        print "RESULT: ", result

        return JSONResponse(result)

    @csrf_exempt
    def events_source_last_day(self, request, pk, format=None):
        """
        Lista todos los eventos de cada hora para una source en las últimas 24 horas
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
                        day = it.Timestamp.strftime("%Y-%m-%d")
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
                            events_per_hour = {hour: 0, "day": day}
                            events_in_hour = 0

                        events_per_hour[hour] = events_in_hour + 1

            list.append(events_per_hour)
            # Asigno el último registro ya que no da la vuelta al bucle de nuevo y quedaría sin asignar
            # a la lista

            return JSONResponse([result for result in list])

    @csrf_exempt
    def events_list_in_day(self, request, pk, day, month, year, format=None):
        """
        Lista todos los eventos de cada hora para una source en las últimas 24 horas
        :param request:
        :param pk:
        :param day:
        :param month:
        :param year:
        :param format:
        :return:
        """

        events_list = []

        try:
            events_list_in_day = Events.objects.filter(ID_Source=pk)
        except Events.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':

            for it in events_list_in_day:
                if it.Timestamp.year == int(year) and it.Timestamp.month == int(month) and it.Timestamp.day == int(day):
                    events_list.append(it)

            serializer = EventsSerializer(events_list,  many=True)
            return JSONResponse(serializer.data)

# Methods


def index(request):
    exist_thread = False

    for threads in threading.enumerate():

        test = Iptables(args=(1,),
                        source={'T': 'Firewall', 'M': 'iptables', 'P': '/var/log/iptables.log',
                                'C': './secapp/kernel/conf/iptables-conf.conf'})
        if type(threads) == type(test):
            exist_thread = True

    if not exist_thread:
        thread_iptables = Iptables(args=(1,),
                                   source={'T': 'Firewall', 'M': 'iptables', 'P': '/var/log/iptables.log',
                                           'C': './secapp/kernel/conf/iptables-conf.conf'})
        thread_iptables.start()

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
