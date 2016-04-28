from django.contrib.auth.backends import ModelBackend
from staff.models import Staff
from django.contrib.auth.models import User

class StaffBackend(ModelBackend):
	"""
	OpenHouse Staff Backend
	"""

	def authenticate(self, username=None, password=None, **kwargs):
		try:
			user = Staff._default_manager.get_by_natural_key(username=username)
			if user.check_password(password):
				return user
		except Staff.DoesNotExist:
			# Run the default password hasher once to reduce the timing
			# difference between an existing and a non-existing user (#20760).
			#UserModel().set_password(password)
			return None

	def get_user(self, user_id):
		"""
		With this method,
		backend can get the correct Staff
		"""
		try:
			user = Staff.objects.get(id=user_id)
			return user
		except Staff.DoesNotExist:
			return None
