from django.shortcuts import render
from django.http import JsonResponse
import os
from datetime import datetime


def main(request):
    return render(request, 'main.html', {'parameter': "test"})


def health(request):
    osInfo = os.uname()
    response = {
    'date': datetime.now().strftime("%d.%m.%y %H:%M"),
    'current_page': request.get_host() + request.get_full_path(),
    'server_info': f"OSName: {osInfo.sysname}; NodeName: {osInfo.nodename}; Release:{osInfo.release}; Version:{osInfo.version}; Indentificator:{osInfo.machine}",
    'client_info': f"Browser: {request.META['HTTP_USER_AGENT']}  IP: {request.META['REMOTE_ADDR']} "
    }
    return JsonResponse(response)
