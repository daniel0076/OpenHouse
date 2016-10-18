from django import forms
import rdss.models
from django.utils import timezone

class SignupCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super(SignupCreationForm, self).__init__(*args, **kwargs)
            self.fields['seminar'].widget.attrs.update({
                'class': 'ui dropdown',
                })

    class Meta:
        model=rdss.models.Signup
        fields='__all__'
        exclude=['payment','receipt_no','ps']

    def save(self,commit=True):
        record = super(SignupCreationForm, self).save(commit=False)
        if commit:
            record.save()
        return record

class SignupEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
            super(SignupCreationForm, self).__init__(*args, **kwargs)
            self.fields['seminar'].widget.attrs.update({
                'class': 'ui dropdown',
                })

    class Meta:
        model=rdss.models.Signup
        fields='__all__'
        exclude=['payment','receipt_no','ps']

    #def clean_cid(self):
    #       raise forms.ValidationError(
    #               self.error_messages['cid_error'],
    #               code='cid_error'
    #               )
    #       return cid

    def save(self,commit=True):
        record = super(SignupEditForm, self).save(commit=False)
        if commit:
            record.save()
        return record

class SeminarInfoCreationForm(forms.ModelForm):

    class Meta:
        model=rdss.models.SeminarInfo
        fields='__all__'
        exclude=['cid']

    def __init__(self, *args, **kwargs):
            super(SeminarInfoCreationForm, self).__init__(*args, **kwargs)
            self.fields['contact_mobile'].widget.attrs.update({
                'placeholder': '格式：0912-345678',
                })

    #def clean_cid(self):
    #       raise forms.ValidationError(
    #               self.error_messages['cid_error'],
    #               code='cid_error'
    #               )
    #       return cid

    def save(self,commit=True):
        record = super(SeminarInfoCreationForm, self).save(commit=False)
        if commit:
            record.save()
        return record

class JobfairInfoCreationForm(forms.ModelForm):

    class Meta:
        model=rdss.models.JobfairInfo
        fields='__all__'
        exclude=['cid']

    #def clean_cid(self):
    #       raise forms.ValidationError(
    #               self.error_messages['cid_error'],
    #               code='cid_error'
    #               )
    #       return cid

    def save(self,commit=True):
        record = super(JobfairInfoCreationForm, self).save(commit=False)
        if commit:
            record.save()
        return record

class EmailPostForm(forms.Form):
    email = forms.EmailField()

class SurveyForm(forms.ModelForm):
    #def __init__(self, *args, **kwargs):
    #       super(SignupCreationForm, self).__init__(*args, **kwargs)
    #       self.fields['seminar'].widget.attrs.update({
    #           'class': 'ui dropdown',
    #           })

    class Meta:
        model=rdss.models.CompanySurvey
        fields='__all__'

    def save(self,commit=True):
        survey = super(SurveyForm, self).save(commit=False)
        if commit:
            survey.save()
        return survey


class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
           super(StudentForm, self).__init__(*args, **kwargs)
           self.fields['idcard_no'].widget.attrs['autofocus']=True

    class Meta:
        model = rdss.models.Student
        fields = ['idcard_no','student_id','phone', 'name', 'dep']

    def save(self, commit=True):
        form = super(StudentForm, self).save(commit=False)
        if commit:
            form.save()
        return form

class RedeemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
           super(RedeemForm, self).__init__(*args, **kwargs)

    class Meta:
        model = rdss.models.RedeemPrize
        fields = '__all__'
        exclude = ['updated','student']

    def save(self, commit=True):
        form = super(RedeemForm, self).save(commit=False)
        if commit:
            form.save()
        return form
