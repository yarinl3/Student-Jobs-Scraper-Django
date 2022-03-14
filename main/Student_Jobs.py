from .Job_Master import jobmaster
from .Sqlink_Jobs import sqlink
from .Drushim_Jobs import drushim
from .AllJobs_Scraper import alljobs
from .Telegram_Jobs_Scraper import telegram_jobs
import os
import warnings
import time
wishlist_copy = None


try:
    os.mkdir('Jobs files')
except Exception:
    pass


def main():
        pop_jobs() # Pop scrapped jobs
        pop_jobs(wishlist=True) # Pop wishlist jobs


def jobs_scrap(func, user):
    funcs = {'alljobs': alljobs, 'drushim': drushim, 'jobmaster': jobmaster,
             'sqlink': sqlink, 'telegram_jobs': telegram_jobs}
    try:
        funcs[func](user)
        return True
    except Exception as e:
        print(e)
        return False


def update_wishlist(jobs):
    with open('Jobs files/wishlist.txt', encoding='utf-8', mode='a+') as fd:
        wishlist_content = fd.read()
        for job in jobs:
            link = job[0]
            title = job[1]
            if link not in wishlist_content:
                fd.write(f"{link}|||{title.replace('|||', ' ')}\n")


def pop_jobs(wishlist=False):
    global wishlist_copy
    if wishlist is True:
        jobs = load_wishlist()
        wishlist_copy = jobs
    else:
        jobs = load_jobs()
    while True:

        with open('Jobs files/unwanted_keywords.txt', encoding='utf-8', mode='r') as fd:
            keywords = fd.read().split('\n')
            while True:
                job = jobs.pop()
                if wishlist is True:
                    wishlist_copy.pop()
                link = job[0]
                title = job[1].replace('\n', '')
                if True not in [check_exist(link, i) for i in ['blacklist', 'sent', 'wishlist']] and \
                        True not in [keyword.lower() in f'{title.lower()} {link.lower()}' for keyword in keywords]:
                    break
        print(f'Total jobs: {len(jobs) + 1}')
        print(f'\n{title}' + u'\u202B')
        print(f'{link}\n')
        choice = input('1. Add to blacklist\n'
                       '2. Save to wishlist\n'
                       '9. Add to sent\n'
                       '4. Exit\n')
        if choice == '1':
            check_exist(link, 'blacklist', add=True)
        elif choice == '2':
            check_exist(link, 'wishlist', add=True, wishlist_title=title)
        elif choice == '9':
            check_exist(link, 'sent', add=True)
        else:
            jobs.append(job)
            if wishlist is True:
                wishlist_copy.append(job)
        if choice == '4':
            if wishlist is True:
                update_wishlist(jobs)
            return
        time.sleep(0.5)


def check_exist(url, filename, add=False, wishlist_title=None):
    try:
        with open(f'Jobs files/{filename}.txt', encoding='utf-8', mode='r') as fd:
            pass
    except FileNotFoundError:
        with open(f'Jobs files/{filename}.txt', encoding='utf-8', mode='w') as fd:
            pass
    with open(f'Jobs files/{filename}.txt', encoding='utf-8', mode='a+') as fd:
        fd.seek(0)
        for line in fd:
            if f'{url}' in line:
                return True
        if add is True:
            if wishlist_title is None:
                fd.write(f'{url}\n')
            else:
                fd.write(f"{url}|||{wishlist_title.replace('|||', ' ')}\n")
    return False


def handle_errors():
    try:
        main()
    except IndexError as e:
        if str(e) == 'pop from empty list':
            print('You went through the entire list of jobs.\n'
                  'For new jobs, please try scraping again.')
    except Exception:
        if wishlist_copy is not None:
            update_wishlist(wishlist_copy)


if __name__ == '__main__':
    handle_errors()
