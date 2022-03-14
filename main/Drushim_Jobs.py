"""
Scraping student jobs (for me) from https://www.drushim.co.il/.
"""
__version__ = '1.0.0'
__author__ = 'Yarin Levi <yarinl330@gmail.com>'

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from main.models import ScrapedJobs


def drushim(user):
    url = 'https://www.drushim.co.il/jobs/subcat/406/'
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    while True:
        try:
            buttons = driver.find_elements_by_xpath("//*[contains(text(), 'הצג לי משרות נוספות')]")
            if len(buttons) < 2:
                break
            for btn in buttons:
                btn.click()
        except Exception:
            pass

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    jobs_div = soup.find_all('div', {'class': 'job-item-main pb-3 job-hdr'})
    jobs = []
    for job_div in jobs_div:
        # finds the job link
        a_list = job_div.find_all('a')
        for a in a_list:
            if '/job/' in a['href']:
                job_link = f'https://www.drushim.co.il{a["href"]}'
                break
        # finds the job title
        h3_list = job_div.find_all('h3')
        job_title = h3_list[0].text.strip()
        jobs.append((job_link, job_title))
    driver.close()

    t = ScrapedJobs.objects
    if len(t.filter(name=user)) == 1:
        t = t.get(name=user)
        for job in jobs:
            t.job_set.create(title=job[1], link=job[0], sent=False)