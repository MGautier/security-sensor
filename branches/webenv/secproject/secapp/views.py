from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
# from django.template import RequestContext, loader

from .models import LogSources, Events, Ips


# Create your views here.

def index(request):
    latest_source_list = LogSources.objects.order_by('id')[:3]

    # Otra forma
    # template = loader.get_template('secapp/index.html')
    # context = RequestContext(request, {
    #    'latest_source_list': latest_source_list
    #})
    # output = ', '.join([lg.Description for lg in latest_source_list])
    # return HttpResponse(template.render(context))

    context = {'latest_source_list': latest_source_list}
    if request.GET.get('run-btn'):
        hello = int(request.GET.get('textbox'))
        context.update({'hello': hello})

    return render(request, 'secapp/index.html', context)


def events(request, id_event):
    # try:
    #    event = Events.objects.get(pk=id_event)
    # except Events.DoesNotExist:
    #    raise Http404("Event does not exist")
    # return render(request, 'secapp/events.html', {'event': event})

    # return HttpResponse("You're looking at event %s. " % id_event)

    event = get_object_or_404(Events, pk=id_event)
    return render(request, 'secapp/events.html', {'event': event})


def sources(request, id_source):

    # response = "You're looking at the log_source of event %s. "
    # return HttpResponse(response % id_source)

    source = get_object_or_404(LogSources, pk=id_source)
    return render(request, 'secapp/sources.html', {'source': source})


def ips(request, id_ip):
    return HttpResponse("You're looking at the ips of packet events %s. " % id_ip)
