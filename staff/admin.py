from django.contrib import admin
from staff.models import Staff
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.conf.urls import url,include
import staff.export as export

#class StaffCreationForm(forms.ModelForm):
#	"""A form for creating new users. Includes all the required
#	fields, plus a repeated password."""
#	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#
#	class Meta:
#		model = Staff
#		fields = '__all__'
#
#	def clean_password2(self):
#		# Check that the two password entries match
#		password1 = self.cleaned_data.get("password1")
#		password2 = self.cleaned_data.get("password2")
#		if password1 and password2 and password1 != password2:
#			raise forms.ValidationError("Passwords don't match")
#		return password2
#
#	def save(self, commit=True):
#		# Save the provided password in hashed format
#		user = super(StaffCreationForm, self).save(commit=False)
#		user.set_password(self.cleaned_data["password1"])
#		if commit:
#			user.save()
#		return user
#
#
#class StaffChangeForm(forms.ModelForm):
#	"""A form for updating users. Includes all the fields on
#	the user, but replaces the password field with admin's
#	password hash display field.
#	"""
#	password = ReadOnlyPasswordHashField(label= ("Password"),
#			help_text= ("Raw passwords are not stored, so there is no way to see "
#			"this user's password, but you can change the password "
#			"using <a href=\"../password/\">this form</a>."))
#
#	class Meta:
#		model = Staff
#		fields = '__all__'
#
#	def clean_password(self):
#		# Regardless of what the user provides, return the initial value.
#		# This is done here, rather than on the field, because the
#		# field does not have access to the initial value
#		return self.initial["password"]
#

class StaffAdmin(UserAdmin):
	# The forms to add and change user instances
	#form = StaffChangeForm
	#add_form = StaffCreationForm

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	exclude = ['last_name','first_name','date_joined']
	list_display = ('username','name', 'role','birthday', 'idno', 'account','is_staff', 'is_superuser')
	list_filter = ()
	fieldsets = (
			("基本資料", {
				'classes': ('wide',),
				'fields': ('username','password','name','gender','birthday','g2_email', 'idno','role',
					'mobile','email','fb_url','account_bank','account')
				}
				),
			("權限設定", {
				'classes': ('wide',),
				'fields': ('user_permissions','groups','is_active','is_staff', 'is_superuser')
				}
				),
			)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
			("基本資料", {
				'classes': ('wide',),
				'fields': ('username','password1','password2','name','gender','g2_email','birthday','idno','role',
					'mobile','email','fb_url','account_bank','account')
				}
				),
			("權限設定", {
				'classes': ('wide',),
				'fields': ('user_permissions','groups','is_active','is_staff', 'is_superuser')
				}
				),
			)
	search_fields = ['username', 'name', ]
	ordering = ('role',)
	filter_horizontal = ()
	def get_urls(self):
		urls = super(StaffAdmin, self).get_urls()
		my_urls = [
			url(r'^export/$',export.ExportStaff,name="staff_export"),
		]
		return my_urls + urls

# Now register the new UserAdmin...
admin.site.register(Staff, StaffAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
#admin.site.unregister(Group)
