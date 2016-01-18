from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404
# from django.template import RequestContext, loader

from .models import LogSources, Events, Ips, PacketEventsInformation, PacketAdditionalInfo
from iptables import Iptables


# Create your views here.

def index(request):
    # Otra forma
    # template = loader.get_template('secapp/index.html')
    # context = RequestContext(request, {
    #    'latest_source_list': latest_source_list
    # })
    # output = ', '.join([lg.Description for lg in latest_source_list])
    # return HttpResponse(template.render(context))

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
    # try:
    #    event = Events.objects.get(pk=id_event)
    # except Events.DoesNotExist:
    #    raise Http404("Event does not exist")
    # return render(request, 'secapp/events.html', {'event': event})

    # return HttpResponse("You're looking at event %s. " % id_event)

    log_source = get_object_or_404(LogSources, pk=id_log_source)
    events_list = get_list_or_404(Events, ID_Source_id=id_log_source)
    event = get_object_or_404(Events, pk=id_log_source)
    context = {'event': event, 'events_list': events_list, 'log_source': log_source}
    return render(request, 'secapp/events.html', context)


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
