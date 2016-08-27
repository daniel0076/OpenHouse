from .models import RecruitSignup
from django.forms import ModelForm

class RecruitSignupForm(ModelForm):
    class Meta:
        model = RecruitSignup
        fields = '__all__'
        exclude = ['payment', 'receipt_no', 'ps', 'cid']
