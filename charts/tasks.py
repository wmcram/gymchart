from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen


@shared_task
def scrape_charts():
    url = "https://recwell.wisc.edu/liveusage/"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    firsts = soup.find_all(class_='tracker-current-count')
    firsts = map(lambda t: t.text, firsts)
    seconds = soup.find_all(class_='tracker-max-count')
    seconds = map(lambda t: t.text, seconds)
    data = zip(firsts, seconds)
