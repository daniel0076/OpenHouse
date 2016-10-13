from .models import RecruitSignup,JobfairInfo
from django.forms import ModelForm

class RecruitSignupForm(ModelForm):
    class Meta:
        model = RecruitSignup
        fields = '__all__'
        exclude = ['payment', 'receipt_no', 'ps', 'cid']

class JobfairInfoForm(ModelForm):
    class Meta:
        model = JobfairInfo
        fields = '__all__'
        exclude = ['company']