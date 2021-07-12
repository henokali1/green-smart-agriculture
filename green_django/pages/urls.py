from django.urls import path
from . import views
from .views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('t/', views.t, name='t.html'),
]