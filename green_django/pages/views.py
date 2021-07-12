from django.views.generic import TemplateView
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


def t(request):
    args={}
    return render(request, 'pages/t.html', args)
