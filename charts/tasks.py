import requests
from celery import shared_task
from charts.models import MetricType, TimeSeriesMetric
from django.utils import timezone


@shared_task
def scrape_charts():
    url = 'https://goboardapi.azurewebsites.net/api/FacilityCount/GetCountsByAccount?AccountAPIKey=7938FC89-A15C-492D-9566-12C961BC1F27'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for location in data:
            name = location["LocationName"]
            metric_type = MetricType.objects.filter(display_name=name).first()
            if metric_type is None:
                metric_type = MetricType.objects.create(
                    display_name=name,
                    capacity=location["TotalCapacity"]
                )
            if metric_type.capacity == 0:
                metric_type.capacity = location["TotalCapacity"]
                metric_type.save()
            TimeSeriesMetric.objects.create(
                metric_type=metric_type,
                timestamp=timezone.now(),
                value=location["LastCount"]
            )
