import os
import sys
import datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'sms.settings'
sys.path.append(os.environ['DATAPY'])
from sms.students.models import *
from sms.fees.models import *

op = {}


op['StudentBasicInfo'] = []
#op['StudentAdditionalInformation'] = []
#op['StudentYearlyInformation'] = []

#op['StudentBasicInfo'].append(['RegistrationNo', 'eq', 3000])
#op['StudentBasicInfo'].append(['RegistrationNo', 'gt', 3000])
#op['StudentBasicInfo'].append(['RegistrationNo', 'lte', 3010])
#op['StudentBasicInfo'].append(['DateOfRegistration','range', (datetime.date(2009,01,01), datetime.date(2009,12,31))])
#op['StudentBasicInfo'].append(['FirstName','startswith', 'A'])
#op['StudentAdditionalInformation'].append(['Fathers_Email', 'startswith', 'a'])
def get_rows(tbl=None, ops=None, default=None):
    if not ops:
        if not default:
            return []
        else:
            return getattr(tbl, 'objects').all()
    
    kargs = {}
    for x in ops:
        if x[1] == 'eq':
            kargs[x[0]] = x[2]
        else:
            kargs[x[0]+'__'+x[1]] = x[2]
    return getattr(tbl, 'objects').filter(**kargs)
def main(op):
    r = []
    student_basic_info = set(get_rows(StudentBasicInfo, op['StudentBasicInfo']))
    if 'StudentAdditionalInformation' in op and op['StudentAdditionalInformation']:
        student_additional_information = set(get_rows(StudentAdditionalInformation, op['StudentAdditionalInformation']))
        student_basic_info = student_basic_info.intersection([x.Id for x in student_additional_information])
    if 'StudentYearlyInformation' in op:
        student_yearly_information = set(get_rows(StudentYearlyInformation, op['StudentYearlyInformation']))
        student_basic_info = student_basic_info.intersection([x.Id for x in student_yearly_information])
    for x in student_basic_info:
        print x
    print len(student_basic_info)
main(op)