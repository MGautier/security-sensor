from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the secapp index.")


def events(request, id_event):
    return HttpResponse("You're looking at event %s. " % id_event)


def log_sources(request, id_source):
    response = "You're looking at the log_source of event %s. "
    return HttpResponse(response % id_source)


def ips(request, id_ip):
    return HttpResponse("You're looking at the ips of packet events %s. " % id_ip)
