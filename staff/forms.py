from django import forms
import staff.models
from django.utils import timezone

class StaffCreationForm(forms.ModelForm):
	error_messages={
			'password_mismatch': ('兩次輸入的密碼不一樣'),
			}
	#customed fields
	password1 = forms.CharField(label=(u'密碼'), widget=forms.PasswordInput)
	password2 = forms.CharField(label=(u'密碼確認'),
			widget=forms.PasswordInput, help_text=('請再次輸入密碼'))

	required_css_class = 'required'

	def __init__(self, *args, **kwargs):
		super(StaffCreationForm, self).__init__(*args, **kwargs)
		self.fields['username'].label="學號(帳號)"

	class Meta:
		model=staff.models.Staff
		fields='__all__'
		exclude=['id','last_name','first_name','password','last_login','is_active','groups','is_superuser','user_permissions','is_staff','date_joined']
		help_texts = {
				'username': ('請輸入學號'),
				}

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
		user = super(StaffCreationForm, self).save(commit=False)
		user.last_login=timezone.now()
		user.set_password(self.cleaned_data['password2'])
		user.is_active = False
		if commit:
			user.save()
		return user
