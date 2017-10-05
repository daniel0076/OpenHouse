from django.conf.urls import url
import rdss.views as views
import staff.export as export

urlpatterns = [
    url(r'^export_staff/$',export.ExportStaff, name="staff_export_staff"),
]
