from django.urls import path
from . import views
from .views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('sensor-real-time/', views.sensor_real_time, name='sensor-real-time.html'),
    path('dashboard/', views.dashboard, name='dashboard.html'),
    path('settings/', views.settings, name='settings.html'),
    path('location/', views.device_location, name='location.html'),
    # path('home/', views.home, name='home-1.html'),
    path('mission/', views.mission, name='mission.html'),
    path('telemetry/', views.telemetry, name='telemetry.html'),
    path('update_live_sensor_data/', views.update_live_sensor_data, name='t.html'),
    path('get_live_sensor_data/', views.get_live_sensor_data, name='t.html'),
    path('ctrl/', views.ctrl, name='ctrl.html'),
    path('ctrl_act/', views.ctrl_act, name='ctrl.html'),
    path('act_stat/', views.act_stat, name='ctrl.html'),
    path('sensor_data_api/', views.save_senosr_data_db, name='t.html'),
    path('mission_chart/', views.get_sensor_hist_data, name='mission-chart.html'),
    path('t/', views.t, name='t.html'),
]
