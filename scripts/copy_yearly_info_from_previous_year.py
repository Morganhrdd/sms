# copy following after running 'manage.py shell'
from students.models import *
import sys

prev_year = raw_input("Enter previous year: ")
next_year = raw_input("Enter next year: ")
for std in [5,6,7,8,9]:
    try:
        s = StudentYearlyInformation.objects.filter(ClassMaster__Standard=std, ClassMaster__AcademicYear__Year=prev_year)
    except Exception, e:
        print e
        sys.exit(1)
    for x in s:
        i += 1
        n = StudentYearlyInformation()
        n.StudentBasicInfo = x.StudentBasicInfo
        n.RollNo = x.RollNo
        n.ClassMaster = ClassMaster.objects.get(Standard=std+1, Division=x.ClassMaster.Division, AcademicYear__Year=next_year)
        n.Hostel = '1' # No hostel set to all
        n.save()
        print n

