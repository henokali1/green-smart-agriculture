from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
import ast
from time import time
import datetime
from django.db.models import Sum
import json
import pickle
import random



lat=0.0
lng=0.0
soil_temp=0.0
soil_moisture=0.0
air_temp=0.0
pump_on = False
light_on = False
ts=0.0
cntr = 0
db_update_min = 1
div = db_update_min*60
manual_ctrl = False


def read_pickle_file(fn):
    with open(fn, 'rb') as handle:
        val = pickle.load(handle)
    return val

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
def device_location(request):
	fn = '/home/henokali1/key/maps-key.pickle'
	# device_id = str(request.user.email)
	# location = Detail.objects.filter(device_id=device_id)
	# args = {
	# 	'maps_key': read_pickle_file(fn),
	# 	'lat':location[0].lat,
	# 	'lng':location[0].lng,
	# }
	args = {
		'maps_key': read_pickle_file(fn),
		'lat':lat,
		'lng':lng,
	}
	return render(request, 'pages/location.html', args)

@login_required
def settings(request):
	args = {}
	return render(request, 'pages/settings.html', args)

def home(request):
	args = {'dashboard': Dashboard.objects.all()}
	return render(request, 'pages/home-1.html', args)

@login_required
def mission(request):
	try:
		sensor = request.GET['sensor']
		date = request.GET['date']
		sp = date.split('-')
		y=int(sp[0])
		m=int(sp[1])
		dt=int(sp[2])
		val=SensorHisData.objects.values_list(sensor, flat=True).filter(date__contains=datetime.date(y,m,dt))
		d=list(SensorHisData.objects.values_list('ts', flat=True).filter(date__contains=datetime.date(y,m,dt)))
		args = {'val': list(val), 'd': d, 'tot': len(d), 'hAxis': 'Date', 'vAxis': sensor, 'tit_date': date}
		return render(request, 'pages/mission.html', args)
	except:
		args={}
		print('norm')
		return render(request, 'pages/mission.html', args)

@login_required
def telemetry(request):
	args={}
	return render(request, 'pages/telemetry.html', args)

@login_required
def ctrl(request):
	args = {'manual_ctrl': manual_ctrl}
	return render(request, 'pages/ctrl.html', args)

def ctrl_act(request):
	global pump_on
	global light_on
	global manual_ctrl

	param = request.GET['param']
	if(param == 'light_on'):
		light_on = True
		print('light on')
	if(param == 'light_off'):
		light_on = False
		print('light off')
	if(param == 'pump_on'):
		pump_on = True
		print('pump on')
	if(param == 'pump_off'):
		pump_on = False
		print('pump off')
	if(param == 'manual'):
		manual_ctrl = True
	if(param == 'auto'):
		manual_ctrl = False
	args = {'light_on': light_on, 'pump_on': pump_on, 'manual_ctrl': manual_ctrl}
	return JsonResponse(args)

def act_stat(request):
	args = {'light_on': light_on, 'pump_on': pump_on, 'manual_ctrl': manual_ctrl}
	return JsonResponse(args)

def update_live_sensor_data(request):
	global lng
	global lat
	global soil_temp
	global soil_moisture
	global air_temp
	global ts
	global cntr
	cntr += 1
	print(cntr)
	soil_temp = request.GET["soil_temp"]
	soil_moisture = request.GET["soil_moisture"]
	air_temp = request.GET["air_temp"]
	lat=request.GET["lat"]
	lng=request.GET["lng"]
	ts = time()
	if(cntr%div == 0):
		new_data, created = SensorHisData.objects.get_or_create(
			soil_temp = soil_temp,
			soil_moisture = soil_moisture,
			air_temp = air_temp,
			ts=int(time())*1000
		)
		print('Hist data updated')
	print(soil_temp)
	print(soil_moisture)
	print(air_temp)
	return JsonResponse(request.GET)

def get_live_sensor_data(request):
	args={
		'lng': lng,
		'lat': lat,
		'soil_temp': soil_temp,
		'soil_moisture': soil_moisture,
		'air_temp': air_temp,
		'ts': ts,
	}
	return JsonResponse(args)


def save_senosr_data_db(request):
	new_data, created = SensorHisData.objects.get_or_create(
		soil_temp = request.GET["soil_temp"],
		soil_moisture = request.GET["soil_moisture"],
		air_temp = request.GET["air_temp"],
		ts=int(time())*1000
	)
	return JsonResponse({})

def get_sensor_hist_data(request):
	try:
		sensor = request.GET['sensor']
		date = request.GET['date']
		sp = date.split('-')
		y=int(sp[0])
		m=int(sp[1])
		dt=int(sp[2])
		val=SensorHisData.objects.values_list(sensor, flat=True).filter(date__contains=datetime.date(y,m,dt))
		d=SensorHisData.objects.values_list('date', flat=True).filter(date__contains=datetime.date(y,m,dt))
		print(len(val) == len(d))
		args = {'val': list(val), 'd': list(d), 'tot': len(d), 'hAxis': 'Date', 'vAxis': sensor}
		return render(request, 'pages/mission.html', args)
	except:
		print('norm')
		return render(request, 'pages/mission.html', args)


def t(request):
	args = {'dashboard': Dashboard.objects.all()}
	return render(request, 'pages/t.html', args)
