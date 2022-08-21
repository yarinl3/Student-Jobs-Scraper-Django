"""
Scraping student jobs (for me) from https://t.me/HiTech_Jobs_In_Israel.
"""
__version__ = '1.0.1'
__author__ = 'Yarin Levi <yarinl330@gmail.com>'

import json
from main.helper import add_job


def telegram_jobs(username, *args):
    try:
        blocked_job_locations = [i.replace('\n', '') for i in
                                 open('Jobs files/blocked_job_location.txt', encoding='utf-8').readlines()]
    except FileNotFoundError:
        blocked_job_locations = []
    if len(args) != 0:
        unfiltered_jobs, error_flag = make_list(args[0])
    else:
        unfiltered_jobs, error_flag = make_list()
    if error_flag is True:
        return 'Failed to load telegram json file.'
    filtered_jobs = make_filtered_job_list(unfiltered_jobs, blocked_job_locations)
    add_job(filtered_jobs, username)


# Creates a list that contains all jobs for students:
def make_list(*args):
    jobs = []
    file_path = 'Jobs files/result.json'

    try:
        if len(args) != 0:
            site_json = json.loads(args[0].read())
        else:
            site_json = json.loads(open(file_path, encoding='utf-8').read())

        for i in site_json['messages']:
            for j in i['text']:
                try:
                    if type(j) == dict and 'student' in j['text'].lower():
                        jobs.append(i['text'])
                        break
                except KeyError:
                    pass
    except Exception:
        return jobs, True
    return jobs, False


def make_filtered_job_list(jobs, blocked_job_locations):
    """Filter jobs by locations"""
    filtered_jobs = []
    for job in jobs:
        try:
            job_title = str(job[0]['text']).replace('\n', '')
            job_location = str(job[1]).replace('\n', '')
            job_link = str(job[2]['href']).replace('\n', '')
            block_flag = False

            # Cuts the location from the sentence:
            if job_location.find('Location:') != -1 and job_location.find('Press') != -1:
                job_location = job_location[job_location.find('Location:')+10:job_location.find('Press')]

            for location in blocked_job_locations:
                if location.lower() in job_location.lower():
                    block_flag = True
                    break

            if block_flag is False:
                filtered_jobs.append((job_link, job_title))

        except TypeError:
            pass
        except KeyError:
            pass
    return filtered_jobs
