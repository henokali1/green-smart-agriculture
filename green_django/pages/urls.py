from django.urls import path
from . import views
from .views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('sensor-real-time/', views.sensor_real_time, name='sensor-real-time.html'),
    path('t/', views.t, name='t.html'),
    path('dashboard/', views.dashboard, name='dashboard.html'),
]
