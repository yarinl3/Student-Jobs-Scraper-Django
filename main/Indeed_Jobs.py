"""
Scraping student jobs (for me) from https://il.indeed.com/.
"""
__version__ = '1.0.0'
__author__ = 'Yarin Levi <yarinl330@gmail.com>'

from bs4 import BeautifulSoup
import requests
from main.helper import add_job


def indeed(username):
    offset = 0
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"}

    url = f'https://il.indeed.com/jobs?q=מדעי המחשב "סטודנט"&l=חולון, מחוז תל אביב&radius=25&limit=50&start=0'
    req = requests.get(url, headers=headers, verify=False).content.decode('utf-8')
    soup = BeautifulSoup(req, 'html.parser')
    number_of_jobs = soup.find('div', {'id': 'searchCountPages'}).text.split()[3]
    try:
        number_of_jobs = int(number_of_jobs)
    except Exception as e:
        return e

    while True:
        if offset > number_of_jobs:
            break
        url = f'https://il.indeed.com/jobs?q=מדעי המחשב "סטודנט"&l=חולון, מחוז תל אביב&radius=25&limit=50&start={offset}'
        offset += 50
        req = requests.get(url, headers=headers, verify=False).content.decode('utf-8')
        soup = BeautifulSoup(req, 'html.parser')
        all_a = soup.find_all('a')

        for i in all_a:
            try:
                if 'rc/clk' in i['href'] or 'pagead/clk' in i['href']:
                    link = f"https://il.indeed.com{i['href']}"
                    title = i.find('span', {'class': ''}).text
                    jobs.append((link, title))
            except Exception:
                pass
    add_job(jobs, username)
