from main.forms import SITES
import os


try:
    os.mkdir('Jobs files')
except Exception:
    pass


def jobs_scrape(func, user, *args):
    funcs = {}
    for site in SITES:
        exec(f'from .{SITES[site][1]} import {site}')
        exec(f'funcs["{site}"] = {site}')

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
