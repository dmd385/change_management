from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import *
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from datetime import datetime


def log_in(request):
    """
    This view will render the log in page that shows when you reach the
    root of the website
    :param request: HTTP request from the web browser
    :return: The log_in page will be rendered
    """
    if request.method == 'POST':
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))

        if user is not None:
            login(request, user)
            path = '/dash/' + str(user.pk) + '/'
            return HttpResponseRedirect(path)
        else:
            return HttpResponseRedirect('/home/?error')
    else:
        content = {}
        if 'error' in request.GET:
            content['error'] = "Incorrect username or password"
        return render(request, 'home/log_in.html', content)


def logOut(request):
    if request.method=='POST':
        logout(request)
        return render(request, 'home/log_in.html')
    else:
        return render(request, 'home/log_in.html')


