from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render,redirect
import xlsxwriter
import staff.models







# Create the HttpResponse object with the appropriate Excel Header
@staff_member_required
def ExportStaff(request):
    filename = "staff_{}.xlsx".format(timezone.localtime(timezone.now()).strftime("%m%d"))
    response = HttpResponse(content_type='application/ms-excel') # microsoft excel
    response['Content-Disposition'] = 'attachment; filename=' + filename

    with xlsxwriter.Workbook(response) as workbook:
        staff_worksheet = workbook.add_worksheet("通訊錄") # set the excel sheet
        staff_worksheet.write(0,0,"學號")# set the title for each colume
        staff_worksheet.write(0,1,"姓名")
        staff_worksheet.write(0,2,"手機")
        staff_worksheet.write(0,3,"信箱")
        staff_worksheet.write(0,4,"職位")

        staff_list = staff.models.Staff.objects.all()
        for row_count, staffs in enumerate(staff_list,1):
            if staffs.is_staff:
                staff_worksheet.write(row_count,0,staffs.username)
                staff_worksheet.write(row_count,1,staffs.name)
                staff_worksheet.write(row_count,2,staffs.mobile)
                staff_worksheet.write(row_count,3,staffs.g2_email)
                staff_worksheet.write(row_count,4,staffs.role)
    return response
