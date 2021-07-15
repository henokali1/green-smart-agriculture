from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
import ast
from time import time
from datetime import datetime, timedelta
from django.db.models import Sum
import json
import pickle
import random

class HomePageView(TemplateView):
    template_name = 'home.html'


@login_required
def dashboard(request):
	args = {'dashboard': Dashboard.objects.all()}
	return render(request, 'pages/dashboard.html', args)

@login_required
def sensor_real_time(request):
	args = {}
	return render(request, 'pages/sensor-real-time.html', args)

@login_required
def settings(request):
	args = {}
	return render(request, 'pages/settings.html', args)

def t(request):
	args = {'dashboard': Dashboard.objects.all()}
	return render(request, 'pages/t.html', args)
