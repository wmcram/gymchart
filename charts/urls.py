from django.urls import path
from . import views

urlpatterns = [
    path('', views.metric_dashboard, name='index'),
    path('metrics/chart/<int:metric_id>/',
         views.metric_chart, name='metric_chart'),
]
