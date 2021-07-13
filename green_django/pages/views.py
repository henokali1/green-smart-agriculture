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
	# dashboard = [{'url': 'url', 'icon': 'home', 'title': 'Sensor Data'}, {'url': 'url', 'icon': 'edit', 'title': 'Sensor Data'}, {'url': 'url', 'icon': 'dashboard', 'title': 'Sensor Data'}]
	args = {'dashboard': Dashboard.objects.all()}
	return render(request, 'pages/dashboard.html', args)

def t(request):
	# dashboard = [{'url': 'url', 'icon': 'home', 'title': 'Sensor Data'}, {'url': 'url', 'icon': 'edit', 'title': 'Sensor Data'}, {'url': 'url', 'icon': 'dashboard', 'title': 'Sensor Data'}]
	args = {'dashboard': Dashboard.objects.all()}
	return render(request, 'pages/t.html', args)
