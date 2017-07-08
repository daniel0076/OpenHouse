class OH_router(object):
	"""
	A router to control all database operations on models in the
	auth application.
	"""

	def __init__(self):
		self.current_year_db="oh_2017"
		self.use_separate_db_list = ['rdss','recruit','comapny_list']

	def db_for_read(self, model, **hints):
		if model._meta.app_label in self.use_separate_db_list:
			return self.current_year_db
		return 'default'

	def db_for_write(self, model, **hints):
		if model._meta.app_label in self.use_separate_db_list:
			return self.current_year_db
		return 'default'

	def allow_relation(self, obj1, obj2, **hints):
		return None

	def allow_migrate(self, db, app_label, model_name=None, **hints):
		if app_label in self.use_separate_db_list:
			return db == self.current_year_db
		else:
			return db == 'default'
