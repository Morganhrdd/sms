# Create your views here.
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponse 
from jp_sms.students.models import TestMapping, StudentTestMarks, StudentYearlyInformation, StudentBasicInfo
from jp_sms.students.models import SubjectMaster, ClassMaster, SubjectMaster, AttendanceMaster
from jp_sms.students.models import StudentAttendance, StudentAdditionalInformation,CoCurricular
from jp_sms.students.models import SocialActivity,PhysicalFitnessInfo,AbhivyaktiVikas,Project,Elocution
from jp_sms.students.models import CompetitiveExam, Competition
from django.template import Context
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,Frame,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
from django.contrib.auth.decorators import login_required
from PIL import Image

PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

Title = "Jnana Prabodhini Prashala"
pageinfo = "School Report"

MONTH_CHOICES = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

GRADE_CHOICES = {
    'O': 'Outstanding',
    'E': 'Excellent',
    'G': 'Good',
    'S': 'Satisfactory',
    'N': 'Needs Improvement',
    'U': 'Unsatisfactory',
    'A': 'No Entry for this category',
    '5': 'Outstanding',
    '4': 'Excellent',
    '3': 'Good',
    '2': 'Satisfactory',
    '1': 'Needs Improvement',
    '0': 'Unsatisfactory',
    '': 'No Entry for this category',
}

GRADE_NUM = {
    'O': 6,
    'E': 5,
    'G': 4,
    'S': 3,
    'N': 2,
    'U': 1,
    'A':0,
    '':0,
    '0':0,
    '1':1,
    '2':2,
    '3':3,
    '4':4,
    '5':5,
    '6':6,
}

GRADE_CHOICE_NUM = ['', 'No Entry for this category','Unsatisfactory','Needs Improvement','Satisfactory','Good','Excellent','Outstanding']

PROJECT_TYPE_CHOICES = {
    'CC': 'Collection, Classification',
    'MM': 'Model Making',
    'IS': 'Investivation by Survey',
    'I': 'Investigation',
    'CP': 'Creative production',
    'AC': 'Appreciation-criticism',
    'O': 'Open ended exploration',
}
def report(request):
    if request.POST:
        keys = request.POST.keys()
        reg_no = request.POST['reg_no']

        student_basic_info = StudentBasicInfo.objects.get(RegistrationNo = reg_no)
        student_yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo = student_basic_info)
        student_add_info = StudentAdditionalInformation.objects.get(Id=student_basic_info)
        student_data={'FirstName':student_basic_info.FirstName,
                      'LastName':student_basic_info.LastName,
                      'DateOfBirth':student_basic_info.DateOfBirth,
                      'MothersName':student_basic_info.MothersName,
                      'FathersName':student_basic_info.FathersName,
                      'RegistrationNo':student_basic_info.RegistrationNo,
                      'Address':student_add_info.Address,
                      'photo':student_yearly_info.Photo}

        attendances = StudentAttendance.objects.filter(StudentYearlyInformation = student_yearly_info)
        attendance_data = []
        for attendance in attendances:
            attendance_data.append({'Month':MONTH_CHOICES[attendance.AttendanceMaster.Month] ,
                                    'Attendance':attendance.ActualAttendance ,
                                    'Working_days':attendance.AttendanceMaster.WorkingDays})
     
##        marks = StudentTestMarks.objects.filter(StudentYearlyInformation=student_yearly_info)
        mark_data = {}
        marks_summary={'TotalMarksObtained':0 , 'TotalMaximumMarks':0}
##        for mark in marks:
##            marks_summary['TotalMarksObtained']+=mark.MarksObtained
##            marks_summary['TotalMaximumMarks']+=mark.TestMapping.MaximumMarks
##            #if marks_summary.has_key[mark.TestMapping.SubjectMaster.Name]:
##             #   marks_summary[mark.TestMapping.SubjectMaster.Name]+=mark.MarksObtained
##            #else:
##             #   marks_summary[mark.TestMapping.SubjectMaster.Name]=0
##            #marks_summary['Subject_Name']+=marks_summary['Subject_Name']
##            subject_marks = {}
##            try:
##                subject_marks[mark.Subject_Name]['obtained'] += mark.MarksObtained
##                subject_marks[mark.Subject_Name]['max_marks'] += mark.MaximumMarks
##            except:
##                subject_marks[mark.Subject_Name]['obtained'] = {}
##                subject_marks[mark.Subject_Name]['max_marks'] = {}
##                subject_marks[mark.Subject_Name]['obtained'] = mark.MarksObtained
##                subject_marks[mark.Subject_Name]['max_marks'] = mark.MaximumMarks
##            if not mark_data.has_key(mark.Subject_Name):
##                mark_data[mark.Subject_Name] = {}
##            if not mark_data[mark.Subject_Name].has_key(mark.TestType):
##                mark_data[mark.Subject_Name][mark.TestType] = {}    
##            mark_data[mark.Subject_Name][mark.TestType]['marks_obtained'] = mark.MarksObtained
##            mark_data[mark.Subject_Name][mark.TestType]['max_marks'] = mark.MaximumMarks

            
##    subjects_data = {}
##    student_test_data = StudentTestMarks.objects.filter(StudentYearlyInformation=student_yearly_info)
##    data = []
##    data.append(['','Subject Name','Test type','Marks','Maximum Marks'])
##    for test_marks in student_test_data:
##        test_mapping = test_marks.TestMapping
##        subject_name = test_mapping.SubjectMaster.Name
##        if not subjects_data.has_key(subject_name):
##            subjects_data[subject_name] = []
##        subject_data = subjects_data[subject_name]
##        subject_data.append(test_marks)
##
##    cummulative_marks=0
##    cummulative_maxmarks=0
##    for subject_item in subjects_data.keys():
##        subject_data = subjects_data[subject_item]
###        addSubHeaderToStory(Story,subject_item);
##        data = []
##        data.append(['','Test Type','Marks','Maximum Marks'])
##        cummulative_subject_marks=0
##        cummulative_subject_maxmarks=0
##        i=0
##        for subject_marks in subject_data:
##            i = i + 1
##            test_mapping = subject_marks.TestMapping
##            subject_name = test_mapping.SubjectMaster.Name
##            test_type = test_mapping.TestType
##            maximum_marks = test_mapping.MaximumMarks
##            marks_obtained = subject_marks.MarksObtained 
##            data.append([i,test_type,marks_obtained,maximum_marks])
##            cummulative_subject_marks = cummulative_subject_marks + marks_obtained
##            cummulative_subject_maxmarks = cummulative_subject_maxmarks + maximum_marks
##        data.append(['','Subject Total :',cummulative_subject_marks,cummulative_subject_maxmarks])
##        cummulative_marks = cummulative_marks + cummulative_subject_marks
##        cummulative_maxmarks = cummulative_maxmarks + cummulative_subject_maxmarks
    
        co_curricular = CoCurricular.objects.filter(StudentYearlyInformation = student_yearly_info)
        co_curricular_data = []
        cumulative_cocur_grade_sum=0
        cumulative_cocur_grade=0
        for co_cur_acts in co_curricular:
            cumulative_cocur_grade_sum=cumulative_cocur_grade_sum + GRADE_NUM[co_cur_acts.Grade]
            co_curricular_data.append({'Activity':co_cur_acts.Activity ,
                                       'Objectives':co_cur_acts.Objectives ,
                                       'Date':co_cur_acts.Date ,
                                       'Guide':co_cur_acts.Guide ,
                                       'Grade':co_cur_acts.Grade ,
                                       'PublicComment':co_cur_acts.PublicComment})
        if len(co_curricular)>0:
            cumulative_cocur_grade=GRADE_CHOICE_NUM[int(round(cumulative_cocur_grade_sum/len(co_curricular)))]        
        print cumulative_cocur_grade

        competitive_exam = CompetitiveExam.objects.filter(StudentYearlyInformation = student_yearly_info)
        competitive_exam_data = []
        cumulative_compexam_grade_sum=0
        cumulative_compexam_grade=0
        for exams in competitive_exam:
            cumulative_compexam_grade_sum=cumulative_compexam_grade_sum + GRADE_NUM[exams.Grade]
            competitive_exam_data.append({'Name':exams.Name ,
                                          'Subject':exams.Subject ,
                                          'Level':exams.Level ,
                                          'Date':exams.Date ,
                                          'Grade':GRADE_CHOICES[exams.Grade] ,
                                          'PublicComment':exams.PublicComment})
        if len(competitive_exam)>0:
            cumulative_compexam_grade=GRADE_CHOICE_NUM[int(round(cumulative_compexam_grade_sum/len(competitive_exam)))]        
        print cumulative_compexam_grade

        competitions = Competition.objects.filter(StudentYearlyInformation = student_yearly_info)
        competitions_data = []
        cumulative_comp_grade_sum=0
        cumulative_comp_grade=0
        for comps in competitions:
            cumulative_comp_grade_sum=0 #cumulative_comp_grade_sum + GRADE_NUM[comps.Achievement]
            competitions_data.append({'Organizer':comps.Organizer ,
                                          'Subject':comps.Subject ,
                                          'Date':comps.Date ,
                                          'Achievement':comps.Achievement,
                                          'Guide':comps.Guide ,
                                          'PublicComment':comps.PublicComment})
        if len(competitions)>0:
            cumulative_comp_grade=GRADE_CHOICE_NUM[int(round(cumulative_comp_grade_sum/len(competitions)))]        
        print cumulative_comp_grade
        
        abhivyakti_vikas = AbhivyaktiVikas.objects.filter(StudentYearlyInformation = student_yearly_info)
        abhivyakti_vikas_data = []
        cumulative_abhi_grade_sum=0
        cumulative_abhi_grade=0
        for abhi_row in abhivyakti_vikas:
            print abhi_row.MediumOfExpression
            abhi_grade_row_sum=int(GRADE_NUM[abhi_row.Participation])+int(GRADE_NUM[abhi_row.ReadinessToLearn])+int(GRADE_NUM[abhi_row.ContinuityInWork])+int(GRADE_NUM[abhi_row.SkillDevelopment])+int(GRADE_NUM[abhi_row.Creativity])
            cumulative_abhi_grade_sum=cumulative_abhi_grade_sum+(int(abhi_grade_row_sum/5))
            abhivyakti_vikas_data.append({'MediumOfExpression':abhi_row.MediumOfExpression ,
                                         'Teacher':abhi_row.Teacher ,
                                         'Participation':GRADE_CHOICES[abhi_row.Participation] ,
                                         'ReadinessToLearn':GRADE_CHOICES[abhi_row.ReadinessToLearn] ,
                                         'ContinuityInWork':GRADE_CHOICES[abhi_row.ContinuityInWork] ,
                                         'SkillDevelopment':GRADE_CHOICES[abhi_row.SkillDevelopment],
                                         'Creativity':GRADE_CHOICES[abhi_row.Creativity],
                                         'PublicComment':abhi_row.PublicComment})
        if(len(abhivyakti_vikas) > 0):
            cumulative_abhi_grade=GRADE_CHOICE_NUM[int(round(cumulative_abhi_grade_sum/len(abhivyakti_vikas)))]
        print cumulative_abhi_grade


        projects = Project.objects.filter(StudentYearlyInformation = student_yearly_info)
        project_data = []
        cumulative_project_grade_sum=0
        cumulative_project_grade=0
        for proj_row in projects:
            print proj_row.Title
            proj_grade_row_sum=int(GRADE_NUM[proj_row.ProblemSelection])+int(GRADE_NUM[proj_row.Review])+int(GRADE_NUM[proj_row.Planning])+int(GRADE_NUM[proj_row.Documentation])+int(GRADE_NUM[proj_row.Communication])
            cumulative_project_grade_sum=cumulative_project_grade_sum+(int(proj_grade_row_sum/5))
            project_data.append({'Title':proj_row.Title ,
                                         'Type':PROJECT_TYPE_CHOICES[proj_row.Type] ,
                                         'Subject':proj_row.Subject ,
                                         'ProblemSelection':GRADE_CHOICES[proj_row.ProblemSelection] ,
                                         'Review':GRADE_CHOICES[proj_row.Review] ,
                                         'Planning':GRADE_CHOICES[proj_row.Planning],
                                         'Documentation':GRADE_CHOICES[proj_row.Documentation],
                                         'Communication':GRADE_CHOICES[proj_row.Communication],
                                         'PublicComment':proj_row.PublicComment})
        if(len(projects) > 0):
            cumulative_project_grade=GRADE_CHOICE_NUM[int(round(cumulative_project_grade_sum/len(projects)))]
        print cumulative_project_grade


        elocution = Elocution.objects.filter(StudentYearlyInformation = student_yearly_info)
        elocution_data = []
        cumulative_elocution_grade_sum=0
        cumulative_elocution_grade=0
        for elo_row in elocution:
            print 'ELOC'
            print elo_row.Title
            print elo_row.Memory
            print elo_row.Content
            elocution_grade_row_sum=int(GRADE_NUM[elo_row.Memory])+int(GRADE_NUM[elo_row.Content])+int(GRADE_NUM[elo_row.Understanding])+int(GRADE_NUM[elo_row.Skill])+int(GRADE_NUM[elo_row.Presentation])
            cumulative_elocution_grade_sum=cumulative_elocution_grade_sum+(int(elocution_grade_row_sum/5))
            elocution_data.append({'Title':elo_row.Title ,
                                         'Memory':GRADE_CHOICES[elo_row.Memory] ,
                                         'Content':GRADE_CHOICES[elo_row.Content] ,
                                         'Understanding':GRADE_CHOICES[elo_row.Understanding] ,
                                         'Skill':GRADE_CHOICES[elo_row.Skill] ,
                                         'Presentation':GRADE_CHOICES[elo_row.Presentation],
                                         'PublicComment':elo_row.PublicComment})
        if(len(elocution) > 0):
            cumulative_elocution_grade=GRADE_CHOICE_NUM[int(round(cumulative_elocution_grade_sum/len(elocution)))]
        print cumulative_elocution_grade

        physical_fit_info = PhysicalFitnessInfo.objects.filter(StudentYearlyInformation = student_yearly_info)
        physical_fit_info_data = []
        cumulative_physical_grade_sum=0
        cumulative_physical_grade=0
        for ph_data in physical_fit_info:
            cumulative_physical_grade_sum=cumulative_physical_grade_sum + GRADE_NUM[ph_data.Grade]
            physical_fit_info_data.append({'Pathak':ph_data.Pathak ,
                                           'Pratod':ph_data.Pratod ,
                                           'Margadarshak':ph_data.Margadarshak ,
                                           'SpecialSport':ph_data.SpecialSport ,                                       
                                           'Weight':ph_data.Weight ,
                                           'Height':ph_data.Height ,
                                           'FlexibleForwardBending':ph_data.FlexibleForwardBending ,
                                           'FlexibleBackwardBending':ph_data.FlexibleBackwardBending ,
                                           'SBJ':ph_data.SBJ ,
                                           'VerticleJump':ph_data.VerticleJump ,
                                           'BallThrow':ph_data.BallThrow ,
                                           'ShuttleRun':ph_data.ShuttleRun ,
                                           'SitUps':ph_data.SitUps ,
                                           'Sprint':ph_data.Sprint ,
                                           'Running400m':ph_data.Running400m ,
                                           'ShortPutThrow':ph_data.ShortPutThrow ,
                                           'BodyMassIndex':ph_data.BodyMassIndex ,
                                           'Balancing':ph_data.Balancing ,
                                           'Grade':ph_data.Grade ,
                                           'PublicComment':ph_data.PublicComment})
        if(len(physical_fit_info) > 0):
            cumulative_physical_grade=GRADE_CHOICE_NUM[int(round(cumulative_physical_grade_sum/len(physical_fit_info)))]        
        print cumulative_physical_grade

        social_activities = SocialActivity.objects.filter(StudentYearlyInformation = student_yearly_info)
        social_activity_data = []
        cumulative_social_grade_sum=0
        cumulative_social_grade=0
        for soc_act_data in social_activities:
            cumulative_social_grade_sum=cumulative_social_grade_sum + GRADE_NUM[soc_act_data.Grade]
            social_activity_data.append({'Activity':soc_act_data.Activity ,
                                         'Objectives':soc_act_data.Objectives ,
                                         'Date':soc_act_data.Date ,
                                         'Organizer':soc_act_data.Organizer ,
                                         'Grade':soc_act_data.Grade ,
                                         'PublicComment':soc_act_data.PublicComment})
        if(len(social_activities) > 0):
            cumulative_social_grade=GRADE_CHOICE_NUM[int(round(cumulative_social_grade_sum/len(social_activities)))]        
        print cumulative_social_grade

        
        return render_to_response('students/Marks_Report.html',Context({'student_data':student_data ,
        'mark_data':mark_data ,
        'marks_summary':marks_summary,
        'attendance_data':attendance_data ,
        'co_curricular_data':co_curricular_data,
        'cumulative_cocur_grade':cumulative_cocur_grade,                                                       
        'abhivyakti_vikas_data':abhivyakti_vikas_data ,
        'cumulative_abhi_grade': cumulative_abhi_grade,
        'project_data':project_data ,
        'cumulative_project_grade':cumulative_project_grade,
        'elocution_data':elocution_data,
        'cumulative_elocution_grade': cumulative_elocution_grade,
        'physical_fit_info_data':physical_fit_info_data,
        'cumulative_physical_grade':cumulative_physical_grade,                                                         
        'social_activity_data':social_activity_data,
        'cumulative_social_grade':cumulative_social_grade}))
    else:
        return HttpResponse ('<html><body>Enter Registration Number<form action="" method="POST"><input type="text" name="reg_no" value="" id="reg_no" size="20"></td>	<input type="submit" value="Enter" /></form></body></html>')




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
        return render_to_response('students/AddMarks.html',Context({'test_details': test_details,'test_id':test_id, 'data':data}))


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
        return render_to_response('students/AddAttendance.html',Context({'attendance_id':attendance_id, 'attendance_details':attendance.ClassMaster, 'data':data}))
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


marks_add = login_required(marks_add)
report=login_required(report)
