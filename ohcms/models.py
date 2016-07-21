from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index


# Index Page
class Index(Page):
	body = RichTextField('內文', blank=True)

	search_name = '首頁'
	template = 'ohcms/index.html'

	#def __init__(self, *args, **kwargs):
	#    year = str(date.today().year + 1)
	#    self._meta.get_field('title').default           = year
	#    self._meta.get_field('slug').default            = year
	#    self._meta.get_field('show_in_menus').default   = True
	#    super(Index, self).__init__(*args, **kwargs)

	class Meta:
		verbose_name = '首頁'

	content_panels = [
			FieldPanel('title', classname='full'),
			FieldPanel('body', classname='full'),
			]


class News(Page):
	body = RichTextField('內文')
	create_time = models.DateTimeField('發佈時間', auto_now_add=True)
	update_time = models.DateTimeField('更新時間', auto_now=True)

	#def __init__(self, *args, **kwargs):
	#	self._meta.get_field('slug').default            = ''
	#	self._meta.get_field('title').default           = ''
	#	self._meta.get_field('show_in_menus').default   = False
	#	super(News, self).__init__(*args, **kwargs)

	subpage_types = tuple()

	class Meta:
		verbose_name = '公告'

	content_panels = [
			FieldPanel('title', classname='full'),
			FieldPanel('body', classname='full'),
			]


