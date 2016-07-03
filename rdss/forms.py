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
		exclude=['payment']

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
		exclude=['payment',]

	#def clean_cid(self):
	#		raise forms.ValidationError(
	#				self.error_messages['cid_error'],
	#				code='cid_error'
	#				)
	#		return cid

	def save(self,commit=True):
		record = super(SignupEditForm, self).save(commit=False)
		if commit:
			record.save()
		return record

class SeminarInfoCreationForm(forms.ModelForm):

	class Meta:
		model=rdss.models.Seminar_Info
		fields='__all__'
		exclude=[]

	#def clean_cid(self):
	#		raise forms.ValidationError(
	#				self.error_messages['cid_error'],
	#				code='cid_error'
	#				)
	#		return cid

	def save(self,commit=True):
		record = super(SeminarInfoCreationForm, self).save(commit=False)
		if commit:
			record.save()
		return record

class JobfairInfoCreationForm(forms.ModelForm):

	class Meta:
		model=rdss.models.Jobfair_Info
		fields='__all__'
		exclude=[]

	#def clean_cid(self):
	#		raise forms.ValidationError(
	#				self.error_messages['cid_error'],
	#				code='cid_error'
	#				)
	#		return cid

	def save(self,commit=True):
		record = super(JobfairInfoCreationForm, self).save(commit=False)
		if commit:
			record.save()
		return record
