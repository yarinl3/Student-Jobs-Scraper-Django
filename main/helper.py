from main.models import Job
from django.contrib.auth.models import User


def add_job(jobs, username):
    for job in jobs:
        job_exist = len(Job.objects.filter(link=job[0])) != 0
        user = User.objects.get(username=username)
        if job_exist is True:
            old_job = Job.objects.filter(link=job[0])[0]
            job_exist_in_others = len(old_job.userjobs_set.filter(username=user)) == 0
            if job_exist_in_others is True:
                old_job.userjobs_set.create(username=user, sent=False, scraped=True, wishlist=False, deleted=False)
        else:
            new_job = Job(link=job[0], title=job[1])
            new_job.save()
            new_job.userjobs_set.create(username=user, sent=False, scraped=True, wishlist=False, deleted=False)
