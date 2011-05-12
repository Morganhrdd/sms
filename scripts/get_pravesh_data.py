# copy following after running 'manage.py shell'
from pravesh.models import *
s = Student.objects.all()
import xlwt
wb = Workbook()
wb = xlwt.Workbook()
ws = wb.add_sheet('2011-12 Pravesh')

cols = ['FirstName', 'MiddleName', 'LastName', 'FatherName', 'MotherName', 'Address', 'Pincode', 'PhoneHome', 'PhoneMobile', 'Email', 'Medium', 'Gender', 'DateOfBirth', 'CurrentSchool', 'CurrentStd', 'PayMode', 'DDNo']
for i in range(len(cols)):
    ws.write(0,i, cols[i])

r = 1
for x in s:
    for i in range(len(cols)):
        ws.write(r, i, getattr(x,cols[i]))
    r += 1

wb.save('pravesh_2011-2012.xls')