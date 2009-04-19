import xlrd, os, sys, datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'jp_sms.settings'
sys.path.append(os.environ['DATAPY'])
from jp_sms.students.models import StudentBasicInfo, SubjectMaster, Teacher, AttendanceMaster
from jp_sms.students.models import AcademicYear, TestMapping, StudentYearlyInformation, StudentAttendance
from jp_sms.students.models import ClassMaster, StudentTestMarks, StudentAdditionalInformation, Elocution
from jp_sms.students.models import AbhivyaktiVikas, CoCurricular, Competition, CompetitiveExam
from jp_sms.students.models import Project, Library

from jp_sms.fees.models import FeeType, FeeReceipt

def get_yrly_info(regno, year, std, div):
    try:
        basicinfo = StudentBasicInfo.objects.get(RegistrationNo=regno)
    except:
        raise 'regno not found in db'
    try:
        yr = AcademicYear.objects.get(Year=year)
    except:
        raise 'academic year not found'
    try:
        classmaster = ClassMaster.objects.get(Standard=std, AcademicYear=yr,Division=div)
    except:
        raise 'class master not found'
    try:
        yrlyinfo = StudentYearlyInformation.objects.get(StudentBasicInfo=basicinfo, ClassMaster=classmaster)
        return yrlyinfo
    except:
        raise 'StudentYearlyInformation not found'
    

def reg_no():
    book = xlrd.open_workbook('REG.xls')
    sh = book.sheet_by_index(0)
    for rx in range(1, sh.nrows):
        row = sh.row_values(rx)
        a=StudentBasicInfo()
        a.RegistrationNo = row[1]
        a.DateOfRegistration = datetime.date(2008,11,25)
        a.FirstName = row[4].capitalize()
        a.LastName = row[6].capitalize()
        tmp = xlrd.xldate_as_tuple(row[18],0)
        x = datetime.date(tmp[0], tmp[1], tmp[2])
        a.DateOfBirth = datetime.date(tmp[0], tmp[1], tmp[2])
        a.Gender = row[2]
        a.FathersName = row[5].capitalize()
        a.MothersName = ''
        a.save()

def add_rollno():
    yr = AcademicYear.objects.get(Year='2008-2009')
    for xls,std,div in zip(["G10.xls"],[10],['G']):
        print xls, std
        book = xlrd.open_workbook(xls)
        sh = book.sheet_by_index(0)
        for rx in range(2, sh.nrows):
            row = sh.row_values(rx)
            regno = row[0]
            try:
                basicinfo = StudentBasicInfo.objects.get(RegistrationNo=regno)
            except:
                print rx, regno
                sys.exit()
            a = StudentYearlyInformation()
            a.StudentBasicInfo = basicinfo
            a.RollNo = row[1]
            classobj = ClassMaster.objects.get(AcademicYear=yr, Standard=std, Division=div, Type='P')
            a.ClassMaster = classobj
            a.save()
    

def add_test():
    yr = AcademicYear.objects.get(Year='2008-2009')
    for xls, std, div in zip(["../B6.xls"], [6], ['B']):
        book = xlrd.open_workbook(xls)
        sh = book.sheet_by_index(0)
        row = sh.row_values(0)
        tests = row[5:]
        row = sh.row_values(1)
        teachers = row[5:]
        row = sh.row_values(2)
        max_marks = row[5:]
        
        for test, teacher, max_mark in zip(tests, teachers, max_marks):
            subject = test[:3]
            test_type = test[3:]
            
            try:
                SubObj = SubjectMaster.objects.get(Standard=std, Name=subject)
            except:
                print 'unable to get subject. adding: '
                print test, std
                SubObj = SubjectMaster()
                SubObj.Standard = std
                SubObj.Name = subject[:3]
                SubObj.save()
            try:
                TeacherObj = Teacher.objects.get(Name=teacher)
            except:
                print 'unable to get teacher.'
                print teacher
            try:
                TestMappingObj = TestMapping.objects.get(SubjectMaster=SubObj, TestType=test_type, MaximumMarks=max_mark, Teacher=TeacherObj, AcademicYear = yr)
                print test, max_mark, teacher, yr, 'already in DB'
            except:
                TestMappingObj = TestMapping()
                TestMappingObj.SubjectMaster = SubObj
                TestMappingObj.TestType = test_type
                TestMappingObj.MaximumMarks = max_mark
                TestMappingObj.Teacher = TeacherObj
                TestMappingObj.AcademicYear = yr
                TestMappingObj.save()
                print 'Added: ', test, max_mark, teacher, yr


def add_additional_info():
    print "Additional Info"
    yr = AcademicYear.objects.get(Year='2008-2009')
    #for xls, std, div in zip(["../Data.xls"], [9], ['B']):
    xls_file = raw_input('Enter filename: ')
    div = raw_input('Enter Division: ')
    std = raw_input('Enter Standard: ')
    book = xlrd.open_workbook(xls_file)
    sh = book.sheet_by_name('Students Information')
    for rx in range(0,40):
        row = sh.row_values(rx)
        regno = row[0]
        try:
            basicinfo = StudentBasicInfo.objects.get(RegistrationNo=regno)
        except:
            print 'regno: ', regno, ' not found in db'
            continue
        try:
            yrlinfo = StudentAdditionalInformation.objects.get(Id=basicinfo)
            continue
        except:
            yrlinfo = StudentAdditionalInformation()
            yrlinfo.Id = basicinfo
            yrlinfo.Strength = row[1]
            yrlinfo.Weakness = row[2]
            yrlinfo.Sankalp = row[3]
            yrlinfo.Sankalp_Comment = row[4]
            yrlinfo.Hobbies = row[5]
            yrlinfo.Fathers_Income = row[7]
            yrlinfo.Fathers_Education = row[8]
            yrlinfo.Fathers_Occupation = row[9]
            yrlinfo.Fathers_Phone_No = str(row[10]).replace('.0','')
            yrlinfo.Fathers_Email = row[11]
            yrlinfo.Mothers_Income = row[13]
            yrlinfo.Mothers_Education = row[14]
            yrlinfo.Mothers_Occupation = row[15]
            yrlinfo.Mothers_Phone_No = str(row[16]).replace('.0','')
            yrlinfo.Mothers_Email = row[17]
            yrlinfo.Address = row[18]
            yrlinfo.save()
            print 'Added regno: ', regno

def add_attendance():
    print "Attendance"
    xls_file = raw_input('Enter filename: ')
    div=raw_input('Enter Division: ')
    std=raw_input('Enter Standard: ')
    book = xlrd.open_workbook(xls_file)
    sh = book.sheet_by_name('School Attendance')
    yr = '2008-2009'
    months = [6, 7, 8, 9, 10, 11, 12, 1, 2, 3]
    row = sh.row_values(1)
    months_max = row[1:11]
    print months_max
#    sys.exit()
    
    for rx in range(2, sh.nrows):
        row = sh.row_values(rx)
        regno = row[0]
        try:
            yrlyinfo = get_yrly_info(regno, yr, std, div)
        except:
            print 'yearly info not found for', regno
        try:
            classmaster = ClassMaster.objects.get(AcademicYear=yr, Standard=std, Division=div, Type='P')
        except:
            print 'classmaster not in db. ', yr, std, div
            continue
        for month, month_max in zip(months, months_max):
            try:
                attendancemaster = AttendanceMaster.objects.get(ClassMaster=classmaster, Month=month)
            except:
                attendancemaster = AttendanceMaster()
            attendancemaster.ClassMaster = classmaster
            attendancemaster.Month = month
            attendancemaster.WorkingDays = month_max
            if not attendancemaster.WorkingDays:
                attendancemaster.WorkingDays = 0
            attendancemaster.save()
            print "Attendance master not in db. ", classmaster, month
            try:
                studentattendance = StudentAttendance.objects.get(AttendanceMaster=attendancemaster, StudentYearlyInformation=yrlyinfo)
                print 'Found', studentattendance
            except:
                studentattendance = StudentAttendance()
            studentattendance.AttendanceMaster = attendancemaster
            studentattendance.StudentYearlyInformation = yrlyinfo
            tmp = month-5
            if tmp < 0:
                tmp += 12
            if not row[tmp]:
                row[tmp] = 0
            studentattendance.ActualAttendance = row[tmp]
            studentattendance.save()
            print studentattendance, 'added/updated in db'
            


def add_marks():
    yr = AcademicYear.objects.get(Year='2008-2009')    
    for xls, std, div in zip(["../B9.xls"], [9], ['B']):
        book = xlrd.open_workbook(xls)
        sh = book.sheet_by_index(0)
        row = sh.row_values(0)
        subjects = row[5:]
        for subject in subjects:
            try:
                SubObj = SubjectMaster.objects.get(Standard=std, Name=subject[:3])
            except:
                SubObj = SubjectMaster()
                SubObj.Name = subject[:3]
                SubObj.Standard = std
                SubObj.save()
                print 'Added new subject', subject[:3]
        yr = AcademicYear.objects.get(Year='2008-2009')
        row = sh.row_values(1)
        teachers = row[5:]
        row = sh.row_values(2)
        max_marks = row[5:]
        for teacher, subject, max_mark in zip(teachers, subjects, max_marks):
            if teacher:
                try:
                    TeacherObj = Teacher.objects.get(Name=teacher)
                except:
                    print teacher
                    sys.exit()
                try:
                    SubObj = SubjectMaster.objects.get(Standard=std, Name=subject[:3])
                except:
                    print 'Subject does not exist ', subject[:3]
                try:
                    testmapping = TestMapping.objects.get(SubjectMaster = SubObj, TestType = subject[3:], MaximumMarks = max_mark, Teacher = TeacherObj, AcademicYear = yr)
                    continue
                except:
                    testmapping = TestMapping()
                    testmapping.SubjectMaster = SubObj
                    testmapping.TestType = subject[3:]
                    testmapping.MaximumMarks = max_mark
                    testmapping.Teacher = TeacherObj
                    testmapping.AcademicYear = yr
                    testmapping.save()
                    print subject, 'successfully added'
        for rx in range(3, sh.nrows):
            row = sh.row_values(rx)
            row = sh.row_values(rx)
            regno = row[0]
            marks = row[5:]
            for teacher, subject, mark, max_mark in zip(teachers, subjects, marks, max_marks):
                if teacher:
                    try:
                        SubObj = SubjectMaster.objects.get(Standard=std, Name=subject[:3])
                    except:
                        print 'Subject does not exist ', subject[:3]
                        sys.exit()
                    try:
                        TeacherObj = Teacher.objects.get(Name=teacher)
                    except:
                        print 'Teacher does not exist ', teacher
                        sys.exit()
                    try:
                        testmapping = TestMapping.objects.get(TestType=subject[3:], SubjectMaster = SubObj, MaximumMarks = max_mark, Teacher = TeacherObj, AcademicYear = yr)
                    except:
                        print 'TestMapping does not exist ',SubObj, TeacherObj, yr, subject[3:], max_mark
                        sys.exit()
                    try:
                        basicinfo = StudentBasicInfo.objects.get(RegistrationNo=regno)
                    except:
                        print 'Basic info not found ', regno
                        sys.exit()
                    try:
                        classmaster = ClassMaster.objects.get(Standard=std, AcademicYear=yr,Division=div)
                    except:
                        print 'ClassMaster not found ', std, yr, div
                        sys.exit()
                    try:
                        yrlyinfo = StudentYearlyInformation.objects.get(StudentBasicInfo=basicinfo, ClassMaster=classmaster)
                    except:
                        print 'StudentYearlyInformation not found ', basicinfo, classmaster
                        sys.exit()
                    try:
                        a=StudentTestMarks.objects.get(StudentYearlyInformation=yrlyinfo, TestMapping=testmapping)
                        continue
                    except:
                        a = StudentTestMarks()
                        a.StudentYearlyInformation = yrlyinfo
                        a.TestMapping = testmapping
                        if not mark:
                            mark = 0.5
                        a.MarksObtained = mark
                        a.save()
                        print "added successfully", a

def add_b5():
    book = xlrd.open_workbook('B5.xls')
    sh = book.sheet_by_index(0)
    row = sh.row_values(0)
    subjects = row[5:]
    for subject in subjects:
        try:
            SubObj = SubjectMaster.objects.get(Standard=5, Name=subject[:3])
        except:
            SubObj = SubjectMaster()
            SubObj.Name = subject[:3]
            SubObj.Standard = 5
            SubObj.save()
            print 'Added new subject'
    yr = AcademicYear.objects.get(Year='2008-2009')
    row = sh.row_values(1)
    teachers = row[5:]
    row = sh.row_values(2)
    max_marks = row[5:]
    for teacher, subject, max_mark in zip(teachers, subjects, max_marks):
        SubObj = SubjectMaster.objects.get(Standard=5, Name=subject[:3])
        continue
        try:
            TeacherObj = Teacher.objects.get(Name=teacher)
        except:
            print teacher
            sys.exit()
        try:
            testmapping = TestMapping.objects.get(SubjectMaster = SubObj, TestType = subject[3:], MaximumMarks = max_mark, Teacher = TeacherObj, AcademicYear = yr)
            continue
        except:
            testmapping = TestMapping()
            testmapping.SubjectMaster = SubObj
            testmapping.TestType = subject[3:]
            testmapping.MaximumMarks = max_mark
            testmapping.Teacher = TeacherObj
            testmapping.AcademicYear = yr
            testmapping.save()
            print subject, 'successfully added'
    for rx in range(3, sh.nrows):
        row = sh.row_values(rx)
        regno = row[0]
        marks = row[5:]
        for subject, mark in zip(subjects,marks):
            SubObj = SubjectMaster.objects.get(Standard=5, Name=subject[:3])
            TeacherObj = Teacher.objects.get(Name=teacher)
            testmapping = TestMapping.objects.get(TestType=subject[3:], SubjectMaster = SubObj, MaximumMarks = max_marks[i], Teacher = TeacherObj, AcademicYear = yr)
            basicinfo = StudentBasicInfo.objects.get(RegistrationNo=regno)
            classmaster = ClassMaster.objects.get(Standard=5, AcademicYear=yr,Division='B')
            yrlyinfo = StudentYearlyInformation.objects.get(StudentBasicInfo=basicinfo, ClassMaster=classmaster)
            a = StudentTestMarks()
            a.StudentYearlyInformation = yrlyinfo
            a.TestMapping = testmapping
            if not marks[i]:
                marks[i] = 0.5
            a.MarksObtained = marks[i]


def populate_elocution():
    print 'Elocution'
    xls_file = raw_input("Enter filename: ")
    div=raw_input('Enter Division: ')
    std = raw_input("Enter standard: ")
    book = xlrd.open_workbook(xls_file)
    sh = book.sheet_by_name('Elocutions')
    yr = '2008-2009'
    for rx in range(0, sh.nrows):
        row = sh.row_values(rx)
        regno = row[0]
        title = row[1]
        memory = int(round(row[2]))
        content = int(round(row[3]))
        understanding = int(round(row[4]))
        skill = int(round(row[5]))
        presentation = int(round(row[6]))
        row = sh.row_values(rx)
        regno = row[0]
        try:
            yrlyinfo = get_yrly_info(regno, yr, std, div)
        except:
            print 'yearly info not found for', regno
            continue
        try:
            elocution_obj = Elocution.objects.get(StudentYearlyInformation=yrlyinfo, Title=title)
            print 'Found', elocution_obj
        except:
            elocution_obj = Elocution()
        elocution_obj.StudentYearlyInformation = yrlyinfo
        elocution_obj.Title = title
        elocution_obj.Memory = memory
        elocution_obj.Content = content
        elocution_obj.Understanding = understanding
        elocution_obj.Skill = skill
        elocution_obj.Presentation = presentation
        elocution_obj.save()
        print 'successfully added/saved', regno


def populate_fee_receipts():
    print 'Fees'
    xls_file = raw_input("Enter filename: ")
    std = '9'
    yr = '2008-2009'
    book = xlrd.open_workbook(xls_file)
    sh = book.sheet_by_index(0)
    for rx in range(1, sh.nrows):
        row = sh.row_values(rx)
        regno = row[3]
        div = False
        if row[6] == std and row[7] == yr:
            print row
            try:
                basicinfo = StudentBasicInfo.objects.get(RegistrationNo=regno)
            except:
                print 'regno: ', regno, ' not found in db'
                continue
            if basicinfo.Gender == 'M':
                div = 'B'
            elif basicinfo.Gender == 'F':
                div = 'G'
            try:
                classmaster = ClassMaster.objects.get(Standard=std, AcademicYear=yr,Division=div)
            except:
                print 'unable to get '
                continue
            try:
                yrlyinfo = StudentYearlyInformation.objects.get(StudentBasicInfo=basicinfo, ClassMaster=classmaster)
            except:
                print 'StudentYearlyInformation not found ', basicinfo, classmaster
                sys.exit()
            if row[8] == 'SCHOOL FEE':
                fee_type = 'School'
            elif row[8] == 'HOSTEL FEE':
                fee_type = 'Hostel'
            fee_type_obj = FeeType.objects.get(ClassMaster=classmaster, Type=fee_type)
            fee_receipt_obj = FeeReceipt()
            fee_receipt_obj.StudentYearlyInformation = yrlyinfo
            fee_receipt_obj.ReceiptNumber = row[1]
            fee_receipt_obj.FeeType = fee_type_obj
            fee_receipt_obj.Amount = row[9]
            fee_receipt_obj.Status = 1
            tmp = row[2].split('/')
            fee_receipt_obj.Date = datetime.date(2008, int(tmp[0]), int(tmp[1]))
            fee_receipt_obj.save()

def populate_abhivyakti():
    print 'Abhivyakti'
    xls_file = raw_input('Enter filename: ')
    div=raw_input('Enter Division: ')
    std=raw_input('Enter Standard: ')
    book = xlrd.open_workbook(xls_file)
    sh = book.sheet_by_name('Abhivyakti Vikas')
    yr = '2008-2009'
    for rx in range(0, sh.nrows):
        row = sh.row_values(rx)
        regno = row[0]
        mediumofexpression = row[1]
        teacher = row[2]
        try:
            yrlyinfo = get_yrly_info(regno, yr, std, div)
        except:
            print 'yearly info not found for ', regno
            continue
        
        try:
            teacher = Teacher(Name=teacher)
        except:
            print 'Teacher ', row[2], 'not in db'
            continue
        try:
            abhivyakti_obj = AbhivyaktiVikas.objects.get(StudentYearlyInformation=yrlyinfo)
            print abhivyakti_obj, 'Already available in database'
        except:
            abhivyakti_obj = AbhivyaktiVikas()
            abhivyakti_obj.StudentYearlyInformation = yrlyinfo
            abhivyakti_obj.Teacher = teacher
            abhivyakti_obj.MediumOfExpression = mediumofexpression
            abhivyakti_obj.save()
            print 'Sucessfully added', abhivyakti_obj
            
        

def populate_cocurricular():
    print 'Cocurricular'
    xls_file = raw_input('Enter filename: ')
    div=raw_input('Enter Division: ')
    std=raw_input('Enter Standard: ')
    book = xlrd.open_workbook(xls_file)
    sh = book.sheet_by_index(1)
    yr = AcademicYear.objects.get(Year='2008-2009')
    for rx in range(5, 83):
        row = sh.row_values(rx)
        regno = row[0]
        activity = row[1]
        tmp = row[3].split('/')
        if tmp[2] == '08':
            tmp[2] = '2008'
        date = datetime.date(int(tmp[2]), int(tmp[1]), int(tmp[0]))
        guide = row[4]
        try:
            basicinfo = StudentBasicInfo.objects.get(RegistrationNo=regno)
        except:
            print 'regno: ', regno, ' not found in db'
            continue
        try:
            classmaster = ClassMaster.objects.get(Standard=std, AcademicYear=yr,Division=div)
        except:
            print 'unable to get '
            continue
        try:
            yrlyinfo = StudentYearlyInformation.objects.get(StudentBasicInfo=basicinfo, ClassMaster=classmaster)
        except:
            print 'StudentYearlyInformation not found ', basicinfo, classmaster
            continue
        try:
            cocurricular_obj = CoCurricular.objects.get(StudentYearlyInformation=yrlyinfo, Activity=activity)
            print cocurricular_obj, 'already in db'
        except:
            cocurricular_obj = CoCurricular()
            cocurricular_obj.StudentYearlyInformation = yrlyinfo
            cocurricular_obj.Activity = activity
            cocurricular_obj.Date = date
            cocurricular_obj.Guide = guide
            cocurricular_obj.save()
            print 'Successfully added', cocurricular_obj

def populate_competitions():
    print 'Competitions'
    xls_file = raw_input('Enter filename: ')
    div = raw_input('Enter Division: ')
    std = raw_input('Enter Standard: ')
    book = xlrd.open_workbook(xls_file)
    yr = '2008-2009'
    sh = book.sheet_by_name('Competitions')
    for rx in range(0, sh.nrows):
        row = sh.row_values(rx)
        regno = row[0]
        try:
            yrlyinfo = get_yrly_info(regno, yr, std, div)
        except:
            print 'yearly info not found for', regno
            continue
        print row
        organizer = row[1]
        subject = row[2]
        tmp = row[3].split('/')
        if tmp[2] == '08':
            tmp[2] = '2008'
        date = datetime.date(int(tmp[2]), int(tmp[1]), int(tmp[0]))
        achievement = row[4]
        guide = row[5]
        try:
            competetion_obj = Competition.objects.get(StudentYearlyInformation=yrlyinfo, Organizer=organizer, Subject=subject, Date=date, Achievement=achievement, Guide=guide)
        except:
            competetion_obj = Competition()
            competetion_obj.StudentYearlyInformation = yrlyinfo
            competetion_obj.Organizer = organizer
            competetion_obj.Subject = subject
            competetion_obj.Date = date
            competetion_obj.Achievement = achievement
            competetion_obj.Guide = guide
            competetion_obj.save()
            print competetion_obj, 'added in db'
    
def populate_competitiveexam():
    print 'CompetitiveExam'
    xls_file = raw_input('Enter filename: ')
    div = raw_input('Enter Division: ')
    std = raw_input('Enter Standard: ')
    book = xlrd.open_workbook(xls_file)
    yr = '2008-2009'
    sh = book.sheet_by_name('Competitive Exams')
    for rx in range(0, sh.nrows):
        row = sh.row_values(rx)
        regno = row[0]
        try:
            yrlyinfo = get_yrly_info(regno, yr, std, div)
        except:
            print 'yearly info not found for', regno
            continue
        print row
        name = row[1]
        subject = row[2]
        level = row[3]
        date = False
        if row[4]:
            tmp = row[4].split('/')
            date = datetime.date(int(tmp[2]), int(tmp[1]), int(tmp[0]))
        else:
            date = datetime.date(1,1,1)
        grade = row[5]
        try:
            competitiveexam_obj = CompetitiveExam.objects.get(StudentYearlyInformation=yrlyinfo, Name=name, Subject=subject, Level=level, Grade=grade)
        except:
            competitiveexam_obj = CompetitiveExam()
            competitiveexam_obj.StudentYearlyInformation = yrlyinfo
            competitiveexam_obj.Name = name
            competitiveexam_obj.Subject = subject
            competitiveexam_obj.Date = date
            competitiveexam_obj.Level = level
            competitiveexam_obj.Grade = grade
            competitiveexam_obj.save()
            print competitiveexam_obj, 'added in db'

def populate_project():
    print 'Projects'
    xls_file = raw_input('Enter filename: ')
    div = raw_input('Enter Division: ')
    std = raw_input('Enter Standard: ')
    book = xlrd.open_workbook(xls_file)
    yr = '2008-2009'
    sh = book.sheet_by_name('Projects')
    for rx in range(0, 42):
        row = sh.row_values(rx)
        regno = row[0]
        try:
            yrlyinfo = get_yrly_info(regno, yr, std, div)
        except:
            print 'yearly info not found for', regno
            continue
        print row
        title = row[1]
        proj_types = {}
        proj_types['Collection, classification'] = 'CC'
        proj_types['Investigation'] = 'I'
        proj_types['Investigation by Survey'] = 'IS'
        proj_types['Creative Production'] = 'CP'
        proj_types['Appreciation- criticism'] = 'AC'
        proj_types['Open Ended Exploration'] = 'O'
        proj_type = proj_types[row[2]]
        subject = row[3]
        try:
            project_obj = Project.objects.get(StudentYearlyInformation=yrlyinfo, Title=title, Subject=subject, Type=proj_type)
        except:
            project_obj = Project()
            project_obj.StudentYearlyInformation = yrlyinfo
            project_obj.Title = title
            project_obj.Subject = subject
            project_obj.Type = proj_type
            project_obj.save()
            print project_obj, 'added in db'


def populate_library():
    print 'Library'
    xls_file = raw_input('Enter filename: ')
    div = raw_input('Enter Division: ')
    std = raw_input('Enter Standard: ')
    book = xlrd.open_workbook(xls_file)
    yr = '2008-2009'
    sh = book.sheet_by_name('Library')
    for rx in range(1, 41):
        row = sh.row_values(rx)
        regno = row[0]
        try:
            yrlyinfo = get_yrly_info(regno, yr, std, div)
        except:
            print 'yearly info not found in db for ', regno
        print row
        booksread = row[1]
        grade = row[2]
        comment = row[3]
        try:
            library_obj = Library.objects.get(StudentYearlyInformation=yrlyinfo, BooksRead=booksread, Grade=grade, PublicComment=comment)
        except:
            library_obj = Library()
            library_obj.StudentYearlyInformation = yrlyinfo
            library_obj.BooksRead = booksread
            library_obj.Grade = grade
            library_obj.PublicComment = comment
            library_obj.save()
            print library_obj, 'added in db'

def populate_subjects():
    #subjects = ['Mathematics', 'English', 'Geography', 'Hindi', 'History', 'Marathi','Sanskrit', 'Science']
    subject = {}
    sub = {}
    subject['5'] = 'ENGF1	ENGN1	ENGQ1	ENGQ2	ENGT1	GEOF1	GEON1	GEOQ1	GEOQ2	GEOT1	HINF1	HINN1	HINQ1	HINQ2	HINT1	HISF1	HISN1	HISQ1	HISQ2	HIST1	MARF1	MARN1	MARQ1	MARQ2	MART1	MATF1	MATN1	MATQ1	MATQ2	MATT1	SANF1	SANN1	SANQ1	SANQ2	SANT1	SATA1	SATA2	SATA3	SATA4	SATB1	SATB2	SATB3	SATB4	SCIF1	SCIN1	SCIQ1	SCIQ2	SCIT1'
    subject['6'] = 'ENGF1	ENGN1	ENGQ1	ENGQ2	ENGT1	GEOF1	GEON1	GEOQ1	GEOQ2	GEOT1	HINF1	HINN1	HINQ1	HINQ2	HINT1	HISF1	HISN1	HISQ1	HISQ2	HIST1	MARF1	MARN1	MARQ1	MARQ2	MART1	MATF1	MATN1	MATQ1	MATQ2	MATT1	SANF1	SANN1	SANQ1	SANQ2	SANT1	SATA1	SATA2	SATA3	SATA4	SATB1	SATB2	SATB3	SATB4	SCIF1	SCIN1	SCIQ1	SCIQ2	SCIT1	COMT1'
    subject['7'] = 'ELOC1	ENGF1	ENGN1	ENGQ1	ENGQ2	ENGT1	FIRS1	GEOF1	GEON1	GEOQ1	GEOQ2	GEOT1	HINF1	HINN1	HINQ1	HINQ2	HINT1	HISF1	HISN1	HISQ1	HISQ2	HIST1	INTE1	MAPS1	MARF1	MARN1	MARQ1	MARQ2	MART1	MATF1	MATN1	MATQ1	MATQ2	MATT1	NOTM1	POST1	RECE1	RECH1	RECM1	RECS1	REDS1	SANF1	SANN1	SANQ1	SANQ2	SANT1	SATA1	SATA2	SATA3	SATA4	SATB1	SATB2	SATB3	SATB4	SCIF1	SCIN1	SCIQ1	SCIQ2	SCIT1	SCRB1'
    subject['8'] = 'ENGF1	ENGN1	ENGQ1	ENGQ2	ENGT1	GEOF1	GEON1	GEOQ1	GEOQ2	GEOT1	HINF1	HINN1	HINQ1	HINQ2	HINT1	HISF1	HISN1	HISQ1	HISQ2	HIST1	MARF1	MARN1	MARQ1	MARQ2	MART1	MATF1	MATN1	MATQ1	MATQ2	MATT1	SANF1	SANN1	SANQ1	SANQ2	SANT1	SATA1	SATA2	SATA3	SATA4	SATB1	SATB2	SATB3	SATB4	SCIF1	SCIN1	SCIQ1	SCIQ2	SCIT1	COMT1'
    subject['9'] = 'ENGF1	ENGN1	ENGQ1	ENGQ2	ENGT1	GEOF1	GEON1	GEOQ1	GEOQ2	GEOT1	HISF1	HISN1	HISQ1	HISQ2	HIST1	MATF1	MATN1	MATQ1	MATQ2	MATT1	SANF1	SANN1	SANQ1	SANQ2	SANT1	SATA1	SATA2	SATA3	SATA4	SATB1	SATB2	SATB3	SATB4	SCIF1	SCIN1	SCIQ1	SCIQ2	SCIT1	COMT1'
    subject['10'] = 'ENGF1	ENGGR	ENG_CD	MATF1	MATGR	MAT_CD	SANF1	SANGR	SAN_CD	SCIF1	SCIGR	SCI_CD  SOCF1';
    for std in subject.keys():
        subjects = subject[std].split('\t')
        y = {}
        for x in subjects:
            y[x[:3]] = 1
        sub[std] = y.keys()
    for std in sub.keys():
        for subject in sub[std]:
            a=SubjectMaster()
            a.Name = subject
            a.Standard = std
            a.save()


def populate_teachers():
    teachers = []
    teachers.sort()
    for teacher in teachers:
        try:
            a=Teacher.objects.get(Name=teacher)
            print a, 'is already available in database'
        except:
            a = Teacher()
            a.Name = teacher
            a.Email = teacher.lower().replace(' ','.')+'@jnanapraboadhini.org'
            a.ResidenceNo = '+912024207000'
            a.MobileNo = '0'
            a.save()
            print "added: ", a

def add_yrly_info():
    book = xlrd.open_workbook('B5.xls')
    sh = book.sheet_by_index(0)
    yr = AcademicYear.objects.get(Year='2007-2008')
    
    for rx in range(2, sh.nrows):
        row = sh.row_values(rx)
        regno = row[0]
        rollno = row[1]
        yrlyinfo = StudentYearlyInformation()
        basicinfo = StudentBasicInfo.objects.get(RegistrationNo = regno)
        yrlyinfo.StudentBasicInfo = basicinfo
        yrlyinfo.RollNo = rollno
        classmaster = ClassMaster.objects.get(Standard=5, AcademicYear=yr,Division='B')
        yrlyinfo.ClassMaster = classmaster
        yrlyinfo.save()

populate_abhivyakti()
populate_competitiveexam()
populate_competitions()
populate_elocution()
add_attendance()
sys.exit()
