from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Div, ButtonHolder, HTML, Submit


class ScrapeForm(forms.Form):
    all = forms.BooleanField(label='Select all', required=False)
    all.widget = forms.CheckboxInput(attrs={'onClick': "toggle(this)"})
    alljobs = forms.BooleanField(label='AllJobs', required=False)
    drushim = forms.BooleanField(label='Drushim', required=False)
    jobmaster = forms.BooleanField(label='Job Master', required=False)
    sqlink = forms.BooleanField(label='Sqlink', required=False)
    jobnet = forms.BooleanField(label='Jobnet', required=False)
    indeed = forms.BooleanField(label='Indeed', required=False)
    telegram_jobs = forms.BooleanField(label='Telegram', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'all',
                'alljobs',
                'drushim',
                'jobmaster',
                'sqlink',
                'jobnet',
                'indeed',
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
