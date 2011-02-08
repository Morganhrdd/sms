#!/home/prabodhini/opt/bin/python
import os, sys, datetime, re
from pprint import pprint
from reportlab.lib import colors
os.environ['DJANGO_SETTINGS_MODULE'] = 'sms.settings'
if 'DATAPY' in os.environ:
    sys.path.append(os.environ['DATAPY'])
else:
    sys.path.append('changeme')
from sms.students.models import *

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle,Frame,PageBreak, CondPageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from pprint import pprint

division = dict()
division['B'] = 'B'
division['G'] = 'A'
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

def get_grade(marks):
    if type(marks) not in [int, float]:
        return '-'
    if marks >= 91:
        return 'A1'
    if 81 <= marks <= 90:
        return 'A'
    if 71 <= marks <= 80:
        return 'B1'
    if 61 <= marks <= 70:
        return 'B2'
    if 51 <= marks <= 60:
        return 'C1'
    if 41 <= marks <= 50:
        return 'C2'
    if 33 <= marks <= 40:
        return 'D'
    if 21 <= marks <= 32:
        return 'E1'
    return 'E2'

var1 = '9' #std
var2 = sys.argv[2] # div
yr = sys.argv[3] # year
doc = SimpleDocTemplate("/tmp/"+var1+'_'+division[var2]+'_'+yr+".pdf",pagesize=A4,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
story = []



for student in StudentYearlyInformation.objects.filter(ClassMaster__Standard = var1, ClassMaster__Division = var2, ClassMaster__AcademicYear__Year=yr):
    '''
    try:
        student = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno)
    except:
        continue
    if student.ClassMaster.Standard != 9:
        continue
    '''
    print 'Regno', student.StudentBasicInfo.RegistrationNo

    style = ParagraphStyle(name='styleName', fontName ='Times-Bold', fontSize = 14, alignment=TA_CENTER)
    story.append(Paragraph("Jnana Prabodhini", style))
    story.append(Spacer(1,0.05*inch))
    story.append(Paragraph("Bal Vikas Mandir Prashala", style))
    story.append(Spacer(1,0.05*inch))
    style = ParagraphStyle(name='styleName', fontName ='Times-Bold', fontSize = 10, alignment=TA_CENTER)
    story.append(Paragraph('156/D, Railway Lines, Solapur', style))
    story.append(Spacer(1,0.05*inch))
    
    style = ParagraphStyle(name='styleName', fontName ='Times-Roman', fontSize = 12, alignment=TA_CENTER)
    story.append(Paragraph('Certificate of School Based Continuous Cumulative Evaluation',style))
    story.append(Spacer(1,0.05*inch))
    story.append(Paragraph('SEMISTER I Year 2010-2011',style))
    story.append(Spacer(1,0.1*inch))

    style = ParagraphStyle(name='styleName', fontName ='Times-Roman', fontSize = 10)
    story.append(Paragraph('<bold>Full Name<bold>: '+student.StudentBasicInfo.FirstName+' '+student.StudentBasicInfo.LastName, style))
    
    story.append(Paragraph('Stdandard/Division: '+str(student.ClassMaster.Standard)+' / '+division[student.ClassMaster.Division], style))
    story.append(Paragraph('Roll Number: '+str(student.RollNo), style))

    style = ParagraphStyle(name='styleName', fontName ='Times-Bold', fontSize = 12)
    story.append(Paragraph('Part 1: Academic Performance', style))
    style = ParagraphStyle(name='styleName', fontName ='Times-Roman', fontSize = 10)


    marks = StudentTestMarks.objects.filter(StudentYearlyInformation=student)

    marks_dict = dict()
    for mark in marks:
        if not mark.TestMapping.SubjectMaster.Name in marks_dict:
            marks_dict[mark.TestMapping.SubjectMaster.Name] = dict()
        marks_dict[mark.TestMapping.SubjectMaster.Name][mark.TestMapping.TestType] = [mark.MarksObtained, mark.TestMapping.MaximumMarks]
        #story.append(Paragraph(mark.TestMapping.SubjectMaster.Name+' --- '+mark.TestMapping.TestType+' === '+str(mark.MarksObtained), style))
    print marks_dict
    marks_data = []
    marks_data.append(['', 'Marks', ''])
    grand_total = ['Total', 0, '810.0']
    for subject in ['Marathi', 'Sanskrit', 'English', 'Science', 'Mathematics', 'Social Science', 'Environmental Science', 'Physical Education', 'Personality Development']:
        tmp = []
        total = 0
        if subject not in marks_dict.keys():
            marks_data.append([subject, '-', '-'])
            continue
        tmp.append(subject)
        x = 'SE 1'
        if x in marks_dict[subject]:
            try:
                tmp.append(marks_dict[subject][x][0])
                tmp.append(marks_dict[subject][x][1])
                grand_total[1] += marks_dict[subject][x][0]
            except:
                tmp.append('Data not available')
                tmp.append('')
        else:
            tmp.append('')
            tmp.append('')
        marks_data.append(tmp)
    marks_data.append(grand_total)
    percent = round(grand_total[1] / 8.1, 2)
    #marks_data.append(['', '', '', '', '', ])
    for subject in ['Work Experience']:
        tmp = []
        total = 0
        tmp.append(subject)
        try:
            tmp.append(marks_dict[subject]['SE 1'][0])
            tmp.append(marks_dict[subject]['SE 1'][1])
        except:
            tmp.append('Data not available')
        marks_data.append(tmp)
    marks_data.append(['%', percent, '100'])
    pprint(marks_dict)
    pprint(marks_data)
    t=Table(marks_data, style=[
        ('GRID', (0,0), (-1,-1), 0.25, colors.black ), 
        ('FONT', (0,0), (-1,0), 'Times-Bold'),
        ('FONT', (0,0), (0,-1), 'Times-Bold'),
    ])
    story.append(t)



    story.append(Spacer(1,0.05*inch))
    style = ParagraphStyle(name='styleName', fontName ='Times-Bold', fontSize = 12)
    story.append(Paragraph('Part II: School Attendance', style))
    story.append(Spacer(1,0.05*inch))
    style = ParagraphStyle(name='styleName', fontName ='Times-Bold', fontSize = 10)
    attendance_data = []
    attendance_data.append(['', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'])
    attendance_objs = StudentAttendance.objects.filter(StudentYearlyInformation=student)
    t1 = ['Attendance', '', '', '', '', '']
    t2 = ['Working Days', '', '', '', '', '']
    for a in attendance_objs:
        t1[a.AttendanceMaster.Month - 5] =  a.ActualAttendance
        t2[a.AttendanceMaster.Month - 5] =  a.AttendanceMaster.WorkingDays
    attendance_data.append(t1)
    attendance_data.append(t2)
    t=Table(attendance_data, style=[
        ('GRID', (0,0), (-1,-1), 0.25, colors.black ), 
        ('FONT', (0,0), (-1,0), 'Times-Bold'),
        ('FONT', (0,0), (0,-1), 'Times-Bold'),
    ])
    story.append(t)


    story.append(Spacer(1,0.05*inch))
    style = ParagraphStyle(name='styleName', fontName ='Times-Bold', fontSize = 12)
    story.append(Paragraph('Part III : Remarks',style))
    story.append(Spacer(1,0.05*inch))
    for x in range(4):
        story.append(Spacer(1,0.3*inch))
        story.append(Paragraph('--------------------------------------------------------------------------------------', style))

    story.append(Spacer(1,0.5*inch))

    people_data = [['Class Teacher', 'Supervisor', 'Head master']]
    t=Table(people_data, style = [
        ('FONT', (0,0), (-1, 0), 'Times-Bold', 14),
    ])
    story.append(t)
    story.append(PageBreak())
doc.build(story)
