# coding=utf-8
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.renderers import JSONRenderer
from .models import LogSources, Events, PacketEventsInformation, PacketAdditionalInfo, Visualizations, Tags
from rest_framework import generics
from serializers import EventsSerializer, VisualizationsSerializer
from calendar import Calendar
import itertools
from types import *


class JSONResponse(HttpResponse):
    """
    Clase que recibe como parametro un objeto HttpResponse cuyo contenido se renderiza o transforma en formato
    JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class VisualizationsInformation(generics.RetrieveAPIView):
    """
    Clase que se emplea para la renderización de datos extraidos del modelo (Base de datos) junto con informacion
    pasada por protocolo Http (peticion GET/POST) para visualizar contenido en formato JSON en la web.
    """

    queryset = Visualizations.objects.all()
    serializer_class = VisualizationsSerializer
    http_method_names = ['get', 'post', ]

    @csrf_exempt
    def list_of_visualizations(self, request):
        """
        Lista de todas las entradas de la tabla visualizations en formato json. Esto me será útil para la generación
        de la tabla de eventos por día, de la cuál luego podré extraer información con api/events o similares.
        Args:
            request: Peticion http (normalmente GET)

        Returns: Muestra en formato JSON todos los items del modelo Visualizations

        """

        if request.method == 'GET':
            serializer = VisualizationsSerializer(Visualizations.objects.all(), many=True)
            return JSONResponse(serializer.data)

    @csrf_exempt
    def list_of_visualizations_week(self, request):
        """
        Lista de todas las entradas de la tabla visualizations en formato json (para la semana actual). Esto me será
        útil para la generación de la tabla de eventos por día, de la cuál luego podré extraer información con
        api/events o similares.
        Args:
            request: Peticion http (normalmente GET)

        Returns: Muestra en formato JSON todos los items del modelo Visualization para la semana actual
        Ejemplo:
        {
        "id":56,
        "Week_Month":1,
        "Week_Day":2,
        "Name_Day":"Wednesday",
        "Date":"2016-06-08",
        "Hour":21,
        "Process_Events":68,
        "ID_Source":1
        }

        """

        if request.method == 'GET':

            # Almacenamos un objeto de la clase Calendar que representa todos los dias del year.
            calendary = Calendar(0)
            # Almacenamos el dia actual en formato date mediante un paquete del framework Django
            today = timezone.localtime(timezone.now())
            # Lista de la semana actual que coincide con el dia actual
            week = []
            # Lista de la primera semana del mes actual
            first_week = []
            for it in calendary.monthdayscalendar(today.year, today.month):
                if it.count(1) == 1:
                    first_week = it
                if it.count(today.day) == 1:
                    week = it

            # Lista de la semana actual con los eventos que se relacionan
            events_day_week = []

            # Compruebo si el dia de la semana esta entre los 7 primeros por si es necesario obtener los dias
            # del mes anterior para la visualizacion de eventos en la grafica

            if 1 <= today.day <= 7 and week == first_week:

                len_month = len(calendary.monthdayscalendar(today.year, today.month - 1))

                for it in calendary.monthdayscalendar(today.year, today.month - 1)[len_month - 1]:
                    if not it == 0:
                        date_week = datetime(today.year, today.month - 1, it)

                        try:
                            serializer = VisualizationsSerializer(Visualizations.objects.filter(Date=date_week),
                                                                  many=True)

                            if serializer.data:
                                for it_list in serializer.data:
                                    events_day_week.append(it_list)

                        except Visualizations.DoesNotExist:
                            pass

            for it in week:
                if not it == 0:
                    date_week = datetime(today.year, today.month, it)

                    try:
                        serializer = VisualizationsSerializer(Visualizations.objects.filter(Date=date_week), many=True)

                        if serializer.data:
                            for it_list in serializer.data:
                                events_day_week.append(it_list)

                    except Visualizations.DoesNotExist:
                        pass

        return JSONResponse([result for result in events_day_week])

    @csrf_exempt
    def visualizations_chart_all(self, request, pk, format=None):
        """
        Lista de todas las entradas de la tabla visualizations en formato json. Esto me será
        útil para la generación de la tabla de eventos por día, de la cuál luego podré extraer información con
        api/events o similares.
        Args:
            request: Peticion http (normalmente GET)
            pk: Identificador de la fuente de la que queremos extraer los eventos
            format:

        Returns: Muestra en formato JSON todos los items del modelo Visualization
        Ejemplo
        {
        "date":"2016-06-08",
        "id_source":1,
        "events":68,
        "day":"Wednesday"
        }

        """
        if request.method == 'GET':

            # Diccionario con los eventos generados por dia
            events_per_day = {}
            list_events = []

            try:
                serializer = VisualizationsSerializer(Visualizations.objects.filter(ID_Source=pk), many=True)
                if serializer.data:
                    for it_list in serializer.data:
                        try:
                            dt = datetime.strptime(it_list['Date'], "%Y-%m-%d")

                            if events_per_day['Day'] == dt.day:
                                events_sum = it_list['Process_Events'] + events_per_day['Events']

                                events_per_day = {
                                    "Events": events_sum,
                                    "Name_Day": it_list['Name_Day'],
                                    "Date": it_list['Date'],
                                    "Day": dt.day,
                                    "Month": dt.month,
                                    "Year": dt.year,
                                    "ID_Source": it_list['ID_Source'],
                                    "id": it_list['id']
                                }
                            else:
                                if events_per_day:

                                    try:
                                        # Este if sirve para condicionar si existe un indice que
                                        # sea identico al dia que se va a introducir, es decir,
                                        # que ya existe una referencia en la lista para el nuevo dia.
                                        if list_events.index(events_per_day):
                                            pass
                                    except ValueError:
                                        list_events.append(events_per_day)

                                    events_per_day = {
                                        "Events": it_list['Process_Events'],
                                        "Name_Day": it_list['Name_Day'],
                                        "Date": it_list['Date'],
                                        "Day": dt.day,
                                        "Month": dt.month,
                                        "Year": dt.year,
                                        "ID_Source": it_list['ID_Source'],
                                        "id": it_list['id']
                                    }
                        except KeyError:
                            events_per_day = {
                                "Events": it_list['Process_Events'],
                                "Name_Day": it_list['Name_Day'],
                                "Date": it_list['Date'],
                                "Day": dt.day,
                                "Month": dt.month,
                                "Year": dt.year,
                                "ID_Source": it_list['ID_Source'],
                                "id": it_list['id']
                            }

            except Visualizations.DoesNotExist:
                pass

            list_events.append(events_per_day)

        return JSONResponse([result for result in list_events])

    @csrf_exempt
    def visualizations_chart(self, request, format=None):
        """
        Lista de todas las entradas de la tabla visualizations en formato json (para la semana actual). Esto me será
        útil para la generación de la tabla de eventos por día, de la cuál luego podré extraer información con
        api/events o similares.
        Args:
            request: Peticion http (normalmente GET)
            format:

        Returns: Muestra en formato JSON todos los items del modelo Visualization para la semana actual
        Ejemplo
        {
        "date":"2016-06-08",
        "id_source":1,
        "events":68,
        "day":"Wednesday"
        }

        """

        if request.method == 'GET':

            # Almacenamos un objeto de la clase Calendar que representa todos los días del year.
            calendary = Calendar(0)

            # Almacenamos el dia actual en formato date mediante un paquete del framework Django
            today = timezone.localtime(timezone.now())
            # Lista de la semana actual que coincide con el dia actual
            week = []
            # Lista de la primera semana del mes actual
            first_week = []
            for it in calendary.monthdayscalendar(today.year, today.month):
                if it.count(1) == 1:
                    first_week = it
                if it.count(today.day) == 1:
                    week = it

            # Diccionario con los eventos generados por dia
            events_per_day = {}
            list_events = []

            # Compruebo si el dia de la semana esta entre los 7 primeros por si es necesario obtener los dias
            # del mes anterior para la visualizacion de eventos en la grafica
            if 1 <= today.day <= 7 and week == first_week:

                len_month = len(calendary.monthdayscalendar(today.year, today.month - 1))

                for it in calendary.monthdayscalendar(today.year, today.month - 1)[len_month - 1]:

                    if not it == 0:
                        date_week = datetime(today.year, today.month - 1, it)

                        try:
                            serializer = VisualizationsSerializer(Visualizations.objects.filter(Date=date_week),
                                                                  many=True)

                            if serializer.data:
                                for it_list in serializer.data:

                                    try:

                                        if events_per_day['Day'] == it_list['Name_Day']:
                                            events_sum = it_list['Process_Events'] + events_per_day['Events']
                                            events_per_day = {
                                                "Events": events_sum,
                                                "Day": it_list['Name_Day'],
                                                "Date": it_list['Date'],
                                                "ID_Source": it_list['ID_Source'],
                                                "id": it_list['id']
                                            }
                                        else:
                                            if events_per_day:
                                                list_events.append(events_per_day)

                                            events_per_day = {
                                                "Events": it_list['Process_Events'],
                                                "Day": it_list['Name_Day'],
                                                "Date": it_list['Date'],
                                                "ID_Source": it_list['ID_Source'],
                                                "id": it_list['id']
                                            }
                                    except KeyError:
                                        events_per_day = {
                                            "Events": it_list['Process_Events'],
                                            "Day": it_list['Name_Day'],
                                            "Date": it_list['Date'],
                                            "ID_Source": it_list['ID_Source'],
                                            "id": it_list['id']
                                        }

                        except Visualizations.DoesNotExist:
                            pass

                list_events.append(events_per_day)

            for it in week:

                if not it == 0:
                    date_week = datetime(today.year, today.month, it)

                    try:
                        serializer = VisualizationsSerializer(Visualizations.objects.filter(Date=date_week), many=True)
                        if serializer.data:
                            for it_list in serializer.data:

                                try:

                                    if events_per_day['Day'] == it_list['Name_Day']:
                                        events_sum = it_list['Process_Events'] + events_per_day['Events']
                                        events_per_day = {
                                            "Events": events_sum,
                                            "Day": it_list['Name_Day'],
                                            "Date": it_list['Date'],
                                            "ID_Source": it_list['ID_Source'],
                                            "id": it_list['id']
                                        }
                                    else:
                                        if events_per_day:

                                            try:
                                                # Este if sirve para condicionar si existe un indice que
                                                # sea identico al dia que se va a introducir, es decir,
                                                # que ya existe una referencia en la lista para el nuevo dia.
                                                if list_events.index(events_per_day):
                                                    pass
                                            except ValueError:
                                                list_events.append(events_per_day)

                                        events_per_day = {
                                            "Events": it_list['Process_Events'],
                                            "Day": it_list['Name_Day'],
                                            "Date": it_list['Date'],
                                            "ID_Source": it_list['ID_Source'],
                                            "id": it_list['id']
                                        }
                                except KeyError:
                                    events_per_day = {
                                        "Events": it_list['Process_Events'],
                                        "Day": it_list['Name_Day'],
                                        "Date": it_list['Date'],
                                        "ID_Source": it_list['ID_Source'],
                                        "id": it_list['id']
                                    }

                    except Visualizations.DoesNotExist:
                        pass

            list_events.append(events_per_day)

        return JSONResponse([result for result in list_events])


class EventsInformation(generics.RetrieveAPIView):
    """
    Clase que visualiza los objetos almacenados en el modelo EventsInformation. Sus metodos los usaremos como parte
    del api restfull (json) de la aplicacion y tambien para la interaccion de las diferentes vistas disponibles.
    """

    # Tenemos que el conjunto de consultas de la clase se realizaran sobre los objetos de la clase Events
    queryset = Events.objects.all()
    # Instanciamos la clase EventsSeralizer que nos permite transformar objeto de tipo BD a manipulables por las
    # funciones internas de la clase
    serializer_class = EventsSerializer
    # Peticiones http permitidas para el uso de esta clase por parte de la aplicacion
    http_method_names = ['get', 'post', ]

    @csrf_exempt
    def events_by_source(self, request, pk):
        """
        Listado de eventos almacenados en el sistema para una determinada fuente.
        Args:
            request: Peticion http (normalmente GET)
            pk: Identificador de la fuente de la que queremos extraer los eventos

        Returns: Listado en formato JSON de todos los eventos de una fuente determinada

        """

        if request.method == 'GET':
            serializer = EventsSerializer(Events.objects.filter(ID_Source=pk), many=True)
            return JSONResponse(serializer.data)

    @csrf_exempt
    def events_by_source_detail(self, request, pk, fk, format=None):
        """
        Muestra el evento almacenado en el sistema para una determinada fuente.
        Args:
            request: Peticion http (normalmente GET)
            pk: Identificador de la fuente de la que queremos extraer el evento
            fk: Identificador del evento del cual queremos obtener mas informacion
            format:

        Returns: JSON con informacion del evento almacenado para una determinada fuente

        """

        if request.method == 'GET':
            return EventsInformation().event_detail(request, fk, format)

    @csrf_exempt
    def events_detail_additional(self, request, pk, format=None):
        """
        Muestra la informacion adicional de un evento almacenado en el sistema
        Args:
            request: Peticion http (normalmente GET)
            pk: Identificador del evento del cual queremos obtener mas informacion
            format:

        Returns: JSON con la informacion adicional del evento almacenado
        """

        try:
            event = Events.objects.get(pk=pk)
            packet_event = PacketEventsInformation.objects.get(id=event)
            packet_event_additional = PacketAdditionalInfo.objects.filter(ID_Packet_Events=packet_event)

        except Events.DoesNotExist:
            return HttpResponse(status=404)
        except PacketEventsInformation.DoesNotExist:
            return HttpResponse(status=404)
        except PacketAdditionalInfo.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':

            list_additional_info = []
            for it in packet_event_additional:
                fields = str(it).split('-')
                info = {"Tag": fields[0], "Description": fields[1], "Value": fields[2]}
                list_additional_info.append(info)

            return JSONResponse([result for result in list_additional_info])

    @csrf_exempt
    def packets(self, request, pk, day, month, year):
        """
        Muestra toda la información del paquete de un evento almacenado en el sistema
        Args:
            request: Peticion http (normalmente GET)
            pk: Identificador del evento del cual queremos obtener todo la informacion del paquete
            day: Valor entero que representa al dia de la fecha y cuyo formato es [0-9][0-9]
            month: Valor entero que representa al mes de la fecha y cuyo formato es [0-9][0-9]
            year: Valor entero que representa al year de la fecha y cuyo formato es {4}[0-9]

        Returns: JSON con la informacion del paquete completo del evento almacenado

        """

        events_list = []
        packet_result = []

        try:
            events_list_in_day = Events.objects.filter(ID_Source=pk)
        except Events.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':

            for it in events_list_in_day:
                if timezone.localtime(it.Timestamp).year == int(year) and \
                                timezone.localtime(it.Timestamp).month == int(month) and \
                                timezone.localtime(it.Timestamp).day == int(day):
                    events_list.append(it)

            serializer = EventsSerializer(events_list, many=True)

        if request.method == 'GET':

            for it in serializer.data:
                packet = {
                    "id": it['id'],
                    "Local_Timestamp": it['Local_Timestamp'],
                    "Timestamp": it['Timestamp'],
                    "Timestamp_Insertion": it['Timestamp_Insertion'],
                    "Comment": it['Comment'],
                    "ID_Source": it['ID_Source']
                }

                try:
                    event = Events.objects.get(pk=it['id'])
                    packet_event = PacketEventsInformation.objects.filter(id=event)

                    for it_packet_data in packet_event:
                        packet['IP_Source'] = str(it_packet_data.ID_IP_Source)
                        packet['IP_Destination'] = str(it_packet_data.ID_IP_Dest)
                        packet['Port_Source'] = str(it_packet_data.ID_Source_Port)
                        packet['Port_Destination'] = str(it_packet_data.ID_Dest_Port)
                        packet['Protocol'] = str(it_packet_data.Protocol)
                        packet['MAC_Source'] = str(it_packet_data.ID_Source_MAC)
                        packet['MAC_Destination'] = str(it_packet_data.ID_Dest_MAC)
                        packet['TAG'] = str(it_packet_data.TAG)

                except Events.DoesNotExist:
                    return HttpResponse(status=404)
                except PacketEventsInformation.DoesNotExist:
                    return HttpResponse(status=404)
                except PacketAdditionalInfo.DoesNotExist:
                    return HttpResponse(status=404)

                packet_result.append(packet)

            return JSONResponse([result for result in packet_result])

    @csrf_exempt
    def events_list(self, request):
        """
        Lista todos los eventos de la bd en formato JSON.
        Args:
            request: Peticion http (normalmente GET)

        Returns: JSON con informacion de todos los eventos del sistema sin discretizar por fuente

        """

        if request.method == 'GET':
            serializer = EventsSerializer(Events.objects.all(), many=True)
            return JSONResponse(serializer.data)

    @csrf_exempt
    def event_detail(self, request, pk):
        """
        Lista el evento mediante su identificador, si se encuentra en la bd, en formato JSON
        Args:
            request: Peticion http (normalmente GET)
            pk: Identificador del evento dentro de la BD

        Returns: JSON con informacion del evento almacenado en el sistema, en caso contrario un error 404

        """

        try:
            details = Events.objects.get(pk=pk)
        except Events.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = EventsSerializer(details)
            return JSONResponse(serializer.data)

    @csrf_exempt
    def events_source_in_hour(self, request, pk):
        """
        Lista el numero de eventos de una hora del día para mostrarlos en las graficas. La franja de tiempo ira desde
        la hora actual hasta una hora menos de la actual.
        Args:
            request: Peticion http (normalmente GET)
            pk: Identificador de la fuente (1:Iptables ,...)

        Returns: JSON con el numero de eventos ocurridos en la ultima hora para la fuente determinada

        """

        try:
            events_source = Events.objects.filter(ID_Source=pk)
        except Events.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            today = timezone.localtime(timezone.now())
            last_hour = today - timedelta(hours=1)

            list_events_in_hour = []
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
                                list_events_in_hour.append(events_per_hour)
                            events_per_hour = {hour: 0, "day": day}

                        events_per_hour[hour] = events_in_hour + 1

            list_events_in_hour.append(events_per_hour)

            return JSONResponse([result for result in list_events_in_hour])

    @csrf_exempt
    def events_source_in_day(self, request, pk):
        """
        Lista todos los eventos de ese dia para una determinada fuente
        Args:
            request: Peticion http (normalmente GET)
            pk: Identificador de la fuente (1:Iptables, ...) o diccionario dependiendo de si el metodo es
            consumido por la web o internamente por la aplicacion

        Returns: JSON con el numero de eventos ocurridos durante el dia actual discretizando por horas

        """

        # Creo esta variable a modo de global para que su ambito llege a todos los puntos del metodo
        events_in_day = 0

        # El diccionario representa a una estructura superior que ha invocado este metodo, como
        # events_source_in_week|month|year y por tanto ya sabemos informacion que ha sido pasada al metodo superior

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
    def events_source_in_week(self, request, pk):
        """
        Lista todos los eventos de la semana (7 dias) en la que nos encontramos actualmente
        Args:
            request: Peticion http (normalmente GET)
            pk: Identificador de la fuente (1:Iptables, ...) o diccionario dependiendo de si el metodo es
            consumido por la web o internamente por la aplicacion

        Returns: JSON con los eventos ocurridos durante la semana discretizando cada dia por las horas en las que han
        ocurrido los eventos.

        """

        list_week = []
        list_events_week = []
        calendary = Calendar(0)
        today = timezone.localtime(timezone.now())
        year = today.year
        month = today.month
        events_in_week = 0

        # El diccionario representa a una estructura superior que ha invocado este metodo, como
        # events_source_in_month|year y por tanto ya sabemos informacion que ha sido pasada al metodo superior

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
    def events_source_in_month(self, request, pk):
        """
        Lista todos los eventos de una fuente determinada para el mes actual.
        Args:
            request: Peticion http (normalmente GET)
            pk: Identificador de la fuente (1:Iptables, ...) o diccionario dependiendo de si el metodo es
            consumido por la web o internamente por la aplicacion

        Returns: JSON con los eventos ocurridos durante el mes discretizando por semanas, dias y en cada dia por horas
        en las que han sucedido los eventos de la fuente

        """

        list_events_month = []
        calendary = Calendar(0)
        today = timezone.localtime(timezone.now())
        year = today.year
        month = today.month
        events_in_month = 0

        # El diccionario representa a una estructura superior que ha invocado este metodo, como
        # events_source_in_year y por tanto ya sabemos informacion que ha sido pasada al metodo superior

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
    def events_source_in_year(self, request, pk):
        """
        [Metodo muy lento] Lista los eventos de una fuente determinada para el year actual.
        Args:
            request: Peticion http (normalmente GET)
            pk: Identificador de la fuente (1:Iptables, ...) o diccionario dependiendo de si el metodo es
            consumido por la web o internamente por la aplicacion

        Returns: JSON que contiene todos los meses del year en donde cada mes se divide por semanas y dias, y los dias
        se dividen por horas en las que ha sucedido cada evento

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

        return JSONResponse(result)

    @csrf_exempt
    def events_source_last_day(self, request, pk):
        """
        Lista todos los eventos de cada hora para una fuente determinada en las ultimas 24 horas contando desde la
        hora actual del sistema.
        Args:
            request: Peticion http (normalmente GET)
            pk: Identificador de la fuente (1:Iptables, ...)

        Returns: JSON con un listado de eventos por horas desde la hora actual hasta 24 horas atras en el tiempo.

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
    def events_list_in_day(self, request, pk, day, month, year):
        """
        Lista todos los eventos de una fecha para una fuente determinada.
        Args:
            request: Peticion http (normalmente GET)
            pk: Identificador de la fuente (1:Iptables, ...)
            day: Valor entero que representa al dia de la fecha y cuyo formato es [0-9][0-9]
            month: Valor entero que representa al mes de la fecha y cuyo formato es [0-9][0-9]
            year: Valor entero que representa al year de la fecha y cuyo formato es {4}[0-9]

        Returns: Listado en JSON con todos los eventos para esa fecha y fuente determinada

        """

        events_list = []

        try:
            events_list_in_day = Events.objects.filter(ID_Source=pk)
        except Events.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':

            for it in events_list_in_day:
                if timezone.localtime(it.Timestamp).year == int(year) and \
                                timezone.localtime(it.Timestamp).month == int(month) and \
                                timezone.localtime(it.Timestamp).day == int(day):
                    events_list.append(it)

            serializer = EventsSerializer(events_list, many=True)
            return JSONResponse(serializer.data)


# Metodos independientes de instancias de clase

def index(request):
    """
    Metodo interno de la clase Views que renderiza la vista index de la aplicacion
    Args:
        request: Peticion http (normalmente GET)

    Returns: Informacion en formato html (plantilla index.html) de la vista inicial de la aplicacion

    """

    latest_source_list = LogSources.objects.order_by('id')[:3]
    context = {'latest_source_list': latest_source_list}
    if request.GET.get('run-btn'):
        hello = int(request.GET.get('textbox'))
        context.update({'hello': hello})

    return render(request, 'secapp/index.html', context)


def events(request, id_log_source):
    """
    Metodo interno de la clase Views que renderiza la vista events de la aplicacion
    Args:
        request: Peticion http
        id_log_source: Identificador de la fuente (1:Iptables, ...)

    Returns: Informacion en formato html (plantilla events.html) de la vista events de la aplicacion

    """

    # Se obtiene los resultados de las consultas con los argumentos de la funcion en formato lista para su posterior
    # manipulacion e iteracion en la generacion de los datos en la vista

    log_source = get_object_or_404(LogSources, pk=id_log_source)
    events_list = get_list_or_404(Events, ID_Source_id=id_log_source)
    event = get_object_or_404(Events, pk=id_log_source)

    # Esta variable almacena en formato JSON o diccionario la informacion obtenida de los diferentes modelos de la
    # base de datos

    context = {'event': event, 'events_list': events_list, 'log_source': log_source}

    if request.method == 'POST' and request.is_ajax():
        data = {"event": event}
        return JsonResponse(data)

    return render(request, 'secapp/events.html', context)


@csrf_protect
def event_information(request, id_log_source, id_event):
    """
    Metodo interno de la clase Views que renderiza la vista information events de la aplicacion
    Args:
        request: Peticion http
        id_log_source: Identificador de la fuente (1:Iptables, ...)
        id_event: Identificador del evento cuyos detalles se quieren mostrar

    Returns: Informacion en formato html (plantilla event_information.html) de la vista information
    events de la aplicacion.

    """

    # Se obtiene los resultados de las consultas con los argumentos de la funcion en formato lista para su posterior
    # manipulacion e iteracion en la generacion de los datos en la vista

    log_source = get_object_or_404(LogSources, pk=id_log_source)
    event = get_object_or_404(Events, pk=id_event)
    packet_event_information = get_object_or_404(PacketEventsInformation, pk=id_event)

    # Esta variable almacena en formato JSON o diccionario la informacion obtenida de los diferentes modelos de la
    # base de datos

    context = {
        'log_source': log_source,
        'event': event,
        'packet_event_information': packet_event_information,
    }

    return render(request, 'secapp/event_information.html', context)


def additional_info(request, id_log_source, id_event):
    """
    Metodo interno de la clase Views que renderiza la vista additional information de la aplicacion
    Args:
        request: Peticion http
        id_log_source: Identificador de la fuente (1:Iptables, ...)
        id_event: Identificador del evento cuyos detalles adicionales se quieren mostrar

    Returns: Informacion en formato html (plantilla additional_info.html) de la vista additional information de
    la aplicacion.

    """

    # Se obtiene los resultados de las consultas con los argumentos de la funcion en formato lista para su posterior
    # manipulacion e iteracion en la generacion de los datos en la vista

    log_source = get_object_or_404(LogSources, pk=id_log_source)
    event = get_object_or_404(Events, pk=id_event)
    packet_event_information = get_object_or_404(PacketEventsInformation, pk=id_event)
    packet_additional_info = get_list_or_404(PacketAdditionalInfo, ID_Packet_Events=packet_event_information)

    # Esta variable almacena en formato JSON o diccionario la informacion obtenida de los diferentes modelos de la
    # base de datos

    context = {
        'log_source': log_source,
        'event': event,
        'packet_additional_info': packet_additional_info,
    }

    return render(request, 'secapp/additional_info.html', context)
