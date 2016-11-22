from django import forms
from . import models
from django.utils import timezone

class SignupForm(forms.ModelForm):
    required_css_class="required field"

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['mentor'].widget.attrs.update({
            'class': 'ui disabled dropdown',
        })

    class Meta:
        model=models.Signup
        fields='__all__'
        exclude=['id','updated','ps']
        widgets = {
            'question': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }

    def save(self,commit=True):
        form = super(SignupForm, self).save(commit=False)
        if commit:
            form.save()
            return form
