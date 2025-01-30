from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen
from charts.models import MetricType, TimeSeriesMetric
from django.utils import timezone


@shared_task
def scrape_charts():
    url = "https://recwell.wisc.edu/liveusage/"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    titles = map(lambda t: t.text, soup.find_all(class_='tracker-location'))
    vals = map(lambda t: t.text, soup.find_all(class_='tracker-current-count'))

    if len(titles) != len(vals):
        print("Titles out of sync with data!")
        return

    for i in len(titles):
        name = titles[i]
        metric_type = MetricType.objects.filter(display_name=name).first()
        if metric_type is None:
            metric_type = MetricType.objects.create(display_name=name)
            metric_type.save()
        new_metric = TimeSeriesMetric.objects.create(
            metric_type=metric_type, timestamp=timezone.now(), value=vals[i])
        new_metric.save()
