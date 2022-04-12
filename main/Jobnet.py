"""
Scraping student jobs (for me) from https://www.jobnet.co.il.
"""
__version__ = '1.0.0'
__author__ = 'Yarin Levi <yarinl330@gmail.com>'

from bs4 import BeautifulSoup
import requests
from main.helper import add_job


def jobnet(username):
    page = 0
    jobs = []
    while True:
        url = f"https://www.jobnet.co.il/Jobs?p={page}&subprofid=752,1073,1079&checkarea=2,5,9"
        page += 1
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"}
        req = requests.get(url, headers=headers, verify=False).content.decode('utf-8')
        soup = BeautifulSoup(req, 'html.parser')
        all_a = soup.find_all('a')
        break_flag = False
        for i in all_a:
            try:
                if 'positionid' in i['href']:
                    break_flag = True
                    jobs.append((f'https://www.jobnet.co.il{i["href"]}', i.text))
            except Exception:
                pass

        if break_flag is False:
            break
    add_job(jobs, username)
