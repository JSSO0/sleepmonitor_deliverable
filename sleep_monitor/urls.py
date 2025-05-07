from django.urls import path
from . import views

app_name = 'sleep_monitor'

urlpatterns = [
    path('', views.index, name='index'),
    path('process_frame/', views.process_frame_view, name='process_frame'),
]
