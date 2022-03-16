from .Job_Master import jobmaster
from .Sqlink_Jobs import sqlink
from .Drushim_Jobs import drushim
from .AllJobs_Scraper import alljobs
from .Telegram_Jobs_Scraper import telegram_jobs
import os


try:
    os.mkdir('Jobs files')
except Exception:
    pass


def jobs_scrap(func, user):
    funcs = {'alljobs': alljobs, 'drushim': drushim, 'jobmaster': jobmaster,
             'sqlink': sqlink, 'telegram_jobs': telegram_jobs}
    try:
        funcs[func](user)
        return True
    except Exception as e:
        print(e)
        return False
