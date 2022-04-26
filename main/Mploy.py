"""
Scraping student jobs (for me) from https://www.mploy.co.il.
"""
__version__ = '1.0.0'
__author__ = 'Yarin Levi <yarinl330@gmail.com>'

from bs4 import BeautifulSoup
import requests
from main.helper import add_job


def mploy(username):
    page = 1
    jobs = []
    while True:
        url = f"https://www.mploy.co.il/job/search/סטודנט-מדעי-המחשב?page={page}"
        page += 1
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"}
        req = requests.get(url, headers=headers, verify=False).content.decode('utf-8')
        soup = BeautifulSoup(req, 'html.parser')
        all_a = soup.find_all('a')
        break_flag = False
        for i in all_a:
            try:
                if 'job/details' in i['href']:
                    break_flag = True
                    jobs.append((f'https://www.mploy.co.il{i["href"]}', i.text))
            except Exception:
                pass

        if break_flag is False:
            break
    add_job(jobs, username)