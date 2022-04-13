from .Job_Master import jobmaster
from .Sqlink_Jobs import sqlink
from .Drushim_Jobs import drushim
from .AllJobs_Scraper import alljobs
from .Telegram_Jobs_Scraper import telegram_jobs
from .Jobnet import jobnet
from .Indeed_Jobs import indeed
import os


try:
    os.mkdir('Jobs files')
except Exception:
    pass


def jobs_scrape(func, user, *args):
    funcs = {'alljobs': alljobs, 'drushim': drushim, 'jobmaster': jobmaster,
             'sqlink': sqlink, 'telegram_jobs': telegram_jobs, 'jobnet': jobnet, 'indeed': indeed}
    try:
        if len(args) != 0:
            error = telegram_jobs(user, args[0])
        else:
            error = funcs[func](user)
        if error is not None:
            return False, error
        return True, error
    except Exception as e:
        return False, e
