from django import forms
import rdss.models
from django.utils import timezone

class ActivityCreationForm(forms.ModelForm):

	class Meta:
		model=rdss.models.Activity
		fields='__all__'
		exclude=['payment',]

	#def clean_cid(self):
	#		raise forms.ValidationError(
	#				self.error_messages['cid_error'],
	#				code='cid_error'
	#				)
	#		return cid

	def save(self,commit=True):
		record = super(ActivityCreationForm, self).save(commit=False)
		if commit:
			record.save()
		return record

class ActivityEditForm(forms.ModelForm):

	class Meta:
		model=rdss.models.Activity
		fields='__all__'
		exclude=['payment',]

	#def clean_cid(self):
	#		raise forms.ValidationError(
	#				self.error_messages['cid_error'],
	#				code='cid_error'
	#				)
	#		return cid

	def save(self,commit=True):
		record = super(ActivityEditForm, self).save(commit=False)
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
