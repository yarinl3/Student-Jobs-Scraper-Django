"""
Scraping student jobs (for me) from https://www.nisha.co.il.
"""
__version__ = '1.0.0'
__author__ = 'Yarin Levi <yarinl330@gmail.com>'

from bs4 import BeautifulSoup
import requests
from main.helper import add_job


def nisha(username):
    page = 1
    jobs = []
    while True:
        url = f"https://www.nisha.co.il/niche/1/24?NicheID=1&catID=24&area=&titles=&pagenum={page}"
        page += 1
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"}
        req = requests.get(url, headers=headers, verify=False).content.decode('utf-8')
        soup = BeautifulSoup(req, 'html.parser')
        all_tbody = soup.find_all('tbody')
        break_flag = False
        for tbody in all_tbody:
            if len(tbody.find_all('tr')) > 1:
                for i in tbody.find_all('h3'):
                    try:
                        if 'nisha.co.il/job' in i['href']:
                            break_flag = True
                            jobs.append((i["href"], i.text))
                    except Exception:
                        pass
        if break_flag is False:
            break
    add_job(jobs, username)
