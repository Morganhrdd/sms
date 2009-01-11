import xlrd, os, sys, datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'jp_sms.settings'
sys.path.append('/Users/shantanoo/repo')
from jp_sms.students.models import StudentBasicInfo, SubjectMaster, Teacher, AcademicYear, TestMapping, StudentYearlyInformation, ClassMaster, StudentTestMarks

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

def add_b5():
    book = xlrd.open_workbook('B5.xls')
    sh = book.sheet_by_index(0)
    row = sh.row_values(0)
    x = 41
    y = 5
    tests = row[x:x+y]
    row = sh.row_values(1)
    max_marks = row[x:x+y]
    teachers = ['Mrudula Pathak']
    yr = AcademicYear.objects.get(Year='2007-2008')
    for i in range(len(tests)):
        test = tests[i]
        max_mark = max_marks[i]
        
        testmapping = TestMapping()
        testmapping.TestType = test[3:]
        subject = test[:3]
        SubObj = SubjectMaster.objects.get(Standard=5, Name=subject)
        testmapping.SubjectMaster = SubObj
        testmapping.Teacher = Teacher.objects.get(Name=teachers[0]) ###
        testmapping.AcademicYear = yr
        testmapping.MaximumMarks = max_mark
        testmapping.save()
    for rx in range(2, sh.nrows):
        row = sh.row_values(rx)
        regno = row[0]
        marks = row[x:x+y]
        for i in range(len(tests)):
            subject = tests[i][:3]
            testtype = tests[i][3:]
            SubObj = SubjectMaster.objects.get(Standard=5, Name=subject)
            TeacherObj = Teacher.objects.get(Name=teachers[0]) ###
            
            testmapping = TestMapping.objects.get(TestType=testtype, SubjectMaster = SubObj, MaximumMarks = max_marks[i], Teacher = TeacherObj, AcademicYear = yr)
            basicinfo = StudentBasicInfo.objects.get(RegistrationNo=regno)
            classmaster = ClassMaster.objects.get(Standard=5, AcademicYear=yr,Division='B')
            yrlyinfo = StudentYearlyInformation.objects.get(StudentBasicInfo=basicinfo, ClassMaster=classmaster)
            a = StudentTestMarks()
            a.StudentYearlyInformation = yrlyinfo
            a.TestMapping = testmapping
            if not marks[i]:
                marks[i] = 0.5
            a.MarksObtained = marks[i]
            a.save()

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
    teachers = ['Vivek Ponkshe', 'Bhagyashree Harshe', 'Milind Naik', 'Shantala Kulkarni', 'Kalyani Keskar', 'Neha Abhyankar','Mrudula Pathak','Mukulika Thatte','Ragini Naik','Rohini Dhavale', 'Prashant Divekar','Kanchan Abhyankar', 'Ashwini Joshi', 'Sheetal Pasalkar', 'Laxmi Roshan', 'Anil Joshi', 'Rekha Paigude', 'Siddharth Dhomkar']
    for teacher in teachers:
        a = Teacher()
        a.Name = teacher
        a.Email = teacher.lower().replace(' ','.')+'@jnanaprabpdhini.org'
        a.ResidenceNo = '+91204207000'
        a.MobileNo = '0'
        a.save()


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

