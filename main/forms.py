from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Div, ButtonHolder, HTML, Submit

# func_name: [button_name, file_name]
SITES = {'alljobs': ['AllJobs', 'AllJobs_Scraper'], 'drushim': ['Drushim', 'Drushim_Jobs'],
         'jobmaster': ['Job Master', 'Job_Master'], 'sqlink': ['Sqlink', 'Sqlink_Jobs'], 'jobnet': ['Jobnet', 'Jobnet'],
         'indeed': ['Indeed', 'Indeed_Jobs'], 'mploy': ['Mploy', 'Mploy'], 'nisha': ['Nisha', 'Nisha'],
         'telegram_jobs': ['Telegram', 'Telegram_Jobs_Scraper']}


class ScrapeForm(forms.Form):
    all = forms.BooleanField(label='Select all', required=False)
    all.widget = forms.CheckboxInput(attrs={'onclick': "$('input:checkbox').not('#id_all').click();"})
    for site in SITES:
        exec(f'{site} = forms.BooleanField(label="{SITES[site][0]}", required=False)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'all',
                *[site for site in SITES if site != 'telegram_jobs'],
                Row('telegram_jobs',
                    ButtonHolder(
                        HTML("""
                        <div class="btn btn-primary upload-div">
                            Upload Json File (optional)
                            <input class="upload-input" type="file" name="upload_json"/>
                        </div>
                        """)
                        )
                    ),
                Row(ButtonHolder(
                        HTML("""
                        <button type="submit" name="save" class="btn btn-success"
                            style="margin-right: 30px; margin-top: 30px">
                            Scrape
                        </button>
                        """)),
                    ButtonHolder(
                        HTML("""
                        <button type="submit" name="reset" class="btn btn-danger" style="margin-top: 30px"
                            onclick="return confirm('Are you sure you want to reset all deleted jobs?')">
                            Reset deleted jobs
                        </button>
                        """))
                    ),
            ),
        )


class JobsListFrom(forms.Form):
    btn = forms.CharField()
    link = forms.CharField()


class AddKeywordForm(forms.Form):
    keyword = forms.CharField()
    btn = forms.CharField()


class DeleteKeywordForm(forms.Form):
    delete = forms.CharField()


class UpdateKeywordForm(forms.Form):
    ckbx = forms.BooleanField(required=False)
    update = forms.CharField()


class GuestRegistrationForm(forms.Form):
    btn = forms.CharField()
