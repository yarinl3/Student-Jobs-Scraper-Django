from main.forms import SITES
import os


try:
    os.mkdir('Jobs files')
except Exception:
    pass


def jobs_scrape(func, user, *args):
    exec(f'from .{SITES[func][1]} import {func}', globals(), locals())
    try:
        res = {}
        if len(args) != 0:
            exec(f'error = {func}(user, args[0])', locals(), res)
        else:
            exec(f'error = {func}(user)', locals(), res)
        error = res['error']

        if error is not None:
            return False, error
        return True, error
    except Exception as e:
        return False, e
