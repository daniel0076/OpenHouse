from django import forms
from .models import StudentApply

class StudentApplyForm(forms.ModelForm):
    class Meta:
        model = StudentApply
        fields = '__all__'
        exclude = ['id']
