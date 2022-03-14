"""
Scraping student jobs (for me) from https://www.alljobs.co.il/.
"""
__version__ = '1.0.0'
__author__ = 'Yarin Levi <yarinl330@gmail.com>'

from bs4 import BeautifulSoup
import requests
from main.models import ScrapedJobs


def alljobs(user):
    url = 'https://www.alljobs.co.il/SearchResultsGuest.aspx?position=1449,1747&type=&source=783&duration=60'

    # Extract cookie from first load
    pre_content = requests.get(url).content.decode('utf-8')
    if 'seed:' in pre_content:
        pre_content = pre_content[pre_content.find('seed:') + 7:]
        headers = {'Cookie': f"rbzid={pre_content[:pre_content.find(',') - 1]}"}
    else:
        headers = {}

    jobs = []
    page = 1
    req = b'\xd7\x93\xd7\xa3 \xd7\x94\xd7\x91\xd7\x90'  # 'דף הבא' in hex
    while 'דף הבא' in req.decode('utf-8'):
        req = requests.get(f"{url[:url.find('?')]}?page={page}&{url[url.find('?') + 1:]}", headers=headers).content
        soup = BeautifulSoup(req, 'html.parser')
        jobs_div = soup.find_all('div', {'class': 'job-content-top'})
        for job_div in jobs_div:
            a_list = job_div.find_all('a', {'class': 'N'})
            for a in a_list:
                if 'JobID' in a['href']:
                    job_link = f"https://www.alljobs.co.il{a['href']}"
                    job_title = a['title']
                    jobs.append((job_link, job_title))
        page += 1

    t = ScrapedJobs.objects
    if len(t.filter(name=user)) == 1:
        t = t.get(name=user)
        for job in jobs:
            t.job_set.create(title=job[1], link=job[0], sent=False)