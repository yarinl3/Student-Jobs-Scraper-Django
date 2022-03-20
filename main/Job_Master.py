"""
Scraping student jobs (for me) from https://www.jobmaster.co.il.
"""
__version__ = '1.0.0'
__author__ = 'Yarin Levi <yarinl330@gmail.com>'

from bs4 import BeautifulSoup
import requests
from main.models import ScrapedJobs


def jobmaster(user):
    page = 1
    jobs = []
    while True:
        url = f'https://www.jobmaster.co.il/jobs/?currPage={page}&q=סטודנטים+למחשבים'
        req = requests.get(url).content.decode('utf-8')
        page += 1
        if 'לא נמצאו תוצאות' in req:
            break

        soup = BeautifulSoup(req, 'html.parser')
        articles = soup.find_all('article', {'class': 'CardStyle JobItem font14'})
        for article in articles:
            links = article.find_all('a')
            link = links[0]['href']
            if 'jobs' in link:
                job_link = f'https://www.jobmaster.co.il{link}'
            else:
                job_link = ''
            job_title = article.find('div', {'class': 'CardHeader'}).text
            jobs.append((job_link, job_title))

    t = ScrapedJobs.objects
    if len(t.filter(name=user)) == 1:
        t = t.get(name=user)
        for job in jobs:
            if len(t.job_set.filter(link=job[0])) == 0:
                t.job_set.create(title=job[1], link=job[0], sent=False, deleted=False)