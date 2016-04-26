
from django import forms
from RDSS_2016.models import Company
from django.utils import timezone

class CompanyCreationForm(forms.ModelForm):

    error_messages={
        'password_mismatch': ('兩次輸入的密碼不一樣'),
        'cid_error': ('統一編號必需都是數字'),
    }
    #customed fields
    cid= forms.CharField(label=(u'公司統一編號'),help_text='請輸入8位數統一編號')
    password1 = forms.CharField(label=(u'密碼'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=(u'密碼確認'),
        widget=forms.PasswordInput, help_text=('請再次輸入密碼'))

    required_css_class = 'required'

    class Meta:
        model=Company
        fields='__all__'
        exclude=['id','password','last_login','is_active']

    def clean_cid(self):
        cid=self.cleaned_data.get('cid')
        if not cid.isdigit():
            raise forms.ValidationError(
                    self.error_messages['cid_error'],
                    code='cid_error'
                    )
        return cid

    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch'
                    )
        return password2

    def save(self,commit=True):
        user = super(CompanyCreationForm, self).save(commit=False)
        user.last_login=timezone.now()
        user.set_password(self.cleaned_data['password2'])
        user.is_active=1;
        if commit:
            user.save()
        return user

class CompanyEditForm(forms.ModelForm):

    error_messages={
        'password_mismatch': ('兩次輸入的密碼不一樣'),
        'cid_error': ('統一編號必需都是數字'),
    }
    #customed fields
    cid= forms.CharField(label=(u'公司統一編號'))
    password1 = forms.CharField(required=False,label=(u'密碼'), widget=forms.PasswordInput)
    password2 = forms.CharField(required=False,label=(u'密碼確認'),
    widget=forms.PasswordInput, help_text=('請再次輸入密碼'))

    required_css_class = 'required'

    class Meta:
        model=Company
        fields='__all__'
        exclude=['cid','password','last_login','date_join','is_active']

#ref here https://docs.djangoproject.com/en/1.8/ref/forms/validation/  search clean_
    def clean_cid(self):
        cid=self.cleaned_data.get('cid')
        if not cid.isdigit():
            raise forms.ValidationError(
                    self.error_messages['cid_error'],
                    code='cid_error'
                    )
        return cid

    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch'
                    )
        return password2

    def save(self,commit=True):
        user = super(CompanyCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user

class CompanySelfCreationForm(CompanyCreationForm):
    class Meta:
        model=Company
        fields='__all__'
        exclude=['password','last_login','date_join','is_active']

class CompanySelfEditForm(CompanyEditForm):
    class Meta:
        model=Company
        fields='__all__'
        exclude=['cid','password','last_login','date_join','is_active']

