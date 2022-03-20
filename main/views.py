import time
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import ScrapForm, JobsListFrom, AddKeywordForm, DeleteKeywordForm, UpdateKeywordForm, GuestRegistrationForm
from .Student_Jobs import jobs_scrap
from .models import JobsList, Job, ScrapedJobs, WishlistJobs, JobsFilters
from threading import Thread
CHECKBOXLIST = ['alljobs', 'drushim', 'jobmaster', 'sqlink', 'telegram_jobs']


# Create your views here.
def home(response):
    if response.user.is_anonymous is True:
        if response.method == "POST":
            form = GuestRegistrationForm(response.POST)
            if form.is_valid():
                val = form.cleaned_data.get("btn")
                if val == 'לחץ כאן':
                    try:
                        counter = 1
                        while True:
                            username = f'guest-{counter}'
                            if len(JobsList.objects.filter(name=username)) == 0:
                                break
                            counter += 1
                        user = User.objects.create_user(username, password='12345')
                        user.is_superuser = False
                        user.is_staff = False
                        user.save()
                        JobsList(name=username).save()
                        ScrapedJobs(jobs_list=JobsList.objects.get(name=username), name=username).save()
                        WishlistJobs(jobs_list=JobsList.objects.get(name=username), name=username).save()
                        JobsFilters(jobs_list=JobsList.objects.get(name=username), name=username).save()

                        copy_jobs = ScrapedJobs.objects.get(name='guest-1').job_set.all()
                        for job_copy in copy_jobs:
                            ScrapedJobs.objects.get(name=username).job_set.create(
                                title=job_copy.title, link=job_copy.link, sent=job_copy.sent, deleted=job_copy.deleted)
                        copy_jobs = WishlistJobs.objects.get(name='guest-1').job_set.all()
                        for job_copy in copy_jobs:
                            WishlistJobs.objects.get(name=username).job_set.create(
                                title=job_copy.title, link=job_copy.link, sent=job_copy.sent, deleted=job_copy.deleted)
                        copy_keywords = JobsFilters.objects.get(name='guest-1').keyword_set.all()
                        for keyword_copy in copy_keywords:
                            JobsFilters.objects.get(name=username).keyword_set.create(keyword=keyword_copy)

                        if user is not None:
                            login(response, user)
                    except Exception as e:
                        print(f'Error in views.home, counter = {counter}, Error: {e}')
        else:
            form = GuestRegistrationForm()
    else:
        form = GuestRegistrationForm()

    return render(response, 'main/home.html', {'form': form, 'username': response.user})


def job_list(response):
    if response.user.is_anonymous is False:
        username = str(response.user)
        jobs = ScrapedJobs.objects.get(name=username).job_set.all()
        if response.method == "POST":
            form = JobsListFrom(response.POST)
            if form.is_valid():
                link = form.cleaned_data.get("link")
                val = form.cleaned_data.get("btn")
                if val == 'Delete':
                    ScrapedJobs.objects.get(name=username).job_set.filter(link=link).update(deleted=True)
                if val == 'Add to Wishlist':
                    job_filter = ScrapedJobs.objects.get(name=username).job_set.filter(link=link)
                    if len(job_filter) > 0:
                        job = job_filter[0]
                        WishlistJobs.objects.get(name=username).job_set.create(title=job.title, link=job.link,
                                                                               sent=job.sent, deleted=job.deleted)
                        job_filter.update(deleted=True)
                if val == 'Add to Sent':
                    ScrapedJobs.objects.get(name=username).job_set.filter(link=link).update(sent=True)
        else:
            form = JobsListFrom()
        new_jobs = []
        for job in jobs:
            if job.sent is False and job.deleted is False:
                new_jobs.append(job)
        return render(response, 'main/job_list.html', {'form': form, 'jobs': new_jobs, 'username': response.user})
    else:
        raise PermissionDenied()


def wishlist(response):
    if response.user.is_anonymous is False:
        username = str(response.user)
        if response.method == "POST":
            form = JobsListFrom(response.POST)
            if form.is_valid():
                link = form.cleaned_data.get("link")
                val = form.cleaned_data.get("btn")
                if val == 'Delete':
                    job = WishlistJobs.objects.get(name=username).job_set.get(link=link)
                    ScrapedJobs.objects.get(name=username).job_set.create(title=job.title, link=job.link,
                                                                          sent=job.sent, deleted=True)
                    job.delete()
                if val == 'Add to Sent':
                    WishlistJobs.objects.get(name=username).job_set.filter(link=link).update(sent=True)
        else:
            form = JobsListFrom()
        new_jobs = []
        jobs = WishlistJobs.objects.get(name=username).job_set.all()
        for job in jobs:
            if job.sent is False:
                new_jobs.append(job)
        return render(response, 'main/wishlist.html', {'form': form, 'jobs': new_jobs, 'username': response.user})
    else:
        raise PermissionDenied()


def sent(response):
    if response.user.is_anonymous is False:
        username = str(response.user)
        jobs = []
        for job in WishlistJobs.objects.get(name=username).job_set.all():
            if job.sent is True:
                jobs.append(job)
        for job in ScrapedJobs.objects.get(name=username).job_set.all():
            if job.sent is True:
                jobs.append(job)
        if response.method == "POST":
            form = JobsListFrom(response.POST)
            if form.is_valid():
                link = form.cleaned_data.get("link")
                val = form.cleaned_data.get("btn")
                if val == 'Delete':
                    wishlist_filter = WishlistJobs.objects.get(name=username).job_set.filter(link=link)
                    scraped_jobs_filter = ScrapedJobs.objects.get(name=username).job_set.filter(link=link)
                    if len(wishlist_filter) > 0:
                        jobs.remove((wishlist_filter[0]))
                        job = wishlist_filter[0]
                        ScrapedJobs.objects.get(name=username).job_set.create(title=job.title, link=job.link,
                                                                              sent=job.sent, deleted=True)
                        job.delete()

                    elif len(scraped_jobs_filter) > 0:
                        jobs.remove((scraped_jobs_filter[0]))
                        scraped_jobs_filter.update(deleted=True)
        else:
            form = JobsListFrom()
        new_jobs = []
        for job in jobs:
            if job.deleted is False:
                new_jobs.append(job)
        return render(response, 'main/sent.html', {'form': form, 'jobs': new_jobs, 'username': response.user})
    else:
        raise PermissionDenied()


def scrap(response):
    scrap_start_time = time.time()
    if response.user.is_anonymous is False:
        errors = []
        username = str(response.user)
        if response.method == "POST":
            form = ScrapForm(response.POST)
            if form.is_valid():
                checked_list = []
                threads = []
                t = ScrapedJobs.objects
                timeout = 25

                if len(t.filter(name=username)) == 0:
                    raise Exception(fr"Error: error in main\views.py, there is no list for {username}")
                elif len(t.filter(name=username)) > 1:
                    raise Exception(fr"Error: error in main\views.py, there is more than one list for {username}")
                res = response.POST
                for key in res:
                    if key in CHECKBOXLIST and res.get(key) == 'on':
                        checked_list.append(key)

                def foo(checked, user):
                    if checked == 'telegram_jobs' and 'upload' in response.FILES:
                        error_flag, error_value = jobs_scrap(checked, user, response.FILES['upload'])
                    else:
                        error_flag, error_value = jobs_scrap(checked, user)

                    if error_flag is True:
                        errors.append(f'{checked} scraped successfully.')
                    else:
                        errors.append(error_value)

                for i in checked_list:
                    t = Thread(target=foo, args=(i, username))
                    threads.append(t)
                    t.start()
                for t in threads:
                    start_time = time.time()
                    t.join(timeout)
                    timeout -= time.time() - start_time
                    if timeout < 0:
                        timeout = 0
                for site in checked_list:
                    site_in_errors = False
                    for error in errors:
                        if site in str(error):
                            site_in_errors = True
                    if site_in_errors is False and time.time() - scrap_start_time >= 25:
                        errors.append(f'Timeout: 25 seconds passed and the scraping did not end.\n'
                                      f'If the connection to {site} is correct it will continue the scraping'
                                      f' in the background. ')
        else:
            form = ScrapForm()
        return render(response, 'main/scrap.html', {'form': form, 'errors': errors, 'username': response.user})
    else:
        raise PermissionDenied()


def keywords(response):
    if response.user.is_anonymous is False:
        username = str(response.user)
        add_form = AddKeywordForm(response.POST)
        del_form = DeleteKeywordForm(response.POST)
        update_form = UpdateKeywordForm(response.POST)
        if response.method == "POST":
            if add_form.is_valid():
                keyword = add_form.cleaned_data.get('keyword')
                if keyword != '' and \
                        len(JobsFilters.objects.get(name=username).keyword_set.filter(keyword=keyword.lower())) == 0:
                    JobsFilters.objects.get(name=username).keyword_set.create(keyword=keyword.lower())
            elif del_form.is_valid():
                keyword = del_form.cleaned_data.get('delete')
                JobsFilters.objects.get(name=username).keyword_set.filter(keyword=keyword.lower()).delete()
            elif update_form.is_valid():
                keywords_list = JobsFilters.objects.get(name=username).keyword_set.all()
                jobs = ScrapedJobs.objects.get(name=username).job_set.all()
                flag_link = update_form.cleaned_data.get("ckbx")
                for job in jobs:
                    for keyword in keywords_list:
                        if keyword.keyword in job.title.lower() or (flag_link and keyword.keyword in job.link.lower()):
                            ScrapedJobs.objects.get(name=username).job_set.filter(link=job.link).update(deleted=True)

        keywords_list = JobsFilters.objects.get(name=username).keyword_set.all()
        return render(response, 'main/keywords.html', {'form': add_form, 'keywords': keywords_list, 'username': response.user})
    else:
        raise PermissionDenied()
