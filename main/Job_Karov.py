"""
Scraping student jobs (for me) from https://www.jobkarov.com/.
"""
__version__ = '1.0.1'
__author__ = 'Yarin Levi <yarinl330@gmail.com>'

from bs4 import BeautifulSoup
import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import pyautogui
from main.helper import add_job
import time


def job_karov(username):
    driver = login_vpn()
    driver.switch_to.window(driver.window_handles[0])
    url = 'https://www.jobkarov.com/Search/?role=2180'
    driver.get(url)
    time.sleep(5)
    htmlElement = driver.find_element(By.TAG_NAME, "html")
    dom = htmlElement.get_attribute("outerHTML")
    print('Start Job Karov scrolling')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        display = driver.execute_script("return window.getComputedStyle(document.querySelector('footer')).display;")
        if display == 'block':
            break
    print('End Job Karov scrolling')
    soup = BeautifulSoup(dom, 'html.parser')
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


def foo(path, conf, x_offset=0, y_offset=0):
    extn = pyautogui.locateOnScreen(path, confidence=conf)
    if extn is not None:
        pyautogui.click(x=extn[0] + x_offset, y=extn[1] + y_offset, clicks=1, interval=0.0, button="left")
    else:
        print(f'Cant find {path}')
        return False


def login_vpn():
    path = os.getcwd()
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    chop = webdriver.ChromeOptions()
    chop.add_argument("--allow-pre-commit-input")
    chop.add_argument("--disable-background-networking")
    chop.add_argument("--disable-backgrounding-occluded-windows")
    chop.add_argument("--disable-client-side-phishing-detection")
    chop.add_argument("--disable-default-apps")
    chop.add_argument("--disable-hang-monitor")
    chop.add_argument("--disable-popup-blocking")
    chop.add_argument("--disable-prompt-on-repost")
    chop.add_argument("--disable-sync")
    chop.add_argument("--enable-automation")
    chop.add_argument("--enable-blink-features=ShadowDOMV0")
    chop.add_argument("--enable-logging")
    chop.add_argument(fr'--load-extension={path}\selenium_vpn\extension_lohjijocnmbpmhlimaamceahcmjbhdmi')
    chop.add_argument("--log-level=0")
    chop.add_argument("--no-first-run")
    chop.add_argument("--no-service-autorun")
    chop.add_argument("--password-store=basic")
    chop.add_argument("--profile-directory=test")
    chop.add_argument("--remote-debugging-port=0")
    chop.add_argument("--test-type=webdriver")
    chop.add_argument("--use-mock-keychain")
    chop.add_argument(fr'--user-data-dir={path}\selenium_vpn\scoped_dir9300_1085488000')
    chop.add_argument("--flag-switches-begin")
    chop.add_argument("--flag-switches-end data:,")
    driver = webdriver.Chrome(options=chop, desired_capabilities=capa)
    icon_error = fr"{path}\selenium_vpn\not_login.png"
    signin = fr"{path}\selenium_vpn\signin.png"

    time.sleep(1)
    foo(icon_error, 0.8)
    time.sleep(2)
    foo(signin, 0.8, 50, 20)
    time.sleep(1)
    try:
        driver.switch_to.window(driver.window_handles[0])
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(4)
        continue_button = driver.find_element(By.CLASS_NAME, "multiLogin__item__button")
        continue_button.click()
    except Exception as e:
        print(e)
        raise 'Login to VPN failed.'
    return driver


if __name__ == '__main__':
    job_karov('')