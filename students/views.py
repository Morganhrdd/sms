# Create your views here.
from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from jp_sms.students.models import *
from django.template import Context, RequestContext
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle,Frame,PageBreak, CondPageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib import colors
import os
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.utils.safestring import mark_safe
import time
import datetime
import string
from pprint import pprint

PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

MONTH_CHOICES = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}

FULLMONTH_CHOICES = {
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
    6: 'Outstanding',
    5: 'Excellent',
    4: 'Good',
    3: 'Satisfactory',
    2: 'Needs Improvement',
    1: 'Unsatisfactory',
    0: '-',
    '': '-',
    '6': 'Outstanding',
    '5': 'Excellent',
    '4': 'Good',
    '3': 'Satisfactory',
    '2': 'Needs Improvement',
    '1': 'Unsatisfactory',
    '0': '-',
    '6.0': 'Outstanding',
    '5.0': 'Excellent',
    '4.0': 'Good',
    '3.0': 'Satisfactory',
    '2.0': 'Needs Improvement',
    '1.0': 'Unsatisfactory',
    '0.0': '-'
}
    
GRADE_CHOICES_3 = {
    '0': 'None',
    '1': 'Satisfactory',
    '2': 'Good',
    '3': 'Outstanding',
     0 : 'None',
     1 : 'Satisfactory',
     2 : 'Good',
     3 : 'Outstanding',
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
    '6.0':6,
    '5.0':5,
    '4.0':4,
    '3.0':3,
    '2.0':2,
    '1.0':1,
    '0.0':0
}

PROJECT_TYPE_CHOICES = {
    'CC': 'Collection, Classification',
    'MM': 'Model Making',
    'IS': 'Investivation by Survey',
    'I': 'Investigation',
    'CP': 'Creative production',
    'AC': 'Appreciation-criticism',
    'O': 'Open ended exploration',
}

DIVISION_NUM = {
    'B': 1,
    'G': 2
}

ones = ["", "One ","Two ","Three ","Four ", "Five ", "Six ","Seven ","Eight ","Nine "]

tens = ["Ten ","Eleven ","Twelve ","Thirteen ", "Fourteen ",
"Fifteen ","Sixteen ","Seventeen ","Eighteen ","Nineteen "]

twenties = ["","","Twenty ","Thirty ","Forty ", "Fifty ","Sixty ","Seventy ","Eighty ","Ninety "]

thousands = ["","Thousand ","Million ", "Billion ", "Trillion "]


class generate_report(object):
    def __init__(self, regno=None, year=None, classmaster_type='P'):
        self.regno = regno
        self.year = year
        self.classmaster_type = classmaster_type
        self.data = {}
    def generate_data(self):
        student_basic_info_obj = StudentBasicInfo.objects.get(RegistrationNo=self.regno)
        year = AcademicYear.objects.get(Year=self.year)
        try:
            student_addtional_info = StudentAdditionalInformation.objects.get(Id=student_basic_info_obj)
        except:
            student_addtional_info = StudentAdditionalInformation()
        student_yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo=student_basic_info_obj, ClassMaster__AcademicYear=year, ClassMaster__Type=self.classmaster_type)
        classmaster = student_yearly_info.ClassMaster
        attendance_objs = StudentAttendance.objects.filter(AttendanceMaster__ClassMaster=classmaster, StudentYearlyInformation=student_yearly_info)
        physical_fitness_info_obj = PhysicalFitnessInfo.objects.filter(StudentYearlyInformation=student_yearly_info)
        test_marks_objs = StudentTestMarks.objects.filter(StudentYearlyInformation=student_yearly_info)
        socialactivity_objs = SocialActivity.objects.filter(StudentYearlyInformation=student_yearly_info)
        cocurricular_objs = CoCurricular.objects.filter(StudentYearlyInformation=student_yearly_info)
        competitiveexam_objs = CompetitiveExam.objects.filter(StudentYearlyInformation=student_yearly_info)
        competition_objs = Competition.objects.filter(StudentYearlyInformation=student_yearly_info)
        abhivyaktivikas_objs = AbhivyaktiVikas.objects.filter(StudentYearlyInformation=student_yearly_info)
        project_objs = Project.objects.filter(StudentYearlyInformation=student_yearly_info)
        elocution_objs = Elocution.objects.filter(StudentYearlyInformation=student_yearly_info)
        library_objs = Library.objects.filter(StudentYearlyInformation=student_yearly_info)
        workexperience_objs = WorkExperience.objects.filter(StudentYearlyInformation=student_yearly_info)
        physicaleducation_objs = PhysicalEducation.objects.filter(StudentYearlyInformation=student_yearly_info)
        thinkingskill_objs = ThinkingSkill.objects.filter(StudentYearlyInformation=student_yearly_info)
        socialskill_objs = SocialSkill.objects.filter(StudentYearlyInformation=student_yearly_info)
        emotionalskill_objs = EmotionalSkill.objects.filter(StudentYearlyInformation=student_yearly_info)
        attitudetowardsschool_objs = AttitudeTowardsSchool.objects.filter(StudentYearlyInformation=student_yearly_info)
        values_objs = Values.objects.filter(StudentYearlyInformation=student_yearly_info)
        self.data['basic_info'] = student_basic_info_obj
        self.data['additional_info'] = student_addtional_info
        self.data['yearly_info'] = student_yearly_info
        self.data['attendance'] = attendance_objs
        self.data['physical_fitness'] = physical_fitness_info_obj
        self.data['test_marks'] = test_marks_objs
        self.data['socialactivity'] = socialactivity_objs
        self.data['cocurricular'] = cocurricular_objs
        self.data['competitiveexam'] = competitiveexam_objs
        self.data['competition'] = competition_objs
        self.data['abhivyaktivikas'] = abhivyaktivikas_objs
        self.data['project'] = project_objs
        self.data['elocution'] = elocution_objs
        self.data['library'] = library_objs
        self.data['workexperience'] = workexperience_objs
        self.data['physicaleducation'] = physicaleducation_objs
        self.data['thinkingskill'] = thinkingskill_objs
        self.data['socialskill'] = socialskill_objs
        self.data['emotionalskill'] = emotionalskill_objs
        self.data['attitudetowardsschool'] = attitudetowardsschool_objs
        self.data['values'] = values_objs
        tmp_data = {}
        tmp_data['workexperience'] = {'nos':['Communication', 'Confidence', 'Involvement'],'strings':['Task','PublicComment']}
        tmp_data['thinkingskill'] = {'nos':['Inquiry', 'LogicalThinking', 'Creativity', 'DecisionMakingAndProblemSolving'], 'strings':['PublicComment']}
        tmp_data['socialskill'] = {'nos':['Communication', 'InterPersonal', 'TeamWork'], 'strings':['PublicComment']}
        tmp_data['emotionalskill'] = {'nos':['Empathy', 'Expression', 'Management'], 'strings':['PublicComment']}
        tmp_data['attitudetowardsschool'] = {'nos':['SchoolTeachers', 'SchoolMates', 'SchoolPrograms', 'SchoolEnvironment'], 'strings':['PublicComment']}
        tmp_data['values'] = {'nos':['Obedience', 'Honesty', 'Equality', 'Responsibility'],'strings':['PublicComment']}
        self.find_avg(tmp_data)
        #find_avg({'values':{'nos':['Obedience', 'Honesty', 'Equality', 'Responsibility'],'strings':['PublicComment']}})
    #
    def find_avg(self, data):
        for k in data.keys():
            retval = {}
            t = self.data[k]
            for x in data[k]['nos']:
                retval[x] = 0
            for x in data[k]['strings']:
                retval[x] = ''
            for x in t:
                for y in data[k]['nos']:
                    retval[y] += int(getattr(x,y))
                for y in data[k]['strings']:
                    retval[y] += getattr(x,y)
            for x in data[k]['nos']:
                retval[x] /= len(t)
                retval[x] = round(retval[x])
            self.data[k] = [retval]
# HTML Report:
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

        mark_data = {}
        marks_summary={'TotalMarksObtained':0 , 'TotalMaximumMarks':0}

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
            cumulative_cocur_grade=GRADE_CHOICES[int(round(cumulative_cocur_grade_sum/len(co_curricular)))]

        competitive_exam = CompetitiveExam.objects.filter(StudentYearlyInformation = student_yearly_info)
        competitive_exam_data = []
        cumulative_compexam_grade_sum=0
        cumulative_compexam_grade=0
        for exams in competitive_exam:
            #cumulative_compexam_grade_sum=cumulative_compexam_grade_sum + GRADE_NUM[exams.Grade]
            competitive_exam_data.append({'Name':exams.Name ,
                                          'Subject':exams.Subject,
                                          'Level':exams.Level,
                                          'Date':exams.Date,
                                          'Grade':exams.Grade,
                                          'PublicComment':exams.PublicComment})
        if len(competitive_exam)>0:
            cumulative_compexam_grade=GRADE_CHOICES[int(round(cumulative_compexam_grade_sum/len(competitive_exam)))]

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
            cumulative_comp_grade=GRADE_CHOICES[int(round(cumulative_comp_grade_sum/len(competitions)))]

        abhivyakti_vikas = AbhivyaktiVikas.objects.filter(StudentYearlyInformation = student_yearly_info)
        abhivyakti_vikas_data = []
        cumulative_abhi_grade_sum=0
        cumulative_abhi_grade=0
        for abhi_row in abhivyakti_vikas:
            abhi_grade_row_sum=(GRADE_NUM[abhi_row.Participation])+(GRADE_NUM[abhi_row.ReadinessToLearn])+(GRADE_NUM[abhi_row.ContinuityInWork])+(GRADE_NUM[abhi_row.SkillDevelopment])+(GRADE_NUM[abhi_row.Creativity])
            cumulative_abhi_grade_sum=cumulative_abhi_grade_sum+int(round(abhi_grade_row_sum/5))
            abhivyakti_vikas_data.append({'MediumOfExpression':abhi_row.MediumOfExpression ,
                                         'Teacher':abhi_row.Teacher ,
                                         'Participation':GRADE_CHOICES[abhi_row.Participation] ,
                                         'ReadinessToLearn':GRADE_CHOICES[abhi_row.ReadinessToLearn] ,
                                         'ContinuityInWork':GRADE_CHOICES[abhi_row.ContinuityInWork] ,
                                         'SkillDevelopment':GRADE_CHOICES[abhi_row.SkillDevelopment],
                                         'Creativity':GRADE_CHOICES[abhi_row.Creativity],
                                         'PublicComment':abhi_row.PublicComment})
        if(len(abhivyakti_vikas) > 0):
            cumulative_abhi_grade=GRADE_CHOICES[int(round(cumulative_abhi_grade_sum/len(abhivyakti_vikas)))]

        projects = Project.objects.filter(StudentYearlyInformation = student_yearly_info)
        project_data = []
        cumulative_project_grade_sum=0
        cumulative_project_grade=0
        for proj_row in projects:
            proj_grade_row_sum=(GRADE_NUM[proj_row.ProblemSelection])+(GRADE_NUM[proj_row.Review])+(GRADE_NUM[proj_row.Planning])+(GRADE_NUM[proj_row.Documentation])+(GRADE_NUM[proj_row.Communication])
            cumulative_project_grade_sum=cumulative_project_grade_sum+int(round(proj_grade_row_sum/5))
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
            cumulative_project_grade=GRADE_CHOICES[int(round(cumulative_project_grade_sum/len(projects)))]

        elocution = Elocution.objects.filter(StudentYearlyInformation = student_yearly_info)
        elocution_data = []
        cumulative_elocution_grade_sum=0
        cumulative_elocution_grade=0
        for elo_row in elocution:
            elocution_grade_row_sum=(GRADE_NUM[elo_row.Memory])+(GRADE_NUM[elo_row.Content])+(GRADE_NUM[elo_row.Understanding])+(GRADE_NUM[elo_row.Pronunciation])+(GRADE_NUM[elo_row.Presentation])
            cumulative_elocution_grade_sum=cumulative_elocution_grade_sum+int(round(elocution_grade_row_sum/5))
            elocution_data.append({'Title':elo_row.Title ,
                                         'Memory':GRADE_CHOICES[elo_row.Memory] ,
                                         'Content':GRADE_CHOICES[elo_row.Content] ,
                                         'Understanding':GRADE_CHOICES[elo_row.Understanding] ,
                                         'Pronunciation':GRADE_CHOICES[elo_row.Pronunciation] ,
                                         'Presentation':GRADE_CHOICES[elo_row.Presentation],
                                         'PublicComment':elo_row.PublicComment})
        if(len(elocution) > 0):
            cumulative_elocution_grade=GRADE_CHOICES[int(round(cumulative_elocution_grade_sum/len(elocution)))]

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
            cumulative_physical_grade=GRADE_CHOICES[int(round(cumulative_physical_grade_sum/len(physical_fit_info)))]

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
            cumulative_social_grade=GRADE_CHOICES[int(round(cumulative_social_grade_sum/len(social_activities)))]

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
        'cumulative_social_grade':cumulative_social_grade}), context_instance=RequestContext(request))
    else:
        return HttpResponse ('<html><body>Enter Registration Number<form action="" method="POST"><input type="text" name="reg_no" value="" id="reg_no" size="20"></td>	<input type="submit" value="Enter" /></form></body></html>')

# Used by HTML Report
def marks_add(request):
    if request.POST:
        keys = request.POST.keys()
        test_id = request.POST['test_id']
        keys.remove('test_id')
        if request.user.is_superuser or request.user.email == test.Teacher.Email:
            test = TestMapping.objects.get(id=test_id)
            for key in keys:
                student = StudentYearlyInformation.objects.get(id=key)
                a = StudentTestMarks.objects.filter(StudentYearlyInformation=student, TestMapping=test)
                a.delete()
                a = StudentTestMarks()
                a.TestMapping = test
                a.StudentYearlyInformation = student
                a.MarksObtained = request.POST[key]
                a.save()
            return HttpResponse('Successfully added record.<br/>\n<a href="/marks_add">Select test for entering data</a>')
        else:
            return HttpResponse('Permission denied')
    else:
        if not request.GET.has_key('test_id'):
            tests = TestMapping.objects.all()
            test_details = ''
            for test in tests:
                if request.user.is_superuser or request.user.email == test.Teacher.Email:
                    test_details += '<a href="/marks_add/?test_id='+str(test.id)+'">' + '%s --- %s' %(test, test.AcademicYear) + '</a><br />'
            if not test_details:
                return HttpResponse('Nothing to add/modify')
            return HttpResponse(test_details)
        test_id = request.GET['test_id']
        #div = request.GET['div']
        test = TestMapping.objects.get(id=test_id)
        subject = SubjectMaster.objects.get(id=test.SubjectMaster.id)
        data = []
        student_test_marks_objs = StudentTestMarks.objects.filter(TestMapping = test).order_by('StudentYearlyInformation__ClassMaster','StudentYearlyInformation__RollNo')
        if not len(student_test_marks_objs):
            for student in StudentYearlyInformation.objects.filter(ClassMaster__Standard=subject.Standard, ClassMaster__AcademicYear=test.AcademicYear):
                x = StudentTestMarks()
                x.StudentYearlyInformation = student
                x.TestMapping = test
                x.MarksObtained = 0
                x.save()
            student_test_marks_objs = StudentTestMarks.objects.filter(TestMapping = test).order_by('StudentYearlyInformation__ClassMaster','StudentYearlyInformation__RollNo')
        test_details = 'Standard: %s, Subject Name: %s, Academic Year: %s, TestType: %s, Max Marks: %s' % (subject.Standard, subject.Name, test.AcademicYear, test.TestType, test.MaximumMarks)
        for student_test_mark_obj in student_test_marks_objs:
            name = '%s %s' % (student_test_mark_obj.StudentYearlyInformation.StudentBasicInfo.FirstName, student_test_mark_obj.StudentYearlyInformation.StudentBasicInfo.LastName)
            rollno = student_test_mark_obj.StudentYearlyInformation.RollNo
            data.append({'id':student_test_mark_obj.StudentYearlyInformation.id, 'name':name, 'rollno':rollno,'marks_obtained':student_test_mark_obj.MarksObtained})
        return render_to_response('students/AddMarks.html',Context({'test_details': test_details,'test_id':test_id, 'data':data}), context_instance=RequestContext(request))
    


def competition_add(request):
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response('students/AddCompetition.html',{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response('students/AddWorkExperience.html',{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    Competition.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        competition_obj = Competition.objects.get(pk=pk)
                    else:
                        competition_obj = Competition()
                    competition_obj.StudentYearlyInformation = yearly_info
                    competition_obj.Organizer = request.POST['Organizer']
                    competition_obj.Subject = request.POST['Subject']
                    competition_obj.Date = request.POST['Date']
                    competition_obj.Achievement = request.POST['Achievement']
                    competition_obj.Guide = request.POST['Guide']
                    competition_obj.PublicComment = request.POST['PublicComment']
                    competition_obj.PrivateComment = request.POST['PrivateComment']
                    competition_obj.save()
            # end store data
            competition_objs = Competition.objects.filter(StudentYearlyInformation=yearly_info)
            data = []
            for competition_obj in competition_objs:
                tmp = {}
                tmp['pk'] = competition_obj.pk
                tmp['Subject'] = competition_obj.Subject
                tmp['Organizer'] = competition_obj.Organizer
                tmp['Date'] = competition_obj.Date
                tmp['Achievement'] = competition_obj.Achievement
                tmp['Guide'] = competition_obj.Guide
                tmp['PublicComment'] = competition_obj.PublicComment
                tmp['PrivateComment'] = competition_obj.PrivateComment
                x = CompetitionDetailsForm(initial=tmp)
                data.append(x)
            data.append(CompetitionDetailsForm(initial={'Delete':'Y'}))
            return render_to_response('students/AddCompetition.html',{'form':genform, 'data':data, 'name':name, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response('students/AddCompetition.html',{'form':genform}, context_instance=RequestContext(request))


#
def elocution_add(request):
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response('students/AddElocution.html',{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response('students/AddWorkExperience.html',{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    Elocution.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        elocution_obj = Elocution.objects.get(pk=pk)
                    else:
                        elocution_obj = Elocution()
                    elocution_obj.StudentYearlyInformation = yearly_info
                    elocution_obj.Title = request.POST['Title']
                    elocution_obj.Memory = request.POST['Memory'] or '0'
                    elocution_obj.Content = request.POST['Content'] or '0'
                    elocution_obj.Understanding = request.POST['Understanding'] or '0'
                    elocution_obj.Pronunciation = request.POST['Pronunciation'] or '0'
                    elocution_obj.Presentation = request.POST['Presentation'] or '0'
                    elocution_obj.PublicComment = request.POST['PublicComment']
                    elocution_obj.PrivateComment = request.POST['PrivateComment']
                    elocution_obj.save()
            # end store data
            elocution_objs = Elocution.objects.filter(StudentYearlyInformation=yearly_info)
            data = []
            for elocution_obj in elocution_objs:
                tmp = {}
                tmp['pk'] = elocution_obj.pk
                tmp['Title'] = elocution_obj.Title
                tmp['Memory'] = elocution_obj.Memory
                tmp['Content'] = elocution_obj.Content
                tmp['Understanding'] = elocution_obj.Understanding
                tmp['Pronunciation'] = elocution_obj.Pronunciation
                tmp['Presentation'] = elocution_obj.Presentation
                tmp['PublicComment'] = elocution_obj.PublicComment
                tmp['PrivateComment'] = elocution_obj.PrivateComment
                x = ElocutionDetailsForm(initial=tmp)
                data.append(x)
            data.append(ElocutionDetailsForm(initial={'Delete':'Y'}))
            return render_to_response('students/AddElocution.html',{'form':genform, 'data':data, 'name':name, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response('students/AddElocution.html',{'form':genform}, context_instance=RequestContext(request))

#
def project_add(request):
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response('students/AddProject.html',{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response('students/AddWorkExperience.html',{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    Project.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        project_obj = Project.objects.get(pk=pk)
                    else:
                        project_obj = Project()
                    project_obj.StudentYearlyInformation = yearly_info
                    project_obj.Title = request.POST['Title']
                    project_obj.Type = request.POST['Type'] or 'N'
                    project_obj.Subject = request.POST['Subject']
                    project_obj.ProblemSelection = request.POST['ProblemSelection'] or '0'
                    project_obj.Review = request.POST['Review'] or '0'
                    project_obj.Planning = request.POST['Planning'] or '0'
                    project_obj.Documentation = request.POST['Documentation'] or '0'
                    project_obj.ExecutionAndHardWork = request.POST['ExecutionAndHardWork'] or '0'
                    project_obj.Communication = request.POST['Communication'] or '0'
                    project_obj.PublicComment = request.POST['PublicComment']
                    project_obj.PrivateComment = request.POST['PrivateComment']
                    project_obj.save()
            # end store data
            project_objs = Project.objects.filter(StudentYearlyInformation=yearly_info)
            data = []
            for project_obj in project_objs:
                tmp = {}
                tmp['pk'] = project_obj.pk
                tmp['Title'] = project_obj.Title
                tmp['Type'] = project_obj.Type
                tmp['Subject'] = project_obj.Subject
                tmp['ProblemSelection'] = project_obj.ProblemSelection
                tmp['Review'] = project_obj.Review
                tmp['Planning'] = project_obj.Planning
                tmp['Documentation'] = project_obj.Documentation
                tmp['ExecutionAndHardWork'] = project_obj.ExecutionAndHardWork
                tmp['Communication'] = project_obj.Communication
                tmp['PublicComment'] = project_obj.PublicComment
                tmp['PrivateComment'] = project_obj.PrivateComment
                x = ProjectDetailsForm(initial=tmp)
                data.append(x)
            data.append(ProjectDetailsForm(initial={'Delete':'Y'}))
            return render_to_response('students/AddProject.html',{'form':genform, 'data':data, 'name':name, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response('students/AddProject.html',{'form':genform}, context_instance=RequestContext(request))
#
def abhivyaktivikas_add(request):
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response('students/AddAbhivyaktiVikas.html',{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response('students/AddWorkExperience.html',{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    AbhivyaktiVikas.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        abhivyaktivikas_obj = AbhivyaktiVikas.objects.get(pk=pk)
                    else:
                        abhivyaktivikas_obj = AbhivyaktiVikas()
                    abhivyaktivikas_obj.StudentYearlyInformation = yearly_info
                    abhivyaktivikas_obj.MediumOfExpression = request.POST['MediumOfExpression']
                    abhivyaktivikas_obj.Teacher = Teacher.objects.get(Name=request.POST['Teacher'])
                    abhivyaktivikas_obj.Participation = request.POST['Participation']
                    abhivyaktivikas_obj.ReadinessToLearn = request.POST['ReadinessToLearn'] or '0'
                    abhivyaktivikas_obj.ContinuityInWork = request.POST['ContinuityInWork'] or '0'
                    abhivyaktivikas_obj.SkillDevelopment = request.POST['SkillDevelopment'] or '0'
                    abhivyaktivikas_obj.Creativity = request.POST['Creativity'] or '0'
                    abhivyaktivikas_obj.PublicComment = request.POST['PublicComment']
                    abhivyaktivikas_obj.PrivateComment = request.POST['PrivateComment']
                    abhivyaktivikas_obj.save()
            # end store data
            abhivyaktivikas_objs = AbhivyaktiVikas.objects.filter(StudentYearlyInformation=yearly_info)
            data = []
            teacher_objs = Teacher.objects.all()
            for abhivyaktivikas_obj in abhivyaktivikas_objs:
                tmp = {}
                tmp['pk'] = abhivyaktivikas_obj.pk
                tmp['MediumOfExpression'] = abhivyaktivikas_obj.MediumOfExpression
                tmp['Teacher'] = abhivyaktivikas_obj.Teacher
                tmp['Participation'] = abhivyaktivikas_obj.Participation
                tmp['ReadinessToLearn'] = abhivyaktivikas_obj.ReadinessToLearn
                tmp['ContinuityInWork'] = abhivyaktivikas_obj.ContinuityInWork
                tmp['SkillDevelopment'] = abhivyaktivikas_obj.SkillDevelopment
                tmp['Creativity'] = abhivyaktivikas_obj.Creativity
                tmp['PublicComment'] = abhivyaktivikas_obj.PublicComment
                tmp['PrivateComment'] = abhivyaktivikas_obj.PrivateComment
                x = AbhivyaktiVikasDetailsForm(initial=tmp)
                data.append(x)
            data.append(AbhivyaktiVikasDetailsForm(initial={'Delete':'Y'}))
            return render_to_response('students/AddAbhivyaktiVikas.html',{'form':genform, 'data':data, 'name':name, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response('students/AddAbhivyaktiVikas.html',{'form':genform}, context_instance=RequestContext(request))

#
def competitiveexam_add(request):
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response('students/AddCompetitiveExam.html',{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response('students/AddWorkExperience.html',{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    CompetitiveExam.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        competitiveexam_obj = CompetitiveExam.objects.get(pk=pk)
                    else:
                        competitiveexam_obj = CompetitiveExam()
                    competitiveexam_obj.StudentYearlyInformation = yearly_info
                    competitiveexam_obj.Name = request.POST['Name']
                    competitiveexam_obj.Subject = request.POST['Subject']
                    competitiveexam_obj.Level = request.POST['Level']
                    competitiveexam_obj.Date = request.POST['Date']
                    competitiveexam_obj.Grade = request.POST['Grade']
                    competitiveexam_obj.PublicComment = request.POST['PublicComment']
                    competitiveexam_obj.PrivateComment = request.POST['PrivateComment']
                    competitiveexam_obj.save()
            # end store data
            competitiveexam_objs = CompetitiveExam.objects.filter(StudentYearlyInformation=yearly_info)
            data = []
            for competitiveexam_obj in competitiveexam_objs:
                tmp = {}
                tmp['pk'] = competitiveexam_obj.pk
                tmp['Name'] = competitiveexam_obj.Name
                tmp['Subject'] = competitiveexam_obj.Subject
                tmp['Level'] = competitiveexam_obj.Level
                tmp['Date'] = competitiveexam_obj.Date
                tmp['Grade'] = competitiveexam_obj.Grade
                tmp['PublicComment'] = competitiveexam_obj.PublicComment
                tmp['PrivateComment'] = competitiveexam_obj.PrivateComment
                x = CompetitiveExamDetailsForm(initial=tmp)
                data.append(x)
            data.append(CompetitiveExamDetailsForm(initial={'Delete':'Y'}))
            return render_to_response('students/AddCompetitiveExam.html',{'form':genform, 'data':data, 'name':name, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response('students/AddCompetitiveExam.html',{'form':genform}, context_instance=RequestContext(request))

#
def cocurricular_add(request):
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response('students/AddCocurricular.html',{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response('students/AddWorkExperience.html',{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    CoCurricular.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        cocurricular_obj = CoCurricular.objects.get(pk=pk)
                    else:
                        cocurricular_obj = CoCurricular()
                    cocurricular_obj.StudentYearlyInformation = yearly_info
                    cocurricular_obj.Activity = request.POST['Activity']
                    cocurricular_obj.Objectives = request.POST['Objectives']
                    cocurricular_obj.Date = request.POST['Date']
                    cocurricular_obj.Guide = request.POST['Guide']
                    cocurricular_obj.Grade = request.POST['Grade']
                    cocurricular_obj.PublicComment = request.POST['PublicComment']
                    cocurricular_obj.PrivateComment = request.POST['PrivateComment']
                    cocurricular_obj.save()
            # end store data
            cocurricular_objs = CoCurricular.objects.filter(StudentYearlyInformation=yearly_info)
            data = []
            for cocurricular_obj in cocurricular_objs:
                tmp = {}
                tmp['pk'] = cocurricular_obj.pk
                tmp['Activity'] = cocurricular_obj.Activity
                tmp['Objectives'] = cocurricular_obj.Objectives
                tmp['Date'] = cocurricular_obj.Date
                tmp['Guide'] = cocurricular_obj.Guide
                tmp['Grade'] = cocurricular_obj.Grade
                tmp['PublicComment'] = cocurricular_obj.PublicComment
                tmp['PrivateComment'] = cocurricular_obj.PrivateComment
                x = CoCurricularDetailsForm(initial=tmp)
                data.append(x)
            data.append(CoCurricularDetailsForm(initial={'Delete':'Y'}))
            return render_to_response('students/AddCocurricular.html',{'form':genform, 'data':data, 'name':name, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response('students/AddCocurricular.html',{'form':genform}, context_instance=RequestContext(request))

#
def socialactivity_add(request):
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response('students/AddSocialActivity.html',{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response('students/AddWorkExperience.html',{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    SocialActivity.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        socialactivity_obj = SocialActivity.objects.get(pk=pk)
                    else:
                        socialactivity_obj = SocialActivity()
                    socialactivity_obj.StudentYearlyInformation = yearly_info
                    socialactivity_obj.Activity = request.POST['Activity']
                    socialactivity_obj.Objectives = request.POST['Objectives']
                    socialactivity_obj.Date = request.POST['Date']
                    socialactivity_obj.Organizer = request.POST['Organizer']
                    socialactivity_obj.Grade = request.POST['Grade']
                    socialactivity_obj.PublicComment = request.POST['PublicComment']
                    socialactivity_obj.PrivateComment = request.POST['PrivateComment']
                    socialactivity_obj.save()
            # end store data
            socialactivity_objs = SocialActivity.objects.filter(StudentYearlyInformation=yearly_info)
            data = []
            for socialactivity_obj in socialactivity_objs:
                tmp = {}
                tmp['pk'] = socialactivity_obj.pk
                tmp['Activity'] = socialactivity_obj.Activity
                tmp['Objectives'] = socialactivity_obj.Objectives
                tmp['Date'] = socialactivity_obj.Date
                tmp['Organizer'] = socialactivity_obj.Organizer
                tmp['Grade'] = socialactivity_obj.Grade
                tmp['PublicComment'] = socialactivity_obj.PublicComment
                tmp['PrivateComment'] = socialactivity_obj.PrivateComment
                x = SocialActivityDetailsForm(initial=tmp)
                data.append(x)
            data.append(SocialActivityDetailsForm(initial={'Delete':'Y'}))
            return render_to_response('students/AddSocialActivity.html',{'form':genform, 'data':data, 'name':name, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response('students/AddSocialActivity.html',{'form':genform}, context_instance=RequestContext(request))

#
def physicalfitnessinfo_add(request):
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response('students/AddPhysicalFitnessInfo.html',{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response('students/AddWorkExperience.html',{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    PhysicalFitnessInfo.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        physicalfitnessinfo_obj = PhysicalFitnessInfo.objects.get(pk=pk)
                    else:
                        physicalfitnessinfo_obj = PhysicalFitnessInfo()
                    physicalfitnessinfo_obj.StudentYearlyInformation = yearly_info


                    physicalfitnessinfo_obj.Weight = request.POST['Weight']
                    physicalfitnessinfo_obj.Height = request.POST['Height']
                    physicalfitnessinfo_obj.FlexibleForwardBending = request.POST['FlexibleForwardBending']
                    physicalfitnessinfo_obj.FlexibleBackwardBending = request.POST['FlexibleBackwardBending']
                    physicalfitnessinfo_obj.SBJ = request.POST['SBJ']
                    physicalfitnessinfo_obj.VerticleJump = request.POST['VerticleJump']
                    physicalfitnessinfo_obj.BallThrow = request.POST['BallThrow']
                    physicalfitnessinfo_obj.ShuttleRun = request.POST['ShuttleRun']
                    physicalfitnessinfo_obj.SitUps = request.POST['SitUps']
                    physicalfitnessinfo_obj.Sprint = request.POST['Sprint']
                    physicalfitnessinfo_obj.Running400m = request.POST['Running400m']
                    physicalfitnessinfo_obj.ShortPutThrow = request.POST['ShortPutThrow']
                    physicalfitnessinfo_obj.Split = request.POST['Split']
                    physicalfitnessinfo_obj.BodyMassIndex = request.POST['BodyMassIndex']
                    physicalfitnessinfo_obj.Balancing = request.POST['Balancing']
                    physicalfitnessinfo_obj.PublicComment = request.POST['PublicComment']
                    physicalfitnessinfo_obj.PrivateComment = request.POST['PrivateComment']
                    physicalfitnessinfo_obj.Pathak = request.POST['Pathak']
                    physicalfitnessinfo_obj.Pratod = request.POST['Pratod']
                    physicalfitnessinfo_obj.Margadarshak = request.POST['Margadarshak']
                    physicalfitnessinfo_obj.SpecialSport = request.POST['SpecialSport']
                    physicalfitnessinfo_obj.Grade = request.POST['Grade']
                    physicalfitnessinfo_obj.save()
            # end store data
            physicalfitnessinfo_objs = PhysicalFitnessInfo.objects.filter(StudentYearlyInformation=yearly_info)
            data = []
            for physicalfitnessinfo_obj in physicalfitnessinfo_objs:
                tmp = {}
                tmp['pk'] = physicalfitnessinfo_obj.pk
                tmp['Weight'] = physicalfitnessinfo_obj.Weight
                tmp['Height'] = physicalfitnessinfo_obj.Height
                tmp['FlexibleForwardBending'] = physicalfitnessinfo_obj.FlexibleForwardBending
                tmp['FlexibleBackwardBending'] = physicalfitnessinfo_obj.FlexibleBackwardBending
                tmp['SBJ'] = physicalfitnessinfo_obj.SBJ
                tmp['VerticleJump'] = physicalfitnessinfo_obj.VerticleJump
                tmp['BallThrow'] = physicalfitnessinfo_obj.BallThrow
                tmp['ShuttleRun'] = physicalfitnessinfo_obj.ShuttleRun
                tmp['SitUps'] = physicalfitnessinfo_obj.SitUps
                tmp['Sprint'] = physicalfitnessinfo_obj.Sprint
                tmp['Running400m'] = physicalfitnessinfo_obj.Running400m
                tmp['ShortPutThrow'] = physicalfitnessinfo_obj.ShortPutThrow
                tmp['Split'] = physicalfitnessinfo_obj.Split
                tmp['BodyMassIndex'] = physicalfitnessinfo_obj.BodyMassIndex
                tmp['Balancing'] = physicalfitnessinfo_obj.Balancing
                tmp['PublicComment'] = physicalfitnessinfo_obj.PublicComment
                tmp['PrivateComment'] = physicalfitnessinfo_obj.PrivateComment
                tmp['Pathak'] = physicalfitnessinfo_obj.Pathak
                tmp['Pratod'] = physicalfitnessinfo_obj.Pratod
                tmp['Margadarshak'] = physicalfitnessinfo_obj.Margadarshak
                tmp['SpecialSport'] = physicalfitnessinfo_obj.SpecialSport
                tmp['Grade'] = physicalfitnessinfo_obj.Grade
                x = PhysicalFitnessInfoDetailsForm(initial=tmp)
                data.append(x)
            if not len(data):
                data.append(PhysicalFitnessInfoDetailsForm(initial={'Delete':'Y'}))
            return render_to_response('students/AddPhysicalFitnessInfo.html',{'form':genform, 'data':data, 'name':name, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response('students/AddPhysicalFitnessInfo.html',{'form':genform}, context_instance=RequestContext(request))

#
def search_reg_no(request=None):
    if not request:
        return
    if not request.POST['RegistrationNo'] and (request.POST.has_key('FirstName') or request.POST.has_key('LastName')):
        tmp = {}
        if request.POST['FirstName']:
            tmp['FirstName'] = request.POST['FirstName']
        if request.POST['LastName']:
            tmp['LastName'] = request.POST['LastName']
        students_basic_info = StudentBasicInfo.objects.filter(**tmp)
        msg = ''
        for x in students_basic_info:
            msg += '<br /> %s %s %s' % (x.RegistrationNo, x.FirstName, x.LastName)
        msg += '<br />'
        return msg
    
#
def workexperience_add(request):
    respage = 'students/AddWorkExperience.html'
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response(respage,{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    WorkExperience.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        workexperience_obj = WorkExperience.objects.get(pk=pk)
                    else:
                        workexperience_obj = WorkExperience()
                    workexperience_obj.StudentYearlyInformation = yearly_info
                    workexperience_obj.Teacher = Teacher.objects.get(Name=request.POST['Teacher'])
                    workexperience_obj.Task = request.POST['Task']
                    workexperience_obj.Communication = request.POST['Communication'] or '0'
                    workexperience_obj.Confidence = request.POST['Confidence'] or '0'
                    workexperience_obj.Involvement = request.POST['Involvement'] or '0'
                    workexperience_obj.PublicComment = request.POST['PublicComment']
                    workexperience_obj.PrivateComment = request.POST['PrivateComment']
                    workexperience_obj.save()
            # end store data
            workexperience_objs = WorkExperience.objects.filter(StudentYearlyInformation=yearly_info)
            data = []
            teacher_objs = Teacher.objects.all()
            for workexperience_obj in workexperience_objs:
                tmp = {}
                tmp['pk'] = workexperience_obj.pk
                tmp['Teacher'] = workexperience_obj.Teacher
                tmp['Task'] = workexperience_obj.Task
                tmp['Communication'] = workexperience_obj.Communication
                tmp['Confidence'] = workexperience_obj.Confidence
                tmp['Involvement'] = workexperience_obj.Involvement
                tmp['PublicComment'] = workexperience_obj.PublicComment
                tmp['PrivateComment'] = workexperience_obj.PrivateComment
                x = WorkExperienceDetailsForm(initial=tmp)
                data.append(x)
            data.append(WorkExperienceDetailsForm(initial={'Delete':'Y'}))
            return render_to_response(respage,{'form':genform, 'data':data, 'name':name, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))

#
def physicaleducation_add(request):
    respage = 'students/AddPhysicalEducation.html'
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response(respage,{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    PhysicalEducation.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        physicaleducation_obj = PhysicalEducation.objects.get(pk=pk)
                    else:
                        physicaleducation_obj = PhysicalEducation()
                    physicaleducation_obj.StudentYearlyInformation = yearly_info
                    physicaleducation_obj.Name = request.POST['Name']
                    physicaleducation_obj.Pratod = request.POST['Pratod']
                    physicaleducation_obj.AbilityToWorkInTeam = request.POST['AbilityToWorkInTeam'] or '0'
                    physicaleducation_obj.Cooperation = request.POST['Cooperation'] or '0'
                    physicaleducation_obj.LeadershipSkill = request.POST['LeadershipSkill'] or '0'
                    physicaleducation_obj.PublicComment = request.POST['PublicComment']
                    physicaleducation_obj.PrivateComment = request.POST['PrivateComment']
                    physicaleducation_obj.save()
            # end store data
            physicaleducation_objs = PhysicalEducation.objects.filter(StudentYearlyInformation=yearly_info)
            data = []
            teacher_objs = Teacher.objects.all()
            for physicaleducation_obj in physicaleducation_objs:
                tmp = {}
                tmp['pk'] = physicaleducation_obj.pk
                tmp['Name'] = physicaleducation_obj.Name
                tmp['Pratod'] = physicaleducation_obj.Pratod
                tmp['AbilityToWorkInTeam'] = physicaleducation_obj.AbilityToWorkInTeam
                tmp['Cooperation'] = physicaleducation_obj.Cooperation
                tmp['LeadershipSkill'] = physicaleducation_obj.LeadershipSkill
                tmp['PublicComment'] = physicaleducation_obj.PublicComment
                tmp['PrivateComment'] = physicaleducation_obj.PrivateComment
                x = PhysicalEducationDetailsForm(initial=tmp)
                data.append(x)
            if not len(data):
                data.append(PhysicalEducationDetailsForm(initial={'Delete':'Y'}))
            return render_to_response(respage,{'form':genform, 'data':data, 'name':name, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))

#
def thinkingskill_add(request):
    respage = 'students/AddThinkingSkill.html'
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response(respage,{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    ThinkingSkill.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        thinkingskill_obj = ThinkingSkill.objects.get(pk=pk)
                    else:
                        thinkingskill_obj = ThinkingSkill()
                    thinkingskill_obj.StudentYearlyInformation = yearly_info
                    thinkingskill_obj.Teacher = Teacher.objects.get(pk=request.POST['Teacher'])
                    thinkingskill_obj.Inquiry = request.POST['Inquiry'] or '0'
                    thinkingskill_obj.LogicalThinking = request.POST['LogicalThinking'] or '0'
                    thinkingskill_obj.Creativity = request.POST['Creativity'] or '0'
                    thinkingskill_obj.DecisionMakingAndProblemSolving = request.POST['DecisionMakingAndProblemSolving'] or '0'
                    thinkingskill_obj.PublicComment = request.POST['PublicComment']
                    thinkingskill_obj.PrivateComment = request.POST['PrivateComment']
                    thinkingskill_obj.save()
            # end store data
            delete = ''
            # error handling to be done for teacher_obj
            teacher_obj = Teacher.objects.get(Email=request.user.email)
            try:
                thinkingskill_obj = ThinkingSkill.objects.get(StudentYearlyInformation=yearly_info, Teacher=teacher_obj)
            except:
                thinkingskill_obj = ThinkingSkill(StudentYearlyInformation=yearly_info,Teacher=teacher_obj)
                delete = 'Y'
            data = []
            tmp = {}
            tmp['pk'] = thinkingskill_obj.pk
            tmp['Inquiry'] = thinkingskill_obj.Inquiry
            tmp['LogicalThinking'] = thinkingskill_obj.LogicalThinking
            tmp['Creativity'] = thinkingskill_obj.Creativity
            tmp['DecisionMakingAndProblemSolving'] = thinkingskill_obj.DecisionMakingAndProblemSolving
            tmp['PublicComment'] = thinkingskill_obj.PublicComment
            tmp['PrivateComment'] = thinkingskill_obj.PrivateComment
            tmp['Delete'] = delete
            x = ThinkingSkillDetailsForm(initial=tmp)
            data.append(x)
            return render_to_response(respage,{'form':genform, 'data':data, 'name':name, 'teacher':teacher_obj, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))

#
def socialskill_add(request):
    respage = 'students/AddSocialSkill.html'
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response(respage,{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    SocialSkill.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        socialskill_obj = SocialSkill.objects.get(pk=pk)
                    else:
                        socialskill_obj = SocialSkill()
                    socialskill_obj.StudentYearlyInformation = yearly_info
                    socialskill_obj.Teacher = Teacher.objects.get(Name=request.POST['Teacher'])
                    socialskill_obj.Communication = request.POST['Communication'] or '0'
                    socialskill_obj.InterPersonal = request.POST['InterPersonal'] or '0'
                    socialskill_obj.TeamWork = request.POST['TeamWork'] or '0'
                    socialskill_obj.PublicComment = request.POST['PublicComment']
                    socialskill_obj.PrivateComment = request.POST['PrivateComment']
                    socialskill_obj.save()
            # end store data
            delete = ''
            # error handling to be done for teacher_obj
            teacher_obj = Teacher.objects.get(Email=request.user.email)
            try:
                socialskill_obj = SocialSkill.objects.get(StudentYearlyInformation=yearly_info, Teacher=teacher_obj)
            except:
                socialskill_obj = SocialSkill(StudentYearlyInformation=yearly_info, Teacher=teacher_obj)
                delete = 'Y'
            data = []
            tmp = {}
            tmp['pk'] = socialskill_obj.pk
            tmp['Teacher'] = socialskill_obj.Teacher
            tmp['Communication'] = socialskill_obj.Communication
            tmp['InterPersonal'] = socialskill_obj.InterPersonal
            tmp['TeamWork'] = socialskill_obj.TeamWork
            tmp['PublicComment'] = socialskill_obj.PublicComment
            tmp['PrivateComment'] = socialskill_obj.PrivateComment
            tmp['Delete'] = delete
            x = SocialSkillDetailsForm(initial=tmp)
            data.append(x)
            return render_to_response('students/AddSocialSkill.html',{'form':genform, 'data':data, 'name':name, 'teacher':teacher_obj, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response('students/AddSocialSkill.html',{'form':genform}, context_instance=RequestContext(request))

#
def attitudetowardsschool_add(request):
    respage = 'students/AddAttitudeTowardsSchool.html'
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response(respage,{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    AttitudeTowardsSchool.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        attitudetowardsschool_obj = AttitudeTowardsSchool.objects.get(pk=pk)
                    else:
                        attitudetowardsschool_obj = AttitudeTowardsSchool()
                    attitudetowardsschool_obj.StudentYearlyInformation = yearly_info
                    attitudetowardsschool_obj.Teacher = Teacher.objects.get(Name=request.POST['Teacher'])
                    attitudetowardsschool_obj.SchoolTeachers = request.POST['SchoolTeachers'] or '0'
                    attitudetowardsschool_obj.SchoolMates = request.POST['SchoolMates'] or '0'
                    attitudetowardsschool_obj.SchoolPrograms = request.POST['SchoolPrograms'] or '0'
                    attitudetowardsschool_obj.SchoolEnvironment = request.POST['SchoolEnvironment'] or '0'
                    attitudetowardsschool_obj.PublicComment = request.POST['PublicComment']
                    attitudetowardsschool_obj.PrivateComment = request.POST['PrivateComment']
                    attitudetowardsschool_obj.save()
            # end store data
            delete = ''
            # error handling to be done for teacher_obj
            teacher_obj = Teacher.objects.get(Email=request.user.email)
            try:
                attitudetowardsschool_obj = AttitudeTowardsSchool.objects.get(StudentYearlyInformation=yearly_info, Teacher=teacher_obj)
            except:
                attitudetowardsschool_obj = AttitudeTowardsSchool(StudentYearlyInformation=yearly_info, Teacher=teacher_obj)
                delete = 'Y'
            data = []
            tmp = {}
            tmp['pk'] = attitudetowardsschool_obj.pk
            tmp['Teacher'] = attitudetowardsschool_obj.Teacher
            tmp['SchoolTeachers'] = attitudetowardsschool_obj.SchoolTeachers
            tmp['SchoolMates'] = attitudetowardsschool_obj.SchoolMates
            tmp['SchoolPrograms'] = attitudetowardsschool_obj.SchoolPrograms
            tmp['SchoolEnvironment'] = attitudetowardsschool_obj.SchoolEnvironment
            tmp['PublicComment'] = attitudetowardsschool_obj.PublicComment
            tmp['PrivateComment'] = attitudetowardsschool_obj.PrivateComment
            tmp['Delete'] = delete
            x = AttitudeTowardsSchoolDetailsForm(initial=tmp)
            data.append(x)
            return render_to_response(respage,{'form':genform, 'data':data, 'name':name, 'teacher':teacher_obj, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))
#
def emotionalskill_add(request):
    respage = 'students/AddEmotionalSkill.html'
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response(respage,{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    EmotionalSkill.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        emotionalskill_obj = EmotionalSkill.objects.get(pk=pk)
                    else:
                        emotionalskill_obj = EmotionalSkill()
                    emotionalskill_obj.StudentYearlyInformation = yearly_info
                    emotionalskill_obj.Teacher = Teacher.objects.get(Name=request.POST['Teacher'])
                    emotionalskill_obj.Empathy = request.POST['Empathy'] or '0'
                    emotionalskill_obj.Expression = request.POST['Expression'] or '0'
                    emotionalskill_obj.Management = request.POST['Management'] or '0'
                    emotionalskill_obj.PublicComment = request.POST['PublicComment']
                    emotionalskill_obj.PrivateComment = request.POST['PrivateComment']
                    emotionalskill_obj.save()
            # end store data
            delete = ''
            # error handling to be done for teacher_obj
            teacher_obj = Teacher.objects.get(Email=request.user.email)
            try:
                emotionalskill_obj = EmotionalSkill.objects.get(StudentYearlyInformation=yearly_info, Teacher=teacher_obj)
            except:
                emotionalskill_obj = EmotionalSkill(StudentYearlyInformation=yearly_info, Teacher=teacher_obj)
            data = []
            tmp = {}
            tmp['pk'] = emotionalskill_obj.pk
            tmp['Teacher'] = emotionalskill_obj.Teacher
            tmp['Empathy'] = emotionalskill_obj.Empathy
            tmp['Expression'] = emotionalskill_obj.Expression
            tmp['Management'] = emotionalskill_obj.Management
            tmp['PublicComment'] = emotionalskill_obj.PublicComment
            tmp['PrivateComment'] = emotionalskill_obj.PrivateComment
            tmp['Delete'] = delete
            x = EmotionalSkillDetailsForm(initial=tmp)
            data.append(x)
            return render_to_response(respage,{'form':genform, 'data':data, 'name':name, 'teacher':teacher_obj, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))

#
def values_add(request):
    respage = 'students/AddValues.html'
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response(respage,{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    Values.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        values_obj = Values.objects.get(pk=pk)
                    else:
                        values_obj = Values()
                    values_obj.StudentYearlyInformation = yearly_info
                    values_obj.Teacher = Teacher.objects.get(Name=request.POST['Teacher'])
                    values_obj.Obedience = request.POST['Obedience'] or '0'
                    values_obj.Honesty = request.POST['Honesty'] or '0'
                    values_obj.Equality = request.POST['Equality'] or '0'
                    values_obj.Responsibility = request.POST['Responsibility'] or '0'
                    values_obj.PublicComment = request.POST['PublicComment']
                    values_obj.PrivateComment = request.POST['PrivateComment']
                    values_obj.save()
            # end store data
            delete = ''
            # error handling to be done for teacher_obj
            teacher_obj = Teacher.objects.get(Email=request.user.email)
            try:
                values_obj = Values.objects.get(StudentYearlyInformation=yearly_info, Teacher=teacher_obj)
            except:
                values_obj = Values(StudentYearlyInformation=yearly_info, Teacher=teacher_obj)
                delete = 'Y'
            data = []
            tmp = {}
            tmp['pk'] = values_obj.pk
            tmp['Teacher'] = values_obj.Teacher
            tmp['Obedience'] = values_obj.Obedience
            tmp['Honesty'] = values_obj.Honesty
            tmp['Equality'] = values_obj.Equality
            tmp['Responsibility'] = values_obj.Responsibility
            tmp['PublicComment'] = values_obj.PublicComment
            tmp['PrivateComment'] = values_obj.PrivateComment
            tmp['Delete'] = delete
            x = ValuesDetailsForm(initial=tmp)
            data.append(x)
            return render_to_response(respage,{'form':genform, 'data':data, 'name':name, 'teacher':teacher_obj, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))
    

#
def medicalreport_add(request):
    respage = 'students/AddMedicalReport.html'
    if not request.POST:
        genform = SearchDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))
    else:
        genform = SearchDetailsForm(request.POST)
        msg = search_reg_no(request=request)
        if msg:
            return render_to_response(respage,{'form':genform,'msg':msg}, context_instance=RequestContext(request))
        if request.POST.has_key('RegistrationNo'):
            regno = request.POST['RegistrationNo']
            student_info = StudentBasicInfo.objects.get(RegistrationNo=regno)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            yr = request.POST['Year']
            yearly_info = StudentYearlyInformation.objects.get(StudentBasicInfo__RegistrationNo=regno, ClassMaster__AcademicYear__Year=yr)
            # store data
            if request.POST.has_key('pk'):
                pk = request.POST['pk']
                delete = request.POST['Delete']
                if pk and delete in ('Y', 'y'):
                    MedicalReport.objects.get(pk=pk).delete()
                if delete not in ('Y', 'y'):
                    if pk:
                        medicalreport_obj = MedicalReport.objects.get(pk=pk)
                    else:
                        medicalreport_obj = MedicalReport()
                    medicalreport_obj.StudentYearlyInformation = yearly_info
                    medicalreport_obj.Height = request.POST['Height']
                    medicalreport_obj.Weight = request.POST['Weight']
                    medicalreport_obj.BloodGroup = request.POST['BloodGroup'] or '0'
                    medicalreport_obj.VisionL = request.POST['VisionL']
                    medicalreport_obj.VisionR = request.POST['VisionR']
                    medicalreport_obj.Teeth = request.POST['Teeth']
                    medicalreport_obj.OralHygiene = request.POST['OralHygiene']
                    medicalreport_obj.SpecificAilment = request.POST['SpecificAilment']
                    medicalreport_obj.Doctor = request.POST['Doctor']
                    medicalreport_obj.ClinicAddress = request.POST['ClinicAddress']
                    medicalreport_obj.Phone = request.POST['Phone']
                    medicalreport_obj.save()
            # end store data
            medicalreport_objs = MedicalReport.objects.filter(StudentYearlyInformation=yearly_info)
            data = []
            for medicalreport_obj in medicalreport_objs:
                tmp = {}
                tmp['pk'] = medicalreport_obj.pk
                tmp['Height'] = medicalreport_obj.Height
                tmp['Weight'] = medicalreport_obj.Weight
                tmp['BloodGroup'] = medicalreport_obj.BloodGroup
                tmp['VisionL'] = medicalreport_obj.VisionL
                tmp['VisionR'] = medicalreport_obj.VisionR
                tmp['Teeth'] = medicalreport_obj.Teeth
                tmp['OralHygiene'] = medicalreport_obj.OralHygiene
                tmp['SpecificAilment'] = medicalreport_obj.SpecificAilment
                tmp['Doctor'] = medicalreport_obj.Doctor
                tmp['ClinicAddress'] = medicalreport_obj.ClinicAddress
                tmp['Phone'] = medicalreport_obj.Phone
                x = MedicalReportForm(initial=tmp)
                data.append(x)
            if not len(data):
                data.append(MedicalReportForm(initial={'Delete':'Y'}))
            return render_to_response(respage,{'form':genform, 'data':data, 'name':name, 'photo':'/media/students_photos/'+yearly_info.ClassMaster.AcademicYear.Year+'_'+regno+'.jpg'}, context_instance=RequestContext(request))
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))


#
def generate_name_columns(request):
    respage = 'students/GenerateNameColumns.html'
    if not request.POST:
        genform = SearchClassDetailsForm(initial={'Year':'2009-2010'})
        return render_to_response(respage,{'form':genform}, context_instance=RequestContext(request))
    else:
        table_style = TableStyle([
               ('FONT', (0,0), (-1,0), 'Times-Bold'),
               ('HALIGN',(0,0),(-1,-1), 'LEFT'),
               ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
               ('FONTSIZE',(0,0),(-1,-1),12),
               ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
               ('INNERGRID', (0,0), (-1,-1), 0.20, colors.gray),
               ('BOX', (0,0), (-1,-1), 0.20, colors.gray)])
        tmp = []
        data = []
        dl = []
        dl.append(1.5*cm)
        dl.append(1.75*cm)
        dl.append(2*inch)
        cols = int(request.POST['Columns'])
        col_width = (defaultPageSize[0]-(5*inch))/cols
        height = defaultPageSize[1]
        yr = request.POST['Year']
        std = request.POST['Standard']
        div = request.POST['Division']
        for i in range(cols):
            tmp.append('')
            dl.append(col_width)
        data.append(['RegNo', 'RollNo', 'Name']+tmp)
        s_objs = StudentYearlyInformation.objects.filter(ClassMaster__AcademicYear__Year=yr,ClassMaster__Standard=std,ClassMaster__Division=div).order_by('RollNo')
        for s in s_objs:
            data.append([s.StudentBasicInfo.RegistrationNo, s.RollNo, s.StudentBasicInfo.FirstName+' '+s.StudentBasicInfo.LastName]+tmp)


        #
        PAGE_HEIGHT=defaultPageSize[1]
        PAGE_WIDTH=defaultPageSize[0]
        styles = getSampleStyleSheet()
        pages  = []
        dr=[]
        for i in data:
            dr.append(.55*cm)
        table = Table(data,dl,dr)
        table.setStyle(table_style)
        pages.append(table)
        response = HttpResponse(mimetype='application/pdf')
        doc = SimpleDocTemplate(response)
        doc.build(pages)
        return response


#
def display_report(request, regno=None, year=None):
    if request.user.username != str(regno) and not request.user.is_superuser and request.user.is_active:
        return redirect('/')
    respage = 'students/DisplayReport.html'
    data = generate_report(regno=regno, year=year)
    data.generate_data()
    return render_to_response(respage,data.data, context_instance=RequestContext(request))

# Used by HTML Report
def attendance_add(request):
    if request.POST:
        keys = request.POST.keys()
        attendance_id = request.POST['attendance_id']
        keys.remove('attendance_id')
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
        return HttpResponse('Successfully added record.<br/>\n<a href="/attendance_add">Select test for entering data</a>')
    else:
        if not request.GET.has_key('attendance_id'):
            attendancemaster = AttendanceMaster.objects.all()
            attendance_details = ''
            for attendance in attendancemaster:
                if request.user.is_superuser or request.user.email == attendance.ClassMaster.Teacher.Email:
                    attendance_details += '<a href="/attendance_add/?attendance_id='+str(attendance.id)+'">'+'%s' %(attendance) + '</a><br/>'
            if not attendance_details:
                return HttpResponse('Nothing to add/modify')
            return HttpResponse(attendance_details)
        attendance_id = request.GET['attendance_id']
        attendance_obj = AttendanceMaster.objects.get(id=attendance_id)
        students = StudentYearlyInformation.objects.filter(ClassMaster=attendance_obj.ClassMaster).order_by('RollNo')
        data = []
        for student in students:
            student_info = StudentBasicInfo.objects.get(RegistrationNo = student.StudentBasicInfo.RegistrationNo)
            name = '%s %s' % (student_info.FirstName, student_info.LastName)
            try:
                attendance = StudentAttendance.objects.get(StudentYearlyInformation=student, AttendanceMaster=attendance_obj).ActualAttendance
            except:
                attendance = ''
            data.append({'id':student.id,'roll_no':student.RollNo, 'name':name, 'attendance':attendance})
        return render_to_response('students/AddAttendance.html',Context({'attendance_id':attendance_id, 'attendance_details':attendance_obj.ClassMaster, 'data':data}), context_instance=RequestContext(request))
    return HttpResponse()

# PDF Report :	--------------------------------------------------

def laterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',6)
    now_time = datetime.datetime.now()
    #epoch_seconds = time.mktime(now_time.timetuple())
    epoch_seconds = now_time.strftime("%d %b %Y %I:%M:%S%p")
    #the number at the bottom right of page will let us trace the exact date and time and will never repeat for any documents
    canvas.drawString(0.4 * PAGE_WIDTH, 0.75 * inch, "%s          %s   page %d" % ("Jnana Prabodhini Prashala's Certificate of School Based Evaluation", epoch_seconds, doc.page))
    canvas.restoreState()
    pageBorder(canvas)

def pageBorder(canvas):
    #centrally placed rectangle
    margin=0.7*inch
    canvas.line(margin, margin, margin, PAGE_HEIGHT - margin)
    canvas.line(margin, PAGE_HEIGHT - margin, PAGE_WIDTH - margin, PAGE_HEIGHT - margin)
    canvas.line(PAGE_WIDTH - margin, PAGE_HEIGHT - margin, PAGE_WIDTH - margin, margin)
    canvas.line(PAGE_WIDTH - margin, margin, margin, margin)
    
    #line separator for footer
    canvas.setLineWidth(0.1)
    canvas.line(PAGE_WIDTH - margin, margin + 0.16*inch, margin, margin + 0.16*inch)

#
def reportPDF(request):
    if request.POST:
        keys = request.POST.keys()
        
        #pick values from html form
        registration_number_min = int(request.POST['registration_number_min'])
        registration_number_max = int(request.POST['registration_number_max'])
        part_option = int(request.POST['part_option'])
        standard = int(request.POST['standard'])
        division = request.POST['division']
        year_option = request.POST['year_option']

        #populate a list of egistration numbers for the specified range
        registration_numbers = []
        registration_number = registration_number_min
        while registration_number <= registration_number_max:
            registration_numbers.append(registration_number)
            registration_number = registration_number + 1

        #populate content for the list of reg numbers
        Story = []
        fillPdfData(Story, registration_numbers, part_option, standard, division, year_option)

        #show an unsaved pdf document in the browser, using reportPDF
        response = HttpResponse(mimetype='application/pdf')
        doc = SimpleDocTemplate(response)
        doc.build(Story, onFirstPage=laterPages, onLaterPages=laterPages)
        
        return response
    else:
        return HttpResponse ('<html><body>'
                             + '<P><B><BIG><BIG>Report in PDF format</BIG></BIG></B></P>'
                             + '<form action="" method="POST">'
                             + '<BIG>Registration Numbers: </BIG><input type="text" name="registration_number_min" value="1000" id="registration_number_min" size="5"></td>'
                             + '<BIG> to </BIG><input type="text" name="registration_number_max" value="6000" id="registration_number_max" size="5"><br /><br />'
                             + '<BIG>Type of Report</BIG>: <input type="text" name="part_option" value="0" id="part_option" size="3"><br /><br />'
                             + '<BIG>Standard</BIG>: <input type="text" name="standard" value="0" id="standard" size="3"><br /><br />'
                             + '<BIG>Division </BIG>: <input type="text" name="division" value="-" id="division" size="3"><br /><br />'
                             + 'Year: <input type="text" name="year_option" value="2009-2010" id="year_option" size="10"><br /><br />'
                             + '<input type="submit" value="Enter" />'
                             + '</form>'
                             + '<br /><br />'
                             + 'Type of Report - 0 for All, Part number for respective Part<br />'
                             + 'Standard - 5 to 10 for respective Standard, any other value for All<br />'
                             + 'Division - B for Boys, G for Girls, any other value for for Both<br /><br />'
                             + '<P>An unsaved PDF file will be generated.<br /> It will contain minimum 5 pages per valid registration number.<br /> At bottom-right, the number after letter P is the page number in this PDF document</P>'
                             + '</body></html>')

def fillPdfData(Story, registration_nos, part_option, standard, division, year_option):
    for registration_no in registration_nos:
        try:
            #read basic and yearly info for the list of reg numbers
            student_basic_info = StudentBasicInfo.objects.get(RegistrationNo = registration_no)
            student_yearly_infos = StudentYearlyInformation.objects.filter(StudentBasicInfo = student_basic_info)
            student_addtional_info = StudentAdditionalInformation.objects.get(Id=student_basic_info.RegistrationNo)
        except:
            #skip the reg numbers if basic info is not found
            continue
        
        for student_yearly_info in student_yearly_infos:

            #filter by year
            student_year = student_yearly_info.ClassMaster.AcademicYear.Year
            if student_year != year_option:
                continue

            #filter by standard if a valid entry is available
            student_standard = student_yearly_info.ClassMaster.Standard
            if (standard >= 5) and (standard <= 10) and (student_standard != standard):
                continue

            #filter by division if a valid entry is available
            student_division = student_yearly_info.ClassMaster.Division
            if ((division == 'B') or (division == 'G')) and (student_division != division):
                continue

            #calculate skill grades and populate
            skillsStory = []
            skillGrades = {
                'ThinkingSkill': '-',
                'SocialSkill': '-',
                'EmotionalSkill': '-',
                'AttitudeTowardsSchool': '-',
                'Values': '-'
            }
            fillSkillsReport(student_yearly_info, skillGrades, skillsStory)
            
            #populate content as per the option chosen
            if part_option == 0:
                fillStaticAndYearlyInfo(student_yearly_info, skillGrades, Story)
                fillAcademicReport(student_yearly_info, Story)
                fillCoCurricularReport(student_yearly_info, Story)
                Story += skillsStory
                fillOutdoorActivityReport(student_yearly_info, Story)
                fillLibraryAndMedicalReport(student_yearly_info, Story)
            elif part_option == 1:
                fillStaticAndYearlyInfo(student_yearly_info, skillGrades, Story)
            elif part_option == 2:
                fillAcademicReport(student_yearly_info, Story)
            elif part_option == 3:
                fillCoCurricularReport(student_yearly_info, Story)
            elif part_option == 4:
                Story.append(skillsStory)
            elif part_option == 5:
                fillOutdoorActivityReport(student_yearly_info, Story)
            elif part_option == 6:
                fillLibraryAndMedicalReport(student_yearly_info, Story)

#helper functions for populating content to pdf report
def addTableToStory(Story,data,align):
    table_style = TableStyle([
        ('FONT', (0,0), (-1,0), 'Times-Bold'),
        ('HALIGN',(0,0),(-1,-1), 'LEFT'),
        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
        ('FONTSIZE',(0,0),(-1,-1),9),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
        ('BOX', (0,0), (-1,-1), 0.25, colors.gray)])
    table=Table(data)
    table.setStyle(table_style)
    table.hAlign=align
    Story.append(table)
    Story.append(Spacer(1,0.1*inch))

def addNoBorderTableToStory(Story, data):
    table=Table(data)
    table_style = TableStyle([
        ('FONT', (0,0), (-1,0), 'Times-Roman'),
        ('FONTSIZE',(0,0),(-1,-1),9)])
    table.setStyle(table_style)
    table.hAlign='LEFT'
    Story.append(table)

def formatDate(dateObj):
    return dateObj.strftime("%d %b %Y")

def addMainHeaderToStory(Story,header_text):
    style = ParagraphStyle(name = 'MainHeader', fontSize = 12, alignment=TA_CENTER)
    Story.append(Paragraph("<strong>" + header_text + "</strong>", style))
    Story.append(Spacer(1,0.20*inch))

def addSubHeaderToStory(Story,header_text):
    Story.append(CondPageBreak(1*inch))
    style = ParagraphStyle(name = 'SubHeader', fontSize = 10, alignment=TA_CENTER)
    Story.append(Paragraph("<strong>" + header_text + "</strong>", style))
    Story.append(Spacer(1,0.20*inch))

def addSignatureSpaceToStory(Story,signature_text,designation):
    Story.append(Spacer(1,0.3*inch))
    style = ParagraphStyle(name = 'SignatureStyle', fontSize = 10, alignment=TA_RIGHT)
    Story.append(Paragraph(signature_text, style))
    Story.append(Paragraph(designation, style))

def addNormalTextToStory(Story,normal_text):
    style = ParagraphStyle(name = 'NormalText', fontSize = 9)
    normal_text = normal_text.replace('&','and')
    Story.append(Paragraph(normal_text, style))

def fillLetterHead(Story):
    style = ParagraphStyle(name='styleName', fontName ='Times-Bold', fontSize = 18, alignment=TA_CENTER)
    Story.append(Paragraph("Jnana Prabodhini Prashala", style))

    Story.append(Spacer(1,0.2*inch))

    style = ParagraphStyle(name='styleName', fontName ='Times-Roman', fontSize = 7, alignment=TA_CENTER)
    Story.append(Paragraph("School Affiliation No:1130001", style))
    Story.append(Paragraph("C.B.S.E./A.I./69/(G)/12096/30/4/69", style))

    style = ParagraphStyle(name='styleName', fontName ='Times-Roman', fontSize = 7, alignment=TA_CENTER)
    Story.append(Paragraph("510, Sadashiv Peth, Pune, 411030", style))
    Story.append(Paragraph("email: prashala@jnanaprabodhini.org", style))
    Story.append(Paragraph("http://prashala.jnanaprabodhini.org", style))
    Story.append(Paragraph("Tel: +91 20 24207122", style))

    data = []
    data.append(["Certificate of School Based Evaluation"])
    table_style = TableStyle([
        ('FONT', (0,0), (-1,0), 'Times-Bold'),
        ('ALIGN',(0,0),(-1,-1), 'CENTER'),
        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
        ('FONTSIZE',(0,0),(-1,-1),12),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LINEABOVE',(0,0),(0,0),1,colors.black),
        ('LINEBELOW',(0,0),(0,0),1,colors.black)
        ])
    margin=0.7*inch
    column_widths=((PAGE_WIDTH-2*(margin))*0.9)
    table=Table(data, colWidths=column_widths)
    table.setStyle(table_style)
    table.hAlign = 'CENTER'
    Story.append(table)

    Story.append(Spacer(1,0.1*inch))

def fillStudentAttendance(student_yearly_info, Story, class_type):
    attendances = StudentAttendance.objects.filter(StudentYearlyInformation = student_yearly_info)
    cumulative_attendance=0
    cumulative_workingdays=0

    data = []

    data_row = []
    data_row.append('')
    #start with jun to dec
    for i in range(6, 13):
        data_row.append(MONTH_CHOICES[i])
    #append jan to may
    for i in range(1, 5):
        data_row.append(MONTH_CHOICES[i])
    data_row.append("Total")
    data.append(data_row)

    monthly_attendance = {}
    for i in range(1, 13):
        monthly_attendance[i] = '-'

    monthly_workingdays = {}
    for i in range(1, 13):
        monthly_workingdays[i] = '-'

    #populate attendance for each month and summation
    for attendance in attendances:
        attendance_master = attendance.AttendanceMaster
        class_master = attendance_master.ClassMaster
        #filter as per class type
        if class_master.Type == class_type:
            actual_attendance = attendance.ActualAttendance
            working_days = attendance.AttendanceMaster.WorkingDays
            monthly_attendance[int(attendance.AttendanceMaster.Month)] = actual_attendance
            monthly_workingdays[int(attendance.AttendanceMaster.Month)] = working_days
            cumulative_attendance = cumulative_attendance + actual_attendance
            cumulative_workingdays = cumulative_workingdays + working_days

    data_row = []
    data_row.append('Attendance')
    for i in range(6, 13):
        data_row.append(monthly_attendance[i])
    for i in range(1, 5):
        data_row.append(monthly_attendance[i])
    data_row.append(cumulative_attendance)
    data.append(data_row)

    data_row = []
    data_row.append('Working Days')
    for i in range(6, 13):
        data_row.append(monthly_workingdays[i])
    for i in range(1, 5):
        data_row.append(monthly_workingdays[i])
    data_row.append(cumulative_workingdays)
    data.append(data_row)

    addTableToStory(Story,data,'CENTER')
    Story.append(Spacer(1,0.25*inch))

#first page, letter head, static info and summary
def fillStaticAndYearlyInfo(student_yearly_info, skillGrades, Story):
    student_basic_info = student_yearly_info.StudentBasicInfo

    try:
        student_addtional_info = StudentAdditionalInformation.objects.get(Id=student_basic_info.RegistrationNo)
    except:
        return
    student_yearly_data = student_yearly_info

    fillLetterHead(Story)

    #academic year
    year = student_yearly_data.ClassMaster.AcademicYear.Year
    style = ParagraphStyle(name = 'SubHeader', fontSize = 10, alignment=TA_CENTER)
    Story.append(Paragraph("<strong>" + "Year" + " " + year + "</strong>", style))
    Story.append(Spacer(1,0.05*inch))

    #Part 1 title
    style = ParagraphStyle(name = 'MainHeader', fontSize = 12, alignment=TA_CENTER)
    Story.append(Paragraph("<strong>" + "Part 1: General Information" + "</strong>", style))
    Story.append(Spacer(1,0.05*inch))

    #basic info
    data = []
    data=(
            ['Registration No.: ' , student_basic_info.RegistrationNo,''],
            ['Name: ' , student_basic_info.FirstName + ' ' + student_basic_info.LastName,''],
            ["Father's Name: " , student_basic_info.FathersName,''],
            ["Mother's Name: " , student_basic_info.MothersName,''],
            ['Address: ' , student_addtional_info.Address,''],
            ['Standard: ' , student_yearly_data.ClassMaster.Standard,''],
            ['Roll No.: ' , student_yearly_data.RollNo,''],
        )
    addNoBorderTableToStory(Story, data)

    # cumulative Academics
    marks = StudentTestMarks.objects.filter(StudentYearlyInformation=student_yearly_info)
    cumulative_marks=0
    cumulative_maximum_marks=0
    cumulative_academics='-'
    for mark in marks:
        if mark.MarksObtained > 0:
            cumulative_marks = cumulative_marks + mark.MarksObtained
            cumulative_maximum_marks = cumulative_maximum_marks + mark.TestMapping.MaximumMarks
    if cumulative_maximum_marks > 0:
        cumulative_academics= str(round((cumulative_marks / cumulative_maximum_marks) * 100, 2)) + "%"

    # Cumulative CoCurricular
    co_curricular = CoCurricular.objects.filter(StudentYearlyInformation = student_yearly_info)
    cumulative_cocur_grade_sum=0
    cumulative_cocur_grade='-'
    for co_cur_acts in co_curricular:
        cumulative_cocur_grade_sum=cumulative_cocur_grade_sum + GRADE_NUM[co_cur_acts.Grade]
    if len(co_curricular) > 0:
        cumulative_cocur_grade=GRADE_CHOICES[int(round(cumulative_cocur_grade_sum/len(co_curricular)))]

    # Cumulative Abhivyakti Vikas
    abhivyakti_vikas = AbhivyaktiVikas.objects.filter(StudentYearlyInformation = student_yearly_info)
    cumulative_abhi_grade_sum=0
    cumulative_abhi_grade='-'
    for abhi_row in abhivyakti_vikas:
        abhi_grade_row_sum=(GRADE_NUM[abhi_row.Participation])+(GRADE_NUM[abhi_row.ReadinessToLearn])+(GRADE_NUM[abhi_row.ContinuityInWork])+(GRADE_NUM[abhi_row.SkillDevelopment])+(GRADE_NUM[abhi_row.Creativity])
        cumulative_abhi_grade_sum=cumulative_abhi_grade_sum+int(round((abhi_grade_row_sum/5)))
    if len(abhivyakti_vikas) > 0:
        cumulative_abhi_grade=GRADE_CHOICES[int(round(cumulative_abhi_grade_sum/len(abhivyakti_vikas)))]

    # Cumulative Projects
    projects = Project.objects.filter(StudentYearlyInformation = student_yearly_info)
    cumulative_project_grade_sum=0
    cumulative_project_grade='-'
    for proj_row in projects:
        try:
            proj_grade_row_sum=(GRADE_NUM[proj_row.ProblemSelection])+(GRADE_NUM[proj_row.Review])+(GRADE_NUM[proj_row.Planning])+(GRADE_NUM[proj_row.Documentation])+(GRADE_NUM[proj_row.Communication])
        except:
            proj_grade_row_sum=0
        cumulative_project_grade_sum=cumulative_project_grade_sum+int(round(proj_grade_row_sum/5))
    if len(projects) > 0:
        cumulative_project_grade=GRADE_CHOICES_3[int(round(cumulative_project_grade_sum/len(projects)))]

    # Cumulative Elocution
    elocutions = Elocution.objects.filter(StudentYearlyInformation = student_yearly_info)
    cumulative_elocution_grade_sum=0
    cumulative_elocution_grade='-'
    for elo_row in elocutions:
        elocution_grade_row_sum=(GRADE_NUM[elo_row.Memory])+(GRADE_NUM[elo_row.Content])+(GRADE_NUM[elo_row.Understanding])+(GRADE_NUM[elo_row.Pronunciation])+(GRADE_NUM[elo_row.Presentation])
        cumulative_elocution_grade_sum=cumulative_elocution_grade_sum+int(round(elocution_grade_row_sum/5))
    if len(elocutions) > 0:
        cumulative_elocution_grade=GRADE_CHOICES_3[int(round(cumulative_elocution_grade_sum/len(elocutions)))]

    # Cumulative Physical Fitness Info
    physical_fit_info = PhysicalFitnessInfo.objects.filter(StudentYearlyInformation = student_yearly_info)
    cumulative_physical_grade_sum=0
    cumulative_physical_grade='-'
    for ph_data in physical_fit_info:
        cumulative_physical_grade_sum=cumulative_physical_grade_sum + GRADE_NUM[ph_data.Grade]
    if len(physical_fit_info) > 0:
        cumulative_physical_grade=GRADE_CHOICES_3[int(round(cumulative_physical_grade_sum/len(physical_fit_info)))]

    # Cumulative Social Activity
    social_activities = SocialActivity.objects.filter(StudentYearlyInformation = student_yearly_info)
    cumulative_social_grade_sum=0
    cumulative_social_grade='-'
    for soc_act_data in social_activities:
        cumulative_social_grade_sum=cumulative_social_grade_sum + GRADE_NUM[soc_act_data.Grade]
    if len(social_activities) > 0:
        cumulative_social_grade=GRADE_CHOICES[int(round(cumulative_social_grade_sum/len(social_activities)))]

    # Cumulative Library Grade
    try:
        library = Library.objects.get(StudentYearlyInformation = student_yearly_info)
        cumulative_library_grade = GRADE_CHOICES[library.Grade]
    except:
        cumulative_library_grade='-'

    # Cumulative Prashala Attendance
    attendances = StudentAttendance.objects.filter(StudentYearlyInformation = student_yearly_info)
    cumulative_attendance=0
    cumulative_workingdays_attendance=0
    cumulative_attendance_percentage='-'
    for attendance in attendances:
        attendance_master = attendance.AttendanceMaster
        class_master = attendance_master.ClassMaster
        if class_master.Type == 'P':
            cumulative_attendance = cumulative_attendance + attendance.ActualAttendance
            cumulative_workingdays_attendance = cumulative_workingdays_attendance + attendance.AttendanceMaster.WorkingDays
    if cumulative_workingdays_attendance > 0:
        cumulative_attendance_percentage = str(round((float(cumulative_attendance) / cumulative_workingdays_attendance * 100),2)) + "%"

    # Cumulative Grade Table
    addSubHeaderToStory(Story,"Report Summary")
    data = []
    data=(
            ['Category','Performance'],
            ['Academics',cumulative_academics],
            ['Evening Sports Activities',cumulative_physical_grade],
            ['Co-curricular Activities',cumulative_cocur_grade],
            ['Self Expression through Arts',cumulative_abhi_grade],
            ['Projects',cumulative_project_grade],
            ['Elocution',cumulative_elocution_grade],
            ['Social activities',cumulative_social_grade],
            ['Thinking Skill',skillGrades['ThinkingSkill']],
            ['Social Skill',skillGrades['SocialSkill']],
            ['Emotional Skill',skillGrades['EmotionalSkill']],
            ['Attitude Towards School',skillGrades['AttitudeTowardsSchool']],
            ['Values',skillGrades['Values']],
            ['Library',cumulative_library_grade],
            ['Attendance',cumulative_attendance_percentage]
        )
    addTableToStory(Story, data, 'CENTER')

    tipStyle = ParagraphStyle(name = 'Note', fontSize = 6, alignment=TA_CENTER)
    Story.append(Paragraph('Note: Grades are Outstanding, Excellent, Good, Satisfactory, Needs improvement and Unsatisfactory,', tipStyle))
    Story.append(Paragraph('which indicate level of participation or performance', tipStyle))

    # Signature
    Story.append(Spacer(1,0.4*inch))
    data = []
    data=(
            ['Supervisor','Vice Principal','Principal'],
            ['(Dr.Bhagyashree Harshe)','(Milind Naik)','(Vivek Ponkshe)'],
        )
    table=Table(data, colWidths=PAGE_WIDTH*0.25)
    table_style = TableStyle([
        ('ALIGN',(0,0),(-1,-1), 'CENTER'),
        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
        ('FONTSIZE',(0,0),(-1,-1),9)
        ])
    table.hAlign='CENTER'
    table.setStyle(table_style)
    Story.append(table)

    Story.append(PageBreak())

def fillAcademicReport(student_yearly_info, Story):
    addMainHeaderToStory(Story, "Part 2: Academic Performance")

    subjects_data = {}
    student_test_data = StudentTestMarks.objects.filter(StudentYearlyInformation=student_yearly_info)
    data = []
    data.append(['','Subject Name','Test type','Marks','Maximum Marks'])
    for test_marks in student_test_data:
        test_mapping = test_marks.TestMapping
        subject_name = test_mapping.SubjectMaster.Name
        if not subjects_data.has_key(subject_name):
            subjects_data[subject_name] = []
        subject_data = subjects_data[subject_name]
        subject_data.append(test_marks)

    #desired sequence
    temp_sort = ['ENG', 'SAN', 'MAT', 'PHY', 'CHE', 'BIO', 'PRA', 'SCI', 'HIS', 'GEO', 'ECO', 'SOC', 'COM']
    cumulative_marks=0
    cumulative_maxmarks=0
    data = []
    data.append(['','W1','W2','W3','W4','T1','N1','F1','Total','%'])
    for subject_item in temp_sort:
        if not subjects_data.has_key(subject_item):
            continue
        subject_data = subjects_data[subject_item]
        subject_name = subject_item
        cumulative_subject_marks=0
        cumulative_subject_maxmarks=0
        subject_test_marks = {}
        subject_test_marks['W1'] = '-'
        subject_test_marks['W2'] = '-'
        subject_test_marks['W3'] = '-'
        subject_test_marks['W4'] = '-'
        subject_test_marks['T1'] = '-'
        subject_test_marks['N1'] = '-'
        subject_test_marks['F1'] = '-'
        subject_test_marks['Total'] = 0
        subject_test_marks['%'] = 0
        for subject_marks in subject_data:
            test_mapping = subject_marks.TestMapping
            subject_name = test_mapping.SubjectMaster.Name
            test_type = test_mapping.TestType
            maximum_marks = test_mapping.MaximumMarks
            marks_obtained = subject_marks.MarksObtained
            if marks_obtained > 0:
                subject_test_marks[test_type] = str(marks_obtained) + " / " + str(int(maximum_marks))
                cumulative_subject_marks = cumulative_subject_marks + marks_obtained
                cumulative_subject_maxmarks = cumulative_subject_maxmarks + maximum_marks
            else:
                subject_test_marks[test_type] = "Absent"
        subject_test_marks['Total'] = str(cumulative_subject_marks) + " / " + str(int(cumulative_subject_maxmarks))
        percentage = 0
        if cumulative_subject_maxmarks > 0:
            percentage = round((cumulative_subject_marks / cumulative_subject_maxmarks * 100),2)
        subject_test_marks['%'] = str(percentage) + '%'
        data_row = []
        data_row.append(subject_name)
        data_row.append(subject_test_marks['W1'])
        data_row.append(subject_test_marks['W2'])
        data_row.append(subject_test_marks['W3'])
        data_row.append(subject_test_marks['W4'])
        data_row.append(subject_test_marks['T1'])
        data_row.append(subject_test_marks['N1'])
        data_row.append(subject_test_marks['F1'])
        data_row.append(subject_test_marks['Total'])
        data_row.append(subject_test_marks['%'])
        data.append(data_row)
        cumulative_marks = cumulative_marks + cumulative_subject_marks
        cumulative_maxmarks = cumulative_maxmarks + cumulative_subject_maxmarks

    addTableToStory(Story, data, 'CENTER')
    Story.append(Spacer(1,0.25*inch))

    percentage = 0
    if cumulative_maxmarks > 0:
        percentage = round((cumulative_marks / cumulative_maxmarks * 100),2)
    addSubHeaderToStory(Story, mark_safe('Grand Total: ' +  str(cumulative_marks) + " / " + str(cumulative_maxmarks)))
    addSubHeaderToStory(Story, 'Percentage: ' + str(percentage) + "%")

    Story.append(Spacer(1,0.5*inch))
    addSubHeaderToStory(Story, "School Attendance")
    fillStudentAttendance(student_yearly_info, Story, 'P')

    class_teacher = student_yearly_info.ClassMaster.Teacher.Name
    addSignatureSpaceToStory(Story,class_teacher, "Class Teacher")
    Story.append(PageBreak())

def fillCoCurricularReport(student_yearly_info, Story):
    addMainHeaderToStory(Story, "Part 3: Co-curricular Activity Report")

    # Abhivyakti Report
    addSubHeaderToStory(Story,"Self Expression through Arts")
    abhivyaktiVikass = AbhivyaktiVikas.objects.filter(StudentYearlyInformation=student_yearly_info)
    if len(abhivyaktiVikass) == 0:
        addNormalTextToStory(Story,'No Activities')
    i=0
    for abhivyaktiVikas in abhivyaktiVikass:
        i = i + 1
        mediumOfExpression = abhivyaktiVikas.MediumOfExpression
        teacher_name = abhivyaktiVikas.Teacher.Name
        participation = GRADE_CHOICES[abhivyaktiVikas.Participation]
        readinessToLearn = GRADE_CHOICES[abhivyaktiVikas.ReadinessToLearn]
        continuityInWork = GRADE_CHOICES[abhivyaktiVikas.ContinuityInWork]
        skillDevelopment = GRADE_CHOICES[abhivyaktiVikas.SkillDevelopment]
        creativity = GRADE_CHOICES[abhivyaktiVikas.Creativity]
        comment = abhivyaktiVikas.PublicComment
        comment = comment.replace('&','and')

        addNormalTextToStory(Story,'<strong>' + 'Abhivyakti' + ' ' + str(i) + '</strong>')
        addNormalTextToStory(Story,'Medium of Expression' + '' + ' : ' + mediumOfExpression)
        addNormalTextToStory(Story,'Teacher' + ' : ' + teacher_name)
        Story.append(Spacer(1,0.2*inch))
        data = []
        data.append(['Participation','Readiness to Learn','Continuity in Work','Skill Development','Creativity'])
        data.append([participation,readinessToLearn,continuityInWork,skillDevelopment,creativity])
        addTableToStory(Story, data, 'CENTER')
        addNormalTextToStory(Story,'Comment' + ' : ' + comment)
        Story.append(Spacer(1,0.2*inch))

    addSignatureSpaceToStory(Story,"Incharge", "Abhivyakti")
    Story.append(Spacer(1,0.5*inch))

    # Competitive Exams
    addSubHeaderToStory(Story,"Competitive Examinations")
    competitive_exams = CompetitiveExam.objects.filter(StudentYearlyInformation=student_yearly_info)
    if len(competitive_exams) == 0:
        addNormalTextToStory(Story,'No Activities')
    i=0
    for competitive_exam in competitive_exams:
        i = i + 1
        name = competitive_exam.Name
        subject = competitive_exam.Subject
        level = competitive_exam.Level
        date = formatDate(competitive_exam.Date)
        try:
            grade = GRADE_CHOICES[competitive_exam.Grade]
        except:
            grade = competitive_exam.Grade
        comment = competitive_exam.PublicComment
        comment = comment.replace('&','and')
        
        addNormalTextToStory(Story,'<strong>' + 'Competitive Exam' + ' ' + str(i) + '</strong>')
        data = []
        data.append(['Name','Subject','Level','Date','Performance'])
        data.append([name,subject,level,date,grade])
        addTableToStory(Story, data, 'CENTER')
        addNormalTextToStory(Story,'Comment' + ' : ' + comment)
        Story.append(Spacer(1,0.2*inch))

    addSignatureSpaceToStory(Story,"Incharge", "Competitive Exams")
    Story.append(Spacer(1,0.5*inch))

    # Competitions
    addSubHeaderToStory(Story,"Competitions")
    competitions = Competition.objects.filter(StudentYearlyInformation=student_yearly_info)
    if len(competitions) == 0:
        addNormalTextToStory(Story,'No Activities')
    i=0
    for competition in competitions:
        i = i + 1
        organizer = competition.Organizer
        subject = competition.Subject
        date = formatDate(competition.Date)
        achievement = competition.Achievement
        guide = competition.Guide
        comment = competition.PublicComment
        comment = comment.replace('&','and')
        
        addNormalTextToStory(Story,'<strong>' + 'Competition'+ ' ' + str(i) + '</strong>')
        data = []
        data.append(['Organizer','Subject','Date','Achievement','Guide'])
        data.append([organizer,subject,date,achievement,guide])
        addTableToStory(Story, data, 'CENTER')
        addNormalTextToStory(Story,'Comment' + ' : ' + comment)
        Story.append(Spacer(1,0.2*inch))

    addSignatureSpaceToStory(Story,"Incharge", "Competition")
    Story.append(PageBreak())

    # Projects
    addSubHeaderToStory(Story,"Projects")
    projects = Project.objects.filter(StudentYearlyInformation=student_yearly_info)
    if len(projects) == 0:
        addNormalTextToStory(Story,'No Activities')
    i=0
    for project in projects:
        i = i + 1
        title = project.Title
        try:
            project_type = PROJECT_TYPE_CHOICES[project.Type]
        except:
            project_type = '-'
        subject = project.Subject
        problem_selection = GRADE_CHOICES_3[project.ProblemSelection]
        review = GRADE_CHOICES_3[project.Review]
        planning = GRADE_CHOICES_3[project.Planning]
        executionAndHardWork = GRADE_CHOICES_3[project.ExecutionAndHardWork]
        documentation = GRADE_CHOICES_3[project.Documentation]
        communication = GRADE_CHOICES_3[project.Communication]
        comment = project.PublicComment
        comment = comment.replace('&','and')

        addNormalTextToStory(Story,'<strong>' + 'Project'+ ' ' + str(i) + '</strong>')
        addNormalTextToStory(Story,'Title' + ' : ' + title)
        addNormalTextToStory(Story,'Type' + ' : ' + project_type)
        addNormalTextToStory(Story,'Subject' + ' : ' + subject)
        Story.append(Spacer(1,0.1*inch))
        data = []
        data.append(['Problem Selection','Review of topic','Planning','Execution','Documentation','Communication'])
        data.append([problem_selection,review,planning,executionAndHardWork,documentation,communication])
        addTableToStory(Story, data, 'CENTER')
        addNormalTextToStory(Story,'Comment' + ' : ' + comment)
        Story.append(Spacer(1,0.2*inch))

    addSignatureSpaceToStory(Story,"Incharge", "Projects")
    Story.append(Spacer(1,0.5*inch))

    # Elocutions
    addSubHeaderToStory(Story,"Elocutions")
    elocutions = Elocution.objects.filter(StudentYearlyInformation=student_yearly_info)
    if len(elocutions) == 0:
        addNormalTextToStory(Story,'No Activities')
    i=0
    for elocution in elocutions:
        i = i + 1
        title = elocution.Title
        memory = GRADE_CHOICES_3[elocution.Memory]
        content = GRADE_CHOICES_3[elocution.Content]
        understanding = GRADE_CHOICES_3[elocution.Understanding]
        pronunciation = GRADE_CHOICES_3[elocution.Pronunciation]
        presentation = GRADE_CHOICES_3[elocution.Presentation]
        comment = elocution.PublicComment
        comment = comment.replace('&','and')

        addNormalTextToStory(Story,'<strong>' + 'Elocution'+ ' ' + str(i) + '</strong>')
        addNormalTextToStory(Story,'Title' + ' : ' + title)
        data = []
        data.append(['Memory','Content','Understanding','Pronunciation','Presentation'])
        data.append([memory,content,understanding,pronunciation,presentation])
        addTableToStory(Story, data, 'CENTER')
        addNormalTextToStory(Story,'Comment' + ' : ' + comment)
        Story.append(Spacer(1,0.2*inch))

    addSignatureSpaceToStory(Story,"Incharge", "Elocution")
    Story.append(Spacer(1,0.5*inch))

    # Work Experience
    addSubHeaderToStory(Story, "Work Experiences")
    workExperiences = WorkExperience.objects.filter(StudentYearlyInformation=student_yearly_info)
    if len(workExperiences) == 0:
        addNormalTextToStory(Story,'No Activities')
    i=0
    for workEx in workExperiences:
        i = i + 1
        teacherName = workEx.Teacher.Name
        task = workEx.Task
        communication = GRADE_CHOICES[workEx.Communication]
        confidence = GRADE_CHOICES[workEx.Confidence]
        involvement = GRADE_CHOICES[workEx.Involvement]
        comment = workEx.PublicComment
        comment = comment.replace('&','and')

        addNormalTextToStory(Story,'<strong>' + 'Work Experience'+ ' ' + str(i) + '</strong>')
        addNormalTextToStory(Story,'Teacher' + ' : ' + teacherName)
        addNormalTextToStory(Story,'Task' + ' : ' + task)
        addNormalTextToStory(Story,'Communication' + ' : ' + communication)
        addNormalTextToStory(Story,'Confidence' + ' : ' + confidence)
        addNormalTextToStory(Story,'Involvement' + ' : ' + involvement)
        addNormalTextToStory(Story,'Comment' + ' : ' + comment)
        Story.append(Spacer(1,0.2*inch))

    addSignatureSpaceToStory(Story,"Incharge", "Work Experience")
    Story.append(Spacer(1,0.5*inch))

    # Other CoCurricular Activities
    addSubHeaderToStory(Story, "Other Co-curricular Activities")
    coCurriculars = CoCurricular.objects.filter(StudentYearlyInformation=student_yearly_info)
    if len(coCurriculars) == 0:
        addNormalTextToStory(Story,'No Activities')
    i=0
    for coCurricular in coCurriculars:
        i = i + 1
        activity = coCurricular.Activity
        objectives = coCurricular.Objectives
        date = formatDate(coCurricular.Date)
        guide = coCurricular.Guide
        try:
            grade = GRADE_CHOICES[coCurricular.Grade]
        except:
            grade = coCurricular.Grade
        comment = coCurricular.PublicComment
        comment = comment.replace('&','and')

        addNormalTextToStory(Story,'<strong>' + 'Activity'+ ' ' + str(i) + '</strong>')
        addNormalTextToStory(Story,'Activity' + ' : ' + activity)
        addNormalTextToStory(Story,'Objectives' + ' : ' + objectives)
        addNormalTextToStory(Story,'Date' + ' : ' + str(date))
        addNormalTextToStory(Story,'Guide' + ' : ' + guide)
        addNormalTextToStory(Story,'Grade' + ' : ' + grade)
        addNormalTextToStory(Story,'Comment' + ' : ' + comment)
        Story.append(Spacer(1,0.2*inch))

    Story.append(PageBreak())

def fillSkillsReport(student_yearly_info, skillGrades, Story):
    addMainHeaderToStory(Story, "Part 4: Skills Report")

    # Thinking Skill
    addSubHeaderToStory(Story, "Thinking Skill")
    thinkingSkills = ThinkingSkill.objects.filter(StudentYearlyInformation=student_yearly_info)
    if len(thinkingSkills) == 0:
        addNormalTextToStory(Story,'No data available')
    else:
        inquiry=0
        logicalThinking = 0
        creativity = 0
        decisionMaking = 0
        length = len(thinkingSkills)
        #add up grades by teachers
        for thinkingSkill in thinkingSkills:
            inquiry = inquiry + GRADE_NUM[thinkingSkill.Inquiry]
            logicalThinking = logicalThinking + GRADE_NUM[thinkingSkill.LogicalThinking]
            creativity = creativity + GRADE_NUM[thinkingSkill.Creativity]
            decisionMaking = decisionMaking + GRADE_NUM[thinkingSkill.DecisionMakingAndProblemSolving]
        
        #total grades
        addNormalTextToStory(Story,'Inquiry' + ' : ' + GRADE_CHOICES[round(inquiry / length)])
        addNormalTextToStory(Story,'LogicalThinking' + ' : ' + GRADE_CHOICES[round(logicalThinking / length)])
        addNormalTextToStory(Story,'Creativity' + ' : ' + GRADE_CHOICES[round(creativity / length)])
        addNormalTextToStory(Story,'DecisionMakingAndProblemSolving' + ' : ' + GRADE_CHOICES[round(decisionMaking / length)])
        Story.append(Spacer(1,0.05*inch))
        skillGrades['ThinkingSkill'] = GRADE_CHOICES[round((inquiry + logicalThinking + creativity + decisionMaking) / (4.0 * length))]
        addNormalTextToStory(Story,'<strong>' + 'Grade' + '</strong>' + ' : ' + skillGrades['ThinkingSkill'])
        Story.append(Spacer(1,0.1*inch))

        addNormalTextToStory(Story,'Comments:')
        i=0
        for thinkingSkill in thinkingSkills:
            comment = thinkingSkill.PublicComment
            comment = comment.replace('&','and')
            if comment != "":
                i=i+1
                addNormalTextToStory(Story, str(i) + '. ' + comment)

    Story.append(Spacer(1,0.2*inch))

    # Social Skill
    addSubHeaderToStory(Story, "Social Skill")
    socialSkills = SocialSkill.objects.filter(StudentYearlyInformation=student_yearly_info)
    if len(socialSkills) == 0:
        addNormalTextToStory(Story,'No data available')
    else:
        communication=0
        interPersonal=0
        teamWork=0
        length = len(socialSkills)
        #add up grades by teachers
        for socialSkill in socialSkills:
            communication = communication + GRADE_NUM[socialSkill.Communication]
            interPersonal = interPersonal + GRADE_NUM[socialSkill.InterPersonal]
            teamWork = teamWork + GRADE_NUM[socialSkill.TeamWork]
       
        #total grades
        addNormalTextToStory(Story,'Communication' + ' : ' + GRADE_CHOICES[round(communication / length)])
        addNormalTextToStory(Story,'InterPersonal' + ' : ' + GRADE_CHOICES[round(interPersonal / length)])
        addNormalTextToStory(Story,'Working in group' + ' : ' + GRADE_CHOICES[round(teamWork / length)])
        Story.append(Spacer(1,0.05*inch))
        skillGrades['SocialSkill'] = GRADE_CHOICES[round((communication + interPersonal + teamWork) / (3.0 * length))]
        addNormalTextToStory(Story,'<strong>' + 'Grade' + '</strong>' + ' : ' + skillGrades['SocialSkill'])
        Story.append(Spacer(1,0.1*inch))

        addNormalTextToStory(Story,'Comments:')
        i=0
        for socialSkill in socialSkills:
            comment = socialSkill.PublicComment
            comment = comment.replace('&','and')
            if comment != "":
                i=i+1
                addNormalTextToStory(Story, str(i) + '. ' + comment)

    Story.append(Spacer(1,0.2*inch))



    # Emotional Skill
    addSubHeaderToStory(Story, "Emotional Skill")
    emotionalSkills = EmotionalSkill.objects.filter(StudentYearlyInformation=student_yearly_info)
    if len(emotionalSkills) == 0:
        addNormalTextToStory(Story,'No data available')
    else:
        empathy=0
        expression=0
        management=0
        length = len(emotionalSkills)
        #add up grades by teachers
        for emotionalSkill in emotionalSkills:
            empathy = empathy + GRADE_NUM[emotionalSkill.Empathy]
            expression = expression + GRADE_NUM[emotionalSkill.Expression]
            management = management + GRADE_NUM[emotionalSkill.Management]
       
        #total grades
        addNormalTextToStory(Story,'Emotional understanding' + ' : ' + GRADE_CHOICES[round(empathy / length)])
        addNormalTextToStory(Story,'Expression' + ' : ' + GRADE_CHOICES[round(expression / length)])
        addNormalTextToStory(Story,'Management' + ' : ' + GRADE_CHOICES[round(management / length)])
        Story.append(Spacer(1,0.05*inch))
        skillGrades['EmotionalSkill'] = GRADE_CHOICES[round((empathy + expression + management) / (3.0 * length))]
        addNormalTextToStory(Story,'<strong>' + 'Grade' + '</strong>' + ' : ' + skillGrades['EmotionalSkill'])
        Story.append(Spacer(1,0.1*inch))
        
        addNormalTextToStory(Story,'Comments:')
        i=0
        for emotionalSkill in emotionalSkills:
            comment = emotionalSkill.PublicComment
            comment = comment.replace('&','and')
            if comment != "":
                i=i+1
                addNormalTextToStory(Story, str(i) + '. ' + comment)

    Story.append(Spacer(1,0.2*inch))



    # Attitude Towards School
    addSubHeaderToStory(Story, "Attitude Towards School")
    attitudeTowardsSchools = AttitudeTowardsSchool.objects.filter(StudentYearlyInformation=student_yearly_info)
    if len(attitudeTowardsSchools) == 0:
        addNormalTextToStory(Story,'No data available')
    else:
        schoolTeachers=0
        schoolMates=0
        schoolPrograms=0
        schoolEnvironment=0
        length = len(attitudeTowardsSchools)
        #add up grades by teachers
        for attitudeTowardsSchool in attitudeTowardsSchools:
            schoolTeachers = schoolTeachers + GRADE_NUM[attitudeTowardsSchool.SchoolTeachers]
            schoolMates = schoolMates + GRADE_NUM[attitudeTowardsSchool.SchoolMates]
            schoolPrograms = schoolPrograms + GRADE_NUM[attitudeTowardsSchool.SchoolPrograms]
            schoolEnvironment = schoolEnvironment + GRADE_NUM[attitudeTowardsSchool.SchoolEnvironment]
            
        #total grades
        addNormalTextToStory(Story,'SchoolTeachers' + ' : ' + GRADE_CHOICES_3[round(schoolTeachers / length)])
        addNormalTextToStory(Story,'SchoolMates' + ' : ' + GRADE_CHOICES_3[round(schoolMates / length)])
        addNormalTextToStory(Story,'SchoolPrograms' + ' : ' + GRADE_CHOICES_3[round(schoolPrograms / length)])
        addNormalTextToStory(Story,'SchoolEnvironment' + ' : ' + GRADE_CHOICES_3[round(schoolEnvironment / length)])
        Story.append(Spacer(1,0.05*inch))
        skillGrades['AttitudeTowardsSchool'] = GRADE_CHOICES_3[round((schoolTeachers + schoolMates + schoolPrograms + schoolEnvironment) / (4.0 * length))]
        addNormalTextToStory(Story,'<strong>' + 'Grade' + '</strong>' + ' : ' + skillGrades['AttitudeTowardsSchool'])
        Story.append(Spacer(1,0.1*inch))
        
        addNormalTextToStory(Story,'Comments:')
        i=0
        for attitudeTowardsSchool in attitudeTowardsSchools:
            comment = attitudeTowardsSchool.PublicComment
            comment = comment.replace('&','and')
            if comment != "":
                i=i+1
                addNormalTextToStory(Story, str(i) + '. ' + comment)

    Story.append(Spacer(1,0.2*inch))



    # Values
    addSubHeaderToStory(Story, "Values")
    valuess = Values.objects.filter(StudentYearlyInformation=student_yearly_info)
    if len(valuess) == 0:
        addNormalTextToStory(Story,'No data available')
    else:
        #add up grades by teachers
        obedience=0
        honesty=0
        equality=0
        responsibility=0
        length = len(valuess)
        for values in valuess:
            obedience = obedience + GRADE_NUM[values.Obedience]
            honesty = honesty + GRADE_NUM[values.Honesty]
            equality = equality + GRADE_NUM[values.Equality]
            responsibility = responsibility + GRADE_NUM[values.Responsibility]
            
        #total grades
        addNormalTextToStory(Story,'Obedience' + ' : ' + GRADE_CHOICES_3[round(obedience / length)])
        addNormalTextToStory(Story,'Honesty' + ' : ' + GRADE_CHOICES_3[round(honesty / length)])
        addNormalTextToStory(Story,'Equality' + ' : ' + GRADE_CHOICES_3[round(equality / length)])
        addNormalTextToStory(Story,'Responsibility' + ' : ' + GRADE_CHOICES_3[round(responsibility / length)])
        Story.append(Spacer(1,0.05*inch))
        skillGrades['Values'] = GRADE_CHOICES_3[round((obedience + honesty + equality + responsibility) / (4.0 * length))]
        addNormalTextToStory(Story,'<strong>' + 'Grade' + '</strong>' + ' : ' + skillGrades['Values'])
        Story.append(Spacer(1,0.1*inch))
        
        addNormalTextToStory(Story,'Comments:')
        i=0
        for values in valuess:
            comment = values.PublicComment
            comment = comment.replace('&','and')
            if comment != "":
                i=i+1
                addNormalTextToStory(Story, str(i) + '. ' + comment)

    Story.append(Spacer(1,0.2*inch))
    
    Story.append(PageBreak())

def fillOutdoorActivityReport(student_yearly_info, Story):
    addMainHeaderToStory(Story, "Part 5: Outdoor Activity Report")

    # Physical Education
    addSubHeaderToStory(Story, "Physical Education")
    try:
        physicalEducation = PhysicalEducation.objects.get(StudentYearlyInformation=student_yearly_info)
        
        addNormalTextToStory(Story,'Name' + ' : ' + physicalEducation.Name)
        addNormalTextToStory(Story,'Pratod' + ' : ' + physicalEducation.Pratod)
        addNormalTextToStory(Story,'Ability to work in team' + ' : ' + GRADE_CHOICES[physicalEducation.AbilityToWorkInTeam])
        addNormalTextToStory(Story,'Cooperation' + ' : ' + GRADE_CHOICES[physicalEducation.Cooperation])
        addNormalTextToStory(Story,'Leadership skill' + ' : ' + GRADE_CHOICES[physicalEducation.LeadershipSkill])
        comment = physicalEducation.PublicComment
        comment = comment.replace('&','and')
        addNormalTextToStory(Story,'Comment' + ' : ' + comment)
    except:
        addNormalTextToStory(Story,'Not available')
    Story.append(Spacer(1,0.2*inch))
    
    pratod = ''
    # Physical Fitness Report
    addSubHeaderToStory(Story, "Physical Fitness Report")
    try:
        physical_fitness_info = PhysicalFitnessInfo.objects.get(StudentYearlyInformation=student_yearly_info)

        weight = physical_fitness_info.Weight
        height = physical_fitness_info.Height
        ffb = physical_fitness_info.FlexibleForwardBending
        fbb = physical_fitness_info.FlexibleBackwardBending
        sbj = physical_fitness_info.SBJ
        verticle_jump = physical_fitness_info.VerticleJump
        ball_throw = physical_fitness_info.BallThrow
        shuttle_run = physical_fitness_info.ShuttleRun
        sit_ups = physical_fitness_info.SitUps
        sprint = physical_fitness_info.Sprint
        running_400m = physical_fitness_info.Running400m
        short_put = physical_fitness_info.ShortPutThrow
        split = physical_fitness_info.Split
        bmi = physical_fitness_info.BodyMassIndex
        bmi = round(float(weight) / (float(height / 100.0) * float(height / 100.0)), 2)
        balancing = physical_fitness_info.Balancing
        try:
            grade = GRADE_CHOICES_3[physical_fitness_info.Grade]
        except:
            grade = physical_fitness_info.Grade
        pathak = physical_fitness_info.Pathak
        special_sport = physical_fitness_info.SpecialSport
        comment = physical_fitness_info.PublicComment
        comment = comment.replace('&','and')

        data = []
        data.append(['W','H','FFB','FBB','SBJ','VJ','BT','SR','SU','S','400m','SP', 'Spl','BMI','B'])
        data.append([weight, height, ffb, fbb, sbj, verticle_jump, ball_throw,
                     shuttle_run, sit_ups, sprint, running_400m, short_put, split, bmi, balancing])
        addTableToStory(Story, data, 'CENTER')
        addNormalTextToStory(Story,'Special Sport' + ' : ' + special_sport)
        addNormalTextToStory(Story,'House' + ' : ' + pathak)
        Story.append(Spacer(1,0.2*inch))
        pratod = physical_fitness_info.Pratod
        Story.append(Spacer(1,0.2*inch))
    except:
        addNormalTextToStory(Story,'Not available')
        pratod = ''
        grade = '-'
        comment = ''

    # Dal Attendance
    addSubHeaderToStory(Story,"Evening Sports Attendance")
    fillStudentAttendance(student_yearly_info, Story, 'D')

    Story.append(Spacer(1,0.1*inch))
    addNormalTextToStory(Story,'<strong>' + 'Grade' + ' : ' + grade + '</strong>')
    addNormalTextToStory(Story,'Comment' + ' : ' + comment)
    Story.append(Spacer(1,0.25*inch))

    # Social Activities
    addSubHeaderToStory(Story,"Social Activities")
    social_activities = SocialActivity.objects.filter(StudentYearlyInformation=student_yearly_info)
    if len(social_activities) == 0:
        addNormalTextToStory(Story,'No Activities')
    i=0
    for social_activity in social_activities:
        i = i + 1
        activity = social_activity.Activity
        objectives = social_activity.Objectives
        date = formatDate(social_activity.Date)
        organizer = social_activity.Organizer
        try:
            grade = GRADE_CHOICES[social_activity.Grade]
        except:
            grade = social_activity.Grade
        comment = social_activity.PublicComment
        comment = comment.replace('&','and')

        addNormalTextToStory(Story,'<strong>' + 'Activity'+ ' ' + str(i) + '</strong>')
        addNormalTextToStory(Story,'Activity' + ' : ' + activity)
        addNormalTextToStory(Story,'Objectives' + ' : ' + objectives)
        addNormalTextToStory(Story,'Date' + ' : ' + str(date))
        addNormalTextToStory(Story,'Organizer' + ' : ' + organizer)
        addNormalTextToStory(Story,'Grade' + ' : ' + grade)
        addNormalTextToStory(Story,'Comment' + ' : ' + comment)
        Story.append(Spacer(1,0.2*inch))
    Story.append(Spacer(1,0.5*inch))

    addSignatureSpaceToStory(Story,pratod , "Activity Incharge")
    Story.append(PageBreak())

def fillLibraryAndMedicalReport(student_yearly_info, Story):
    addMainHeaderToStory(Story, "Part 6: Other")

    #Library Report
    addSubHeaderToStory(Story, "Library Report")
    try:
        library = Library.objects.get(StudentYearlyInformation=student_yearly_info)

        comment = library.PublicComment
        comment = comment.replace('&','and')
        
        data = []
        data.append(['Books Read',str(library.BooksRead)])
        data.append(['Grade',GRADE_CHOICES[library.Grade]])
        data.append(['Comment',comment])
        addNoBorderTableToStory(Story, data)   
    except:
        addNormalTextToStory(Story,'Not available')

    Story.append(Spacer(1,0.3*inch))
    addSignatureSpaceToStory(Story, "","Librarian")
    Story.append(Spacer(1,1*inch))


    #Medical Report
    addSubHeaderToStory(Story, "Medical Report")
    try:
        medicalReport = MedicalReport.objects.get(StudentYearlyInformation=student_yearly_info)

        data = []
        data.append(['Height',str(medicalReport.Height)])
        data.append(['Weight',str(medicalReport.Weight)])
        data.append(['Blood Group',medicalReport.BloodGroup])
        data.append(['VisionL',medicalReport.VisionL])
        data.append(['VisionR',medicalReport.VisionR])
        data.append(['Oral Hygiene',medicalReport.OralHygiene])
        data.append(['Specific Ailment',medicalReport.SpecificAilment])
        data.append(['',''])
        data.append(['Doctor',medicalReport.Doctor])
        data.append(['Clinic Address',medicalReport.ClinicAddress])
        data.append(['Phone',medicalReport.Phone])
        addNoBorderTableToStory(Story, data)
    except:
        addNormalTextToStory(Story,'Not available')
 
    Story.append(PageBreak())

# PDF Certificate :	--------------------------------------------------

def CertificateLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',6)
    now_time = datetime.datetime.now()
    epoch_seconds = time.mktime(now_time.timetuple())
    canvas.drawString(PAGE_WIDTH * 0.6, 0.75 * inch, "%s          ES%dP%d" % ("Jnana Prabodhini Prashala's Bonafide Certificate", epoch_seconds, doc.page))
    canvas.restoreState()
    pageBorder(canvas)

def addCertificateTextToStory(Story,header_text):
    style = ParagraphStyle(name = 'Text', fontSize = 11, alignment=TA_CENTER)
    Story.append(Paragraph(header_text, style))
    Story.append(Spacer(1,0.05*inch))

def addCertificateNumberTextToStory(Story,header_text):
    style = ParagraphStyle(name = 'NumberText', fontSize = 8, alignment=TA_RIGHT)
    Story.append(Paragraph(header_text, style))

#
@csrf_exempt
def certificatePDF(request):
    if request.POST:
        keys = request.POST.keys()
        registration_number_min = int(request.POST['registration_number_min'])
        registration_number_max = int(request.POST['registration_number_max'])
        standard = 0 
        division = "-"

        registration_numbers = []
        registration_number = registration_number_min
        while registration_number <= registration_number_max:
            registration_numbers.append(registration_number)
            registration_number = registration_number + 1
        Story = []
        fillCertificatePdfData(Story, registration_numbers, standard, division)
        response = HttpResponse(mimetype='application/pdf')
        doc = SimpleDocTemplate(response)
        doc.build(Story, onFirstPage=CertificateLaterPages, onLaterPages=CertificateLaterPages)
        return response
    else:
        return HttpResponse ('<html><body>'
                             + '<P><B><BIG><BIG>Bonafide Certificate in PDF format</BIG></BIG></B></P>'
                             + '<form action="" method="POST">'
                             + '<BIG>Registration Numbers: </BIG><input type="text" name="registration_number_min" value="0" id="registration_number_min" size="5"></td>'
                             + '<BIG> to </BIG><input type="text" name="registration_number_max" value="9999" id="registration_number_max" size="5"><br /><br />'
                             + '<input type="submit" value="Enter" />'
                             + '</form>'
                             + '<br /><br />'
                             + '<P>An unsaved PDF file will be generated.'
                             + '<br />It will contain 1 page per valid registration number.'
                             + '<br />At bottom-right, the number after letter P is the page number in this PDF document</P>'
                             + '</body></html>')

def fillCertificatePdfData(Story, registration_nos, standard, division):
    for registration_no in registration_nos:
        try:
            student_basic_info = StudentBasicInfo.objects.get(RegistrationNo = registration_no)
        except:
            continue
        fillCertificateHeader(Story)
        fillCertificate(student_basic_info, Story)

def fillCertificateHeader(Story):
    style = ParagraphStyle(name='styleName', fontName ='Times-Bold', fontSize = 18, alignment=TA_CENTER)
    Story.append(Paragraph("Jnana Prabodhini Prashala", style))

    Story.append(Spacer(1,0.1*inch))

    style = ParagraphStyle(name='styleName', fontName ='Times-Roman', fontSize = 8, alignment=TA_CENTER)
    Story.append(Paragraph("School Affiliation No:1130001", style))
    Story.append(Paragraph("C.B.S.E./A.I./69/(G)/12096/30/4/69", style))

    style = ParagraphStyle(name='styleName', fontName ='Times-Roman', fontSize = 9, alignment=TA_CENTER)
    Story.append(Paragraph("510, Sadashiv Peth, Pune, 411030", style))
    Story.append(Paragraph("email: prashala@jnanaprabodhini.org", style))
    Story.append(Paragraph("http://prashala.jnanaprabodhini.org", style))
    Story.append(Paragraph("Tel: +91 20 24207122", style))

    data = []
    data.append(["Certificate"])
    table_style = TableStyle([
        ('FONT', (0,0), (-1,0), 'Times-Bold'),
        ('ALIGN',(0,0),(-1,-1), 'CENTER'),
        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
        ('FONTSIZE',(0,0),(-1,-1),12),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LINEABOVE',(0,0),(0,0),1,colors.black),
        ('LINEBELOW',(0,0),(0,0),1,colors.black)
        ])
    margin=0.7*inch
    column_widths=((PAGE_WIDTH-2*(margin))*0.9)
    table=Table(data, colWidths=column_widths)
    table.setStyle(table_style)
    table.hAlign = 'CENTER'
    Story.append(table)

    Story.append(Spacer(1,0.1*inch))

def fillCertificate(student_basic_info, Story):
    certificateNumber = str(student_basic_info.RegistrationNo)
    addCertificateNumberTextToStory(Story, "Certificate No. : " + certificateNumber)

    schoolRegistrationNumber = str(student_basic_info.RegistrationNo)
    addCertificateNumberTextToStory(Story, "School Registration No. : " + schoolRegistrationNumber)

    Story.append(Spacer(1,0.2*inch))

    now_time = datetime.datetime.now()
    date = formatDate(now_time)
    addCertificateNumberTextToStory(Story, "Date : " + date)

    Story.append(Spacer(1,0.7*inch))
    studentName = student_basic_info.FirstName + ' ' + student_basic_info.LastName
    addCertificateTextToStory(Story, "This is to certify that <strong>" + studentName + "</strong> is/was a bona fide student of")

    dateOfRegistration = student_basic_info.DateOfRegistration
    fromYear = dateOfRegistration.year

    terminationDate = student_basic_info.TerminationDate
    try:
        toYear = terminationDate.year
        toYearStr = str(toYear)
    except:
        now_time = datetime.datetime.now()
        toYear = now_time.year
        toYearStr = "till date"

    student_yearly_infos = StudentYearlyInformation.objects.filter(StudentBasicInfo = student_basic_info)

    admissionClass = "______"
    admission_year1 = str(int(fromYear) - 1) + "-" + str(fromYear)
    admission_year2 = str(fromYear) + "-" + str(int(fromYear) + 1)
    for yearly_info in student_yearly_infos:
        student_year = yearly_info.ClassMaster.AcademicYear.Year
        if student_year == admission_year1:
            admissionClass = str(yearly_info.ClassMaster.Standard) + "th"
        elif student_year == admission_year2:
            admissionClass = str(yearly_info.ClassMaster.Standard) + "th"

    terminationClass = "______"
    terminationYear1 = str(toYear) + "-" + str(int(toYear) + 1)
    terminationYear2 = str(int(toYear) - 1) + "-" + str(toYear)
    for yearly_info in student_yearly_infos:
        student_year = yearly_info.ClassMaster.AcademicYear.Year
        if student_year == terminationYear1:
            terminationClass = str(yearly_info.ClassMaster.Standard) + "th"
        elif student_year == terminationYear2:
            terminationClass = str(yearly_info.ClassMaster.Standard) + "th"

    addCertificateTextToStory(Story, "Jnana Prabodhini Prashala during the year " + "<strong>" + str(fromYear) + "</strong>" + " to " + "<strong>" + toYearStr + "</strong>")
    addCertificateTextToStory(Story, "from " + "<strong>" + admissionClass + "</strong>" + " class to " + "<strong>" + terminationClass + "</strong>" + " class.")

    genderMentionCapital = "He"
    genderBelong = "his"
    genderMentionSmall= "he"
    if student_basic_info.Gender == "F":
        genderMentionCapital = "She"
        genderBelong = "her"
        genderMentionSmall= "she"

    caste = str(student_basic_info.Caste)
    if caste == "None":
        caste = "______________"
    addCertificateTextToStory(Story, genderMentionCapital + " belongs to " + "<strong>" + caste + "</strong>" + " category")

    dateOfBirth = student_basic_info.DateOfBirth
    birthDate = formatDate(dateOfBirth)
    addCertificateTextToStory(Story, "According to our school record, " + genderBelong + " birth date is " + "<strong>" + birthDate +"</strong>")

    addCertificateTextToStory(Story, "To the best of my knowledge and belief, " + genderMentionSmall + " bears good moral character.")

    Story.append(Spacer(1,0.7*inch))

    addSignatureSpaceToStory(Story, "Principal","Jnana Prabodhini Prashala")

    Story.append(Spacer(1,0.1*inch))
    Story.append(PageBreak())

# PDF School Leaving :	--------------------------------------------------

def SchoolLeavingLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',6)
    now_time = datetime.datetime.now()
    epoch_seconds = time.mktime(now_time.timetuple())
    canvas.drawString(PAGE_WIDTH * 0.55, 0.75 * inch, "%s          ES%dP%d" % ("Jnana Prabodhini Prashala's School Leaving Certificate", epoch_seconds, doc.page))
    canvas.restoreState()
    pageBorder(canvas)

def addSchoolLeavingTextToStory(Story,header_text):
    style = ParagraphStyle(name = 'Text', fontSize = 11, alignment=TA_CENTER)
    Story.append(Paragraph(header_text, style))
    Story.append(Spacer(1,0.05*inch))

#
def schoolLeavingPDF(request):
    if request.POST:
        keys = request.POST.keys()
        registration_number_min = int(request.POST['registration_number_min'])
        registration_number_max = int(request.POST['registration_number_max'])
        standard = int(request.POST['standard'])
        division = request.POST['division']
        year_option = request.POST['year_option']

        registration_numbers = []
        registration_number = registration_number_min
        while registration_number <= registration_number_max:
            registration_numbers.append(registration_number)
            registration_number = registration_number + 1
            
        Story = []
        fillSchoolLeavingPdfData(Story, registration_numbers, standard, division, year_option)
        
        response = HttpResponse(mimetype='application/pdf')
        doc = SimpleDocTemplate(response)
        doc.build(Story, onFirstPage=SchoolLeavingLaterPages, onLaterPages=SchoolLeavingLaterPages)

        return response
    else:
        return HttpResponse ('<html><body>'
                             + '<P><B><BIG><BIG>School Leaving Certificate in PDF format</BIG></BIG></B></P>'
                             + '<form action="" method="POST">'
                             + '<BIG>Registration Numbers: </BIG><input type="text" name="registration_number_min" value="0" id="registration_number_min" size="5"></td>'
                             + '<BIG> to </BIG><input type="text" name="registration_number_max" value="9999" id="registration_number_max" size="5"><br /><br />'
                             + '<BIG>Standard</BIG>: <input type="text" name="standard" value="0" id="standard" size="3"><br /><br />'
                             + '<BIG>Division </BIG>: <input type="text" name="division" value="-" id="division" size="3"><br /><br />'
                             + 'Year: <input type="text" name="year_option" value="2008-2009" id="year_option" size="10"><br /><br />'
                             + '<input type="submit" value="Enter" />'
                             + '</form>'
                             + '<br /><br />'
                             + 'Standard - 5 to 10 for respective Standard, any other value for All<br />'
                             + 'Division - B for Boys, G for Girls, any other value for for Both<br /><br />'
                             + '<P>An unsaved PDF file will be generated.'
                             + '<br />It will contain 1 page per valid registration number.'
                             + '<br />At bottom-right, the number after letter P is the page number in this PDF document</P>'
                             + '</body></html>')

def fillSchoolLeavingPdfData(Story, registration_nos, standard, division, year_option):
    for registration_no in registration_nos:
        try:
            student_basic_info = StudentBasicInfo.objects.get(RegistrationNo = registration_no)
            student_yearly_infos = StudentYearlyInformation.objects.filter(StudentBasicInfo = student_basic_info)
        except:
            continue
        for student_yearly_info in student_yearly_infos:
            student_year = student_yearly_info.ClassMaster.AcademicYear.Year
            if student_year != year_option:
                continue
            student_standard = student_yearly_info.ClassMaster.Standard
            if (standard >= 5) and (standard <= 10) and (student_standard != standard):
                continue
            student_division = student_yearly_info.ClassMaster.Division
            if ((division == 'B') or (division == 'G')) and (student_division != division):
                continue

            fillSchoolLeavingHeader(Story)
            fillSchoolLeaving(student_yearly_info, Story)

def fillSchoolLeavingHeader(Story):
    style = ParagraphStyle(name='styleName', fontName ='Times-Bold', fontSize = 18, alignment=TA_CENTER)
    Story.append(Paragraph("Jnana Prabodhini Prashala", style))

    Story.append(Spacer(1,0.1*inch))

    style = ParagraphStyle(name='styleName', fontName ='Times-Roman', fontSize = 8, alignment=TA_CENTER)
    Story.append(Paragraph("School Affiliation No:1130001", style))
    Story.append(Paragraph("C.B.S.E./A.I./69/(G)/12096/30/4/69", style))

    style = ParagraphStyle(name='styleName', fontName ='Times-Roman', fontSize = 9, alignment=TA_CENTER)
    Story.append(Paragraph("510, Sadashiv Peth, Pune, 411030", style))
    Story.append(Paragraph("email: prashala@jnanaprabodhini.org", style))
    Story.append(Paragraph("http://prashala.jnanaprabodhini.org", style))
    Story.append(Paragraph("Tel: +91 20 24207122", style))

    data = []
    data.append(["School Leaving Certificate"])
    table_style = TableStyle([
        ('FONT', (0,0), (-1,0), 'Times-Bold'),
        ('ALIGN',(0,0),(-1,-1), 'CENTER'),
        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
        ('FONTSIZE',(0,0),(-1,-1),12),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LINEABOVE',(0,0),(0,0),1,colors.black),
        ('LINEBELOW',(0,0),(0,0),1,colors.black)
        ])
    margin=0.7*inch
    column_widths=((PAGE_WIDTH-2*(margin))*0.9)
    table=Table(data, colWidths=column_widths)
    table.setStyle(table_style)
    table.hAlign = 'CENTER'
    Story.append(table)

    Story.append(Spacer(1,0.1*inch))

def fillSchoolLeaving(student_yearly_info, Story):
    student_basic_info = student_yearly_info.StudentBasicInfo

    certificateNumber = str(student_basic_info.RegistrationNo)
    addCertificateNumberTextToStory(Story, "School Leaving Certificate No. : " + certificateNumber)

    schoolRegistrationNumber = str(student_basic_info.RegistrationNo)
    addCertificateNumberTextToStory(Story, "School Registration No. : " + schoolRegistrationNumber)

    Story.append(Spacer(1,0.2*inch))

    now_time = datetime.datetime.now()
    date = formatDate(now_time)
    addCertificateNumberTextToStory(Story, "Date : " + date)

    terminationDate = student_basic_info.TerminationDate
    try:
        terminationDate = formatDate(terminationDate)
    except:
        terminationDate = "NOT AVAILABLE"
        addSchoolLeavingTextToStory(Story, "CERTIFICATE IS NOT VALID as Date of Leaving School is not available")

    studentName = student_basic_info.FirstName + ' ' + student_basic_info.LastName

    nationality = student_basic_info.Nationality
    caste = str(student_basic_info.Caste)
    if caste == "None":
        caste = ""
    place = student_basic_info.BirthPlace
    lastSchool = student_basic_info.PreviousSchool

    dateOfBirth = student_basic_info.DateOfBirth
    birthDate = dateOfBirth.strftime("%d/%m/%Y")
    birthDateInWords = int2word(dateOfBirth.day) + FULLMONTH_CHOICES[dateOfBirth.month] + " " + int2word(dateOfBirth.year)

    dateOfRegistration = student_basic_info.DateOfRegistration
    dateOfRegistration = formatDate(dateOfRegistration)

    progress = ""
    conduct = ""
    reason = student_basic_info.ReasonOfLeavingSchool

    Story.append(Spacer(1,0.1*inch))
    data = []
    data=(
            ["Name of the Pupil: " , studentName],
            ["Nationality: " , nationality],
            ["Scheduled Caste or Tribe (if any): " , caste],
            ["Place of Birth: " , place],
            ["Date of Birth (dd/mm/yyyy): " , birthDate],
            ["Date of Birth (in Words): " , birthDateInWords],
            ["Last School attended: " , lastSchool],
            ["Date of Admission: " , dateOfRegistration],
            ["Progress: " , progress],
            ["Conduct: " , conduct],
            ["Date of Leaving School: " , terminationDate],
            ["Reason of Leaving School: " , reason],
        )
    table=Table(data)
    table_style = TableStyle([
        ('FONT', (0,0), (-1,0), 'Times-Roman'),
        ('FONTSIZE',(0,0),(-1,-1),10)])
    table.setStyle(table_style)
    table.hAlign='LEFT'
    Story.append(table)
    Story.append(Spacer(1,0.2*inch))

    addSchoolLeavingTextToStory(Story, "Certified that the above information is in accordance with the School Register.")

    Story.append(Spacer(1,0.7*inch))

    addSignatureSpaceToStory(Story, "Principal","Jnana Prabodhini Prashala")

    Story.append(Spacer(1,0.1*inch))
    Story.append(PageBreak())

def int2word(n):
    """
    convert an integer number n into a string of english words
    """
    # break the number into groups of 3 digits using slicing
    # each group representing hundred, thousand, million, billion, ...
    n3 = []
    r1 = ""
    # create numeric string
    ns = str(n)
    for k in range(3, 33, 3):
        r = ns[-k:]
        q = len(ns) - k
        # break if end of ns has been reached
        if q < -2:
            break
        else:
            if  q >= 0:
                n3.append(int(r[:3]))
            elif q >= -1:
                n3.append(int(r[:2]))
            elif q >= -2:
                n3.append(int(r[:1]))
        r1 = r

    # break each group of 3 digits into
    # ones, tens/twenties, hundreds
    # and form a string
    nw = ""
    for i, x in enumerate(n3):
        b1 = x % 10
        b2 = (x % 100)//10
        b3 = (x % 1000)//100

        if x == 0:
            continue  # skip
        else:
            t = thousands[i]
        if b2 == 0:
            nw = ones[b1] + t + nw
        elif b2 == 1:
            nw = tens[b1] + t + nw
        elif b2 > 1:
            nw = twenties[b2] + ones[b1] + t + nw
        if b3 > 0:
            nw = ones[b3] + "Hundred " + nw
    return nw

# ------------------- Cards PDF --------------------------------

def cardsLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',6)
    now_time = datetime.datetime.now()
    epoch_seconds = now_time.strftime("%d %b %Y %I:%M:%S%p")
    #the number at the bottom right of page will let us trace the exact date and time and will never repeat for any documents
    canvas.drawString(0.4 * PAGE_WIDTH, 0.1 * inch, "%s          %s   page %d" % ("Jnana Prabodhini Prashala - Students Information", epoch_seconds, doc.page))
    canvas.restoreState()

def checkBoxValue(request, checkBoxName):
    try:
        return (request.POST[checkBoxName] == 'on')
    except:
        return False

#
@csrf_exempt
def cardsPDF(request):
    if request.POST:
        keys = request.POST.keys()
        
        #pick values from html form
        #range and filters for registration numbers
        registration_number_min = int(request.POST['registration_number_min'])
        registration_number_max = int(request.POST['registration_number_max'])
        standard = int(request.POST['standard'])
        division = request.POST['division']
        academic_year = request.POST['year_option']

        #selection of fields to be shown on card
        isShowRegNo = checkBoxValue(request, 'isShowRegNo')
        isShowRollNo = checkBoxValue(request, 'isShowRollNo')
        isShowName = checkBoxValue(request, 'isShowName')
        isShowAddress = checkBoxValue(request, 'isShowAddress')
        isShowBirthDate = checkBoxValue(request, 'isShowBirthDate')
        isShowPhoneNo = checkBoxValue(request, 'isShowPhoneNo')

        isSortByRollNo = checkBoxValue(request, 'isSortByRollNo')

        #select student yearly informations
        student_yearly_infos = []
        selectYearlyInfos(student_yearly_infos, registration_number_min, registration_number_max,
                          standard, division, academic_year)

        if isSortByRollNo:
            student_yearly_infos.sort(compareYearlyInfo)

        #populate content for the list of reg numbers
        Story = []
        fillCardsData(Story, student_yearly_infos,
                      isShowRegNo, isShowRollNo, isShowName, isShowAddress, isShowBirthDate, isShowPhoneNo)

        #show an unsaved pdf document in the browser, using reportPDF
        response = HttpResponse(mimetype='application/pdf')

        margin=0.01*PAGE_WIDTH
        doc = SimpleDocTemplate(response,
                leftMargin=margin,
                rightMargin=margin,
                topMargin=margin,
                bottomMargin=margin)
        doc.build(Story, onFirstPage=cardsLaterPages, onLaterPages=cardsLaterPages)
        
        return response
    else:
        return HttpResponse ('<html><body>'
                             + '<P><B><BIG><BIG>Cards in PDF format</BIG></BIG></B></P>'
                             + '<form action="" method="POST">'
                             + '<BIG>Registration Numbers: </BIG><input type="text" name="registration_number_min" value="1000" id="registration_number_min" size="5"></td>'
                             + '<BIG> to </BIG><input type="text" name="registration_number_max" value="6000" id="registration_number_max" size="5"><br /><br />'
                             + '<BIG>Standard</BIG>: <input type="text" name="standard" value="0" id="standard" size="3"><br /><br />'
                             + '<BIG>Division </BIG>: <input type="text" name="division" value="-" id="division" size="3"><br /><br />'
                             + '<BIG>Year </BIG>: <input type="text" name="year_option" value="2009-2010" id="year_option" size="10"><br /><br />'
                             + '<input type="checkbox" name="isShowRegNo" checked>Registration number</input><br />'
                             + '<input type="checkbox" name="isShowRollNo" checked>Roll number</input><br />'
                             + '<input type="checkbox" name="isShowName" checked>Name</input><br />'
                             + '<input type="checkbox" name="isShowAddress" checked>Address</input><br />'
                             + '<input type="checkbox" name="isShowBirthDate" checked>Birth Date</input><br />'
                             + '<input type="checkbox" name="isShowPhoneNo" checked>Phone number</input><br />'
                             + '<br />'
                             + '<input type="checkbox" name="isSortByRollNo" checked>Sort by Standard and Roll number</input><br />'
                             + '<br />'
                             + '<input type="submit" value="Enter" />'
                             + '</form>'
                             + '<br /><br />'
                             + 'Standard - 5 to 10 for respective Standard, any other value for All<br />'
                             + 'Division - B for Boys, G for Girls, any other value for for Both<br /><br />'
                             + '<P>An unsaved PDF file will be generated.</P>'
                             + '</body></html>')

#use this function for other pdfs once tested
def selectYearlyInfos(selected_yearly_infos, registration_number_min, registration_number_max, standard, division, academic_year):

    #populate a list of registration numbers for the specified range
    registration_numbers = []
    registration_number = registration_number_min
    while registration_number <= registration_number_max:
        registration_numbers.append(registration_number)
        registration_number = registration_number + 1

    #filter and populate a list of yearly informations
    for registration_no in registration_numbers:
        try:
            #read basic and yearly info for the list of reg numbers
            student_basic_info = StudentBasicInfo.objects.get(RegistrationNo = registration_no)
            student_yearly_infos = StudentYearlyInformation.objects.filter(StudentBasicInfo = student_basic_info)
            student_addtional_info = StudentAdditionalInformation.objects.get(Id=student_basic_info.RegistrationNo)
        except:
            #skip the reg numbers if basic info is not found
            continue

        #filter
        for student_yearly_info in student_yearly_infos:

            #filter by year
            student_year = student_yearly_info.ClassMaster.AcademicYear.Year
            if student_year != academic_year:
                continue

            #filter by standard if a valid entry is available
            student_standard = student_yearly_info.ClassMaster.Standard
            if (standard >= 5) and (standard <= 10) and (student_standard != standard):
                continue

            #filter by division if a valid entry is available
            student_division = student_yearly_info.ClassMaster.Division
            if ((division == 'B') or (division == 'G')) and (student_division != division):
                continue

            #select
            selected_yearly_infos.append(student_yearly_info)

def compareYearlyInfo(yearly_info_left, yearly_info_right):  
    rollNo_left = comparisonIndex(yearly_info_left)
    rollNo_right = comparisonIndex(yearly_info_right)
    return cmp(int(rollNo_left), int(rollNo_right))

def comparisonIndex(student_yearly_info):
    division = student_yearly_info.ClassMaster.Division
    standard = student_yearly_info.ClassMaster.Standard
    rollNo = student_yearly_info.RollNo
    return standard * 10000 + DIVISION_NUM[division] * 1000 + rollNo
    
def fillCardsData(Story, student_yearly_infos,
                  isShowRegNo, isShowRollNo, isShowName, isShowAddress, isShowBirthDate, isShowPhoneNo):

    count = len(student_yearly_infos)
    #take 2 consecutive entries at a time to fill a row of 2 cards
    for i in range(0, count, 2):
	fillCardRow(Story, student_yearly_infos[i:i+2],
                    isShowRegNo, isShowRollNo, isShowName, isShowAddress, isShowBirthDate, isShowPhoneNo)

def fillCardRow(Story, student_yearly_infos,
                isShowRegNo, isShowRollNo, isShowName, isShowAddress, isShowBirthDate, isShowPhoneNo):

    cardsRow = []
    for student_yearly_info in student_yearly_infos:

        #populate selected fields to a card
        student_basic_info = student_yearly_info.StudentBasicInfo
        student_additional_info = StudentAdditionalInformation.objects.get(Id=student_basic_info.RegistrationNo)

        studentCardText = ''
        
        if isShowRegNo:
            regNo = 'RegNo' + ' ' + str(student_basic_info.RegistrationNo)
            studentCardText += regNo + ',    '

        if isShowRollNo:
            rollNo = str(student_yearly_info.ClassMaster.Standard) + 'th Std' + ',    ' + 'RollNo' + ' ' + str(student_yearly_info.RollNo)
            studentCardText += rollNo

        if studentCardText != '':
            studentCardText += '<br/>'

        if isShowName:
            name = student_basic_info.FirstName + ' ' + student_basic_info.LastName
            studentCardText += name + '<br/>'

        if isShowAddress:
            address = student_additional_info.Address
            studentCardText += address + '<br/>'

        if isShowBirthDate:
            birthDate = 'Birth Date:' + ' ' + formatDate(student_basic_info.DateOfBirth)
            studentCardText += birthDate + '<br/>'

        if isShowPhoneNo:
            phoneNoText = 'PhoneNo:' + ' ' + str(student_additional_info.Fathers_Phone_No) + '   ' + str(student_additional_info.Mothers_Phone_No)
            studentCardText += phoneNoText + '<br/>'

        #append card to row
        style = ParagraphStyle(name = 'NameStyle', fontSize = 12)
        studentCardText = studentCardText.replace('&','and')
        studentCard = Paragraph(studentCardText, style)
        cardsRow.append(studentCard)

    #for last odd record
    if len(student_yearly_infos) < 2:
        cardsRow.append('')
   
    Story.append(CondPageBreak(1*inch))

    #table
    data = [cardsRow]
    colWidthValues = [0.49*PAGE_WIDTH,0.49*PAGE_WIDTH]
    table=Table(data, colWidths=colWidthValues)
    table_style = TableStyle([('VALIGN',(0,0),(-1,-1), 'TOP')])
    table.setStyle(table_style)
    Story.append(table)

#----------------------------------------------------------------------------------------------------

marks_add = login_required(marks_add)
competition_add = login_required(competition_add)
attendance_add = login_required(attendance_add)
elocution_add = login_required(elocution_add)
abhivyaktivikas_add = login_required(abhivyaktivikas_add)
project_add = login_required(project_add)
competitiveexam_add = login_required(competitiveexam_add)
cocurricular_add = login_required(cocurricular_add)
socialactivity_add = login_required(socialactivity_add)
workexperience_add = login_required(workexperience_add)
physicalfitnessinfo_add = login_required(physicalfitnessinfo_add)
thinkingskill_add = login_required(thinkingskill_add)
socialskill_add = login_required(socialskill_add)
attitudetowardsschool_add = login_required(attitudetowardsschool_add)
emotionalskill_add = login_required(emotionalskill_add)
values_add = login_required(values_add)
report=login_required(report)
reportPDF=login_required(reportPDF)
certificatePDF = login_required(certificatePDF)
cardsPDF=login_required(cardsPDF)
display_report = login_required(display_report)
generate_name_columns = login_required(generate_name_columns)
