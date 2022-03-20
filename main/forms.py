from django import forms


class ScrapForm(forms.Form):
    all = forms.BooleanField(label='Select all',  required=False)
    all.widget = forms.CheckboxInput(attrs={'onClick': "toggle(this)"})
    alljobs = forms.BooleanField(label='AllJobs', required=False)
    drushim = forms.BooleanField(label='Drushim', required=False)
    jobmaster = forms.BooleanField(label='Job Master', required=False)
    sqlink = forms.BooleanField(label='Sqlink', required=False)
    telegram_jobs = forms.BooleanField(label='Telegram', required=False)


class JobsListFrom(forms.Form):
    btn = forms.CharField()
    link = forms.CharField()


class AddKeywordForm(forms.Form):
    keyword = forms.CharField()
    btn = forms.CharField()


class DeleteKeywordForm(forms.Form):
    delete = forms.CharField()
