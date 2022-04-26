"""
Scraping student jobs (for me) from https://www.jobkarov.com/.
"""
__version__ = '1.0.0'
__author__ = 'Yarin Levi <yarinl330@gmail.com>'

from bs4 import BeautifulSoup
import os
import undetected_chromedriver as uc
from main.helper import add_job


def job_karov(username):
    driver = uc.Chrome()
    url = 'https://www.jobkarov.com/Search/?role=2180'
    driver.set_page_load_timeout(10)
    driver.get(url)

    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        display = driver.execute_script("return window.getComputedStyle(document.querySelector('footer')).display;")
        if display == 'block':
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    all_li = soup.find_all('li')
    jobs = []
    for li in all_li:
        a_list = li.find_all('a')
        for a in a_list:
            if '/Search/Site/' in a['href']:
                job_link = f'https://www.jobkarov.com{a["href"]}'
                job_title = a.text.strip()
                break
        jobs.append((job_link, job_title))
    driver.close()
    add_job(jobs, username)
