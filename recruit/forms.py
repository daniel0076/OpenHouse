from django import forms
from .models import RecruitSignup,JobfairInfo, CompanySurvey, SeminarInfo,Student
from django.forms import ModelForm

class RecruitSignupForm(ModelForm):
    class Meta:
        model = RecruitSignup
        fields = '__all__'
        exclude = ['payment', 'receipt_no', 'ps', 'cid']

class SeminarInfoCreationForm(forms.ModelForm):

    class Meta:
        model=SeminarInfo
        fields='__all__'
        exclude=['cid']

    def __init__(self, *args, **kwargs):
            super(SeminarInfoCreationForm, self).__init__(*args, **kwargs)
            self.fields['contact_mobile'].widget.attrs.update({
                'placeholder': '格式：0912-345678',
                })

    def save(self,commit=True):
        record = super(SeminarInfoCreationForm, self).save(commit=False)
        if commit:
            record.save()
        return record

class JobfairInfoForm(ModelForm):
    class Meta:
        model = JobfairInfo
        fields = '__all__'
        exclude = ['company']

class SurveyForm(forms.ModelForm):
    #def __init__(self, *args, **kwargs):
    #       super(SignupCreationForm, self).__init__(*args, **kwargs)
    #       self.fields['seminar'].widget.attrs.update({
    #           'class': 'ui dropdown',
    #           })

    class Meta:
        model=CompanySurvey
        fields='__all__'

    def save(self,commit=True):
        survey = super(SurveyForm, self).save(commit=False)
        if commit:
            survey.save()
        return survey


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = fields = ['card_num','student_id','phone']

