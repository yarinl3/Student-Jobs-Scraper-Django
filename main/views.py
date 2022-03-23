import random
import time
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import *
from .Student_Jobs import jobs_scrap
from .models import *
from threading import Thread
CHECKBOXLIST = ['alljobs', 'drushim', 'jobmaster', 'sqlink', 'telegram_jobs']
TIMEOUT = 25


# Create your views here.
def home(response):
    form = GuestRegistrationForm()
    if response.user.is_anonymous is True:
        if response.method == "POST":
            form = GuestRegistrationForm(response.POST)
            if form.is_valid():
                val = form.cleaned_data.get("btn")
                if val == 'לחץ כאן':
                    try:
                        while True:
                            username = f'guest-{random.randint(1,100000)}'
                            if len(UserJobs.objects.all().filter(username=username)) == 0 and\
                                    len(JobsFilters.objects.all().filter(username=username)) == 0:
                                user = User.objects.create_user(username, password='12345')
                                user.is_superuser = False
                                user.is_staff = False
                                user.save()
                                break
                        for job in Job.objects.all():
                            if len(job.userjobs_set.filter(username='guest-1')) != 0:
                                guest1 = job.userjobs_set.get(username='guest-1')
                                job.userjobs_set.create(username=username, sent=guest1.sent, scraped=guest1.scraped,
                                                        wishlist=guest1.wishlist, deleted=guest1.deleted)

                        for keyword in Keyword.objects.all():
                            if len(keyword.jobsfilters_set.filter(username='guest-1')) != 0:
                                guest1 = keyword.jobsfilters_set.get(username='guest-1')
                                keyword.jobsfilters_set.create(username=username, keyword=guest1.keyword)

                    except Exception as e:
                        print(f'Error in views.home, username = {username}, Error: {e}')

                    finally:
                        if user is not None:
                            login(response, user)
    return render(response, 'main/home.html', {'form': form, 'username': response.user})


def same_code(response, page_name):
    if response.user.is_anonymous is False:
        username = str(response.user)
        if response.method == "POST":
            form = JobsListFrom(response.POST)
            if form.is_valid():
                link = form.cleaned_data.get("link")
                val = form.cleaned_data.get("btn")
                print(form)
                user_job = Job.objects.get(link=link).userjobs_set.filter(username=username)
                if val == 'Delete':
                    user_job.update(sent=False, scraped=False, wishlist=False, deleted=True)
                if page_name == 'scraped_list':
                    if val == 'Add to Wishlist':
                        user_job.update(sent=False, scraped=False, wishlist=True, deleted=False)
                if page_name in ['scraped_list', 'wishlist']:
                    if val == 'Add to Sent':
                        user_job.update(sent=True, scraped=False, wishlist=False, deleted=False)
        else:
            form = JobsListFrom()
        new_jobs = []
        jobs = Job.objects.all()
        for job in jobs:
            if len(job.userjobs_set.filter(username=username, sent=(page_name == 'sent'),
                                           scraped=(page_name == 'scraped_list'), wishlist=(page_name == 'wishlist'),
                                           deleted=False)) != 0:
                new_jobs.append(job)
        return render(response, f'main/{page_name}.html', {'form': form, 'jobs': new_jobs, 'username': response.user})
    else:
        raise PermissionDenied()


def scraped_list(response):
    return same_code(response, 'scraped_list')


def wishlist(response):
    return same_code(response, 'wishlist')


def sent(response):
    return same_code(response, 'sent')


def pre_scrap(response):
    global TIMEOUT
    scrap_start_time = time.time()
    if response.user.is_anonymous is False:
        errors = []
        threads = []
        username = str(response.user)
        form = ScrapForm()
        if response.method == "POST":
            form = ScrapForm(response.POST)
            if 'save' in response.POST:
                if form.is_valid():
                    res = response.POST
                    checked_list = [key for key in res if key in CHECKBOXLIST and res.get(key) == 'on']

                    def scrap(checkbox):
                        if checkbox == 'telegram_jobs' and 'upload' in response.FILES:
                            error_flag, error_value = jobs_scrap(checkbox, username, response.FILES['upload'])
                        else:
                            error_flag, error_value = jobs_scrap(checkbox, username)

                        if error_flag is True:
                            errors.append(f'{checkbox} scraped successfully.')
                        else:
                            errors.append(error_value)
                    for checked in checked_list:
                        t = Thread(target=scrap, args=(checked,))
                        threads.append(t)
                        t.start()
                    for t in threads:
                        start_time = time.time()
                        t.join(TIMEOUT)
                        TIMEOUT -= time.time() - start_time
                        if TIMEOUT < 0:
                            TIMEOUT = 0
                    errors = collect_errors(checked_list, errors, scrap_start_time)
            elif 'reset' in response.POST:
                user_job = UserJobs.objects.filter(username=username, deleted=True)
                user_job.update(sent=False, scraped=True, wishlist=False, deleted=False)
        return render(response, 'main/scrap.html', {'form': form, 'errors': errors, 'username': response.user})
    else:
        raise PermissionDenied()


def keywords(response):
    if response.user.is_anonymous is False:
        username = str(response.user)
        add_form = AddKeywordForm(response.POST)
        del_form = DeleteKeywordForm(response.POST)
        update_form = UpdateKeywordForm(response.POST)
        keywords_list = JobsFilters.objects.filter(username=username)
        if response.method == "POST":
            if add_form.is_valid():
                keyword = add_form.cleaned_data.get('keyword').lower()
                if keyword != '' and keyword.isspace() is False:
                    keyword_exist = len(Keyword.objects.all().filter(keyword=keyword)) != 0
                    if keyword_exist is True:
                        old_keyword = Keyword.objects.get(keyword=keyword)
                        keyword_exist_in_others = len(old_keyword.jobsfilters_set.filter(username=username)) == 0
                        if keyword_exist_in_others is True:
                            old_keyword.jobsfilters_set.create(username=username)
                    else:
                        new_keyword = Keyword(keyword=keyword)
                        new_keyword.save()
                        new_keyword.jobsfilters_set.create(username=username)

            elif del_form.is_valid():
                keyword = del_form.cleaned_data.get('delete').lower()
                Keyword.objects.get(keyword=keyword).jobsfilters_set.filter(username=username).delete()
            elif update_form.is_valid():

                userjobs = UserJobs.objects.filter(username=username, scraped=True)
                checkbox = update_form.cleaned_data.get("ckbx")
                for userjob in userjobs:
                    for keyword in keywords_list:
                        job = Job.objects.get(id=userjob.job_id)
                        if str(keyword.keyword) in job.title.lower() or\
                                (checkbox is True and str(keyword.keyword) in job.link.lower()):
                            UserJobs.objects.filter(username=username, job_id=job.id).update(sent=False,
                                                                                             scraped=False,
                                                                                             wishlist=False,
                                                                                             deleted=True)
        return render(response, 'main/keywords.html', {'form': add_form, 'keywords': keywords_list,
                                                       'username': response.user})
    else:
        raise PermissionDenied()


def collect_errors(checked_list, errors, scrap_start_time):
    for site in checked_list:
        site_in_errors = False
        for error in errors:
            if site in str(error):
                site_in_errors = True
        if site_in_errors is False and time.time() - scrap_start_time >= 25:
            errors.append(f'Timeout: 25 seconds passed and the scraping did not end.\n'
                          f'If the connection to {site} is correct it will continue the scraping'
                          f' in the background. ')
    return errors
