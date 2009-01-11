# Create your views here.
from django.db.models import Q
from django.shortcuts import render_to_response
from models import StudentBasicInfo
from django.http import HttpResponse 
from jp_sms.students.models import TestMapping, StudentTestMarks, StudentYearlyInformation, SubjectMaster, ClassMaster, SubjectMaster, AttendanceMaster, StudentAttendance, StudentAdditionalInformation
from django.template import Context
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,Frame,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib import colors
import os

PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

Title = "Jnana Prabodhini Prashala"
pageinfo = "School Report"

def report(request):
   # SubObj = SubjectMaster.objects.get(Standard=5, Name='hindi')
    #print SubObj
    #test = TestMapping.objects.get(SubjectMaster=SubObj)
    #print test
    student = StudentYearlyInformation.objects.get(id=1)
    print student
    
    student_data = []
    student_data.append({'FirstName':student.StudentBasicInfo.FirstName,'LastName':student.StudentBasicInfo.LastName})
    
    marks = StudentTestMarks.objects.filter(StudentYearlyInformation=student)
    mark_data = []
    for mark in marks:
        print mark.MarksObtained
        mark_data.append({'MarksObtained':mark.MarksObtained , 'MaximumMarks':mark.TestMapping.MaximumMarks ,'Subject_Name':mark.TestMapping.SubjectMaster.Name,'test_type':mark.TestMapping.TestType})
        
    attendances = StudentAttendance.objects.filter(StudentYearlyInformation = student)
    attendance_data = []
    for attendance in attendances:
        print attendance.ActualAttendance
        attendance_data.append({'Month':attendance.AttendanceMaster.Month , 'Attendance':attendance.ActualAttendance , 'Working_days':attendance.AttendanceMaster.WorkingDays})
        
    return render_to_response('Marks_Report.html',Context({'student_data':student_data ,'mark_data':mark_data , 'attendance_data':attendance_data}))

def marks_add(request):
    if request.POST:
        keys = request.POST.keys()
        test_id = request.POST['test_id']
        keys.remove('test_id')
        for key in keys:
            print request.POST[key]
            test = TestMapping.objects.get(id=test_id)
            student = StudentYearlyInformation.objects.get(id=key)
            a = StudentTestMarks.objects.filter(StudentYearlyInformation=student, TestMapping=test)
            a.delete()
            a = StudentTestMarks()
            a.TestMapping = test
            a.StudentYearlyInformation = student
            a.MarksObtained = request.POST[key]
            a.save()
        return HttpResponse('Successfully added record.<br/>\n<a href="http://localhost:8000/marks_add">Select test for entering data</a>')
    else:
        if not request.GET.has_key('test_id'):
            tests = TestMapping.objects.all()
            test_details = ''
            for test in tests:
                test_details += '<a href="http://localhost:8000/marks_add/?test_id='+str(test.id)+ '">' + '%s' %(test) + '</a><br/>'
            return HttpResponse(test_details)
        test_id = request.GET['test_id']
        test = TestMapping.objects.get(id=test_id)

        subject = SubjectMaster.objects.get(id=test.SubjectMaster.id)

        class_masters = ClassMaster.objects.filter(AcademicYear=test.AcademicYear, Standard=subject.Standard)
        data = []
        for class_master in class_masters:
            students = StudentYearlyInformation.objects.filter(ClassMaster=class_master.id)
            test_details = 'Standard: %s, Subject Name: %s, Academic Year: %s, TestType: %s, Max Marks: %s' % (subject.Standard, subject.Name, test.AcademicYear, test.TestType, test.MaximumMarks)
            for student in students:
                student_info = StudentBasicInfo.objects.get(RegistrationNo = student.StudentBasicInfo.RegistrationNo)
                name = '%s %s' % (student_info.FirstName, student_info.LastName)
                print name
	        data.append({'id':student.id, 'name': name, 'rollno':student.RollNo })
        return render_to_response('AddMarks.html',Context({'test_details': test_details,'test_id':test_id, 'data':data}))


def attendance_add(request):
    if request.POST:
        keys = request.POST.keys()
        attendance_id = request.POST['attendance_id']
        keys.remove('attendance_id')
        print attendance_id
        for key in keys:
            attendance_master = AttendanceMaster.objects.get(id = attendance_id)
            student = StudentYearlyInformation.objects.get(id = key)
            a = StudentAttendance.objects.filter(AttendanceMaster = attendance_master, StudentYearlyInformation = student)
            a.delete()
            a = StudentAttendance()
            a.AttendanceMaster = attendance_master
            a.StudentYearlyInformation = student
            a.ActualAttendance = request.POST[key]
            a.save()
        return HttpResponse('Successfully added record.<br/>\n<a href="http://localhost:8000/attendance_add">Select test for entering data</a>')
    else:
        if not request.GET.has_key('attendance_id'):
            attendancemaster = AttendanceMaster.objects.all()
            attendance_details = ''
            for attendance in attendancemaster:
                attendance_details += '<a href="http://localhost:8000/attendance_add/?attendance_id='+str(attendance.id)+'">'+'%s' %(attendance) + '</a><br/>'
            return HttpResponse(attendance_details)
        attendance_id = request.GET['attendance_id']
        attendance = AttendanceMaster.objects.get(id=attendance_id)
        students = StudentYearlyInformation.objects.filter(ClassMaster=attendance.ClassMaster)
        data = []
        for student in students:
            student_info = StudentBasicInfo.objects.get(RegistrationNo = student.StudentBasicInfo.RegistrationNo)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            data.append({'id':student.id,'roll_no':student.RollNo, 'name':name})
        return render_to_response('AddAttendance.html',Context({'attendance_id':attendance_id, 'attendance_details':attendance.ClassMaster, 'data':data}))
    return HttpResponse()

	

def firstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold',16)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-100, "Jnana Prabodhini Prashala")
    canvas.setFont('Times-Roman',12)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-115, "510 Sadashiv Peth Pune 411030")
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-130, "Email: prashala@jnanaprabodhini.org")
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)


def laterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
    canvas.restoreState()

def go(request):
    for param in os.environ.keys():
        print "%20s %s" % (param,os.environ[param])
    #return HttpResponse()
    if request.GET.has_key('id'):
        response = HttpResponse(mimetype='application/pdf')
        doc = SimpleDocTemplate(response)
        Story = []
        fillStaticAndYearlyInfo(Story)
        fillAcademicReport(Story)
        # fillCoCurricularReport(Story)
        # fillOutdoorActivityReport(Story)
        # fillLibraryReport(Story)
        doc.build(Story, onFirstPage=firstPage)
        return response
    else:
        return HttpResponse('Id not provided')
    
def fillStaticAndYearlyInfo(Story):
    student = StudentYearlyInformation.objects.get(id=1)
    student_basic_info = StudentBasicInfo.objects.get(RegistrationNo = student.StudentBasicInfo.RegistrationNo)
    #student_addtional_info = StudentAdditionalInformation.objects.get(Id = student_basic_info.RegistrationNo)
    Story.append(Spacer(1,1*inch))
#    im = Image(student.photo,width= 100,height=100)
    data=[['Certificate of School Based Evaluation','',''],
          ['Part 1: General Information(Static and yearly info)','',''],
          ['Name:' + student_basic_info.FirstName + ' ' + student_basic_info.LastName,'',[]],
#          ['Address:' + student_addtional_info.Address,'',''],
          ['School attendance:','',''],
          ['Principal Signature','','']]
    t=Table(data,style=[('SPAN',(0,0),(-1,0)),('SPAN',(1,0),(1,-1))])
    Story.append(t)
    Story.append(PageBreak())

def fillAcademicReport(Story):
    style = styles["Normal"]  
    Story.append(Paragraph("Part 2: Academic Information", style))
    Story.append(Spacer(1,1*inch))
    student_yearly_data = StudentYearlyInformation.objects.get(id=1)
    student_test_data = StudentTestMarks(student_yearly_data)
    test_details = student_test_data.TestMapping.SubjectMaster.Name
    marks_obtained = student_test_data.MarksObtained
    data= [[test_details],[marks_obtained]]
    t=Table(data)
    Story.append(t)
    Story.append(Spacer(1,4*inch))
    Story.append(Paragraph("Class teacher Signature", style))
    Story.append(PageBreak())

def fillCoCurricularReport(Story):
    style = styles["Normal"]
    Story.append(Paragraph("Part 3: CoCurricular Activity Report", style))
    Story.append(Spacer(1,1*inch))
    Story.append(Paragraph("Abhivyakti Report", style))
    Story.append(Spacer(1,1*inch))
    Story.append(Paragraph("Competitive Exams:", style))
    Story.append(Spacer(1,1*inch))
    Story.append(Paragraph("Competitions:", style))
    Story.append(Spacer(1,4*inch))
    Story.append(Paragraph("Incharge Abhivyakti\tIncharge Competition\tIncharge Projects", style))
    Story.append(PageBreak())
  
def fillOutdoorActivityReport(Story):
    style = styles["Normal"]
    Story.append(Paragraph("Part 3: Outdoor Activity Report", style))
    Story.append(Spacer(1,1*inch))
    Story.append(Paragraph("Physical fitness Report", style))
    Story.append(Spacer(1,1*inch))
    Story.append(Paragraph("Dal:", style))
    Story.append(Spacer(1,1*inch))
    Story.append(Paragraph("Dal Attendance:", style))
    Story.append(Spacer(1,1*inch))
    Story.append(Paragraph("Social activities:", style))
    Story.append(Spacer(1,4*inch))
    Story.append(Paragraph("Dal Pratod", style))
    Story.append(PageBreak())

def fillLibraryReport(Story):
    style = styles["Normal"]
    Story.append(Paragraph("Part 2: Library Report", style))
    Story.append(Spacer(1,1*inch))
    data= [['Book1'],
    ['Hindi2'],
    ['Sanskrit Book'],
    ['Marathi lit']]
    Story.append(Table(data))
    Story.append(Spacer(1,4*inch))
    Story.append(Paragraph("Librarian Signature", style))
    Story.append(PageBreak())
