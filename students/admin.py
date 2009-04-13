from jp_sms.students.models import StudentBasicInfo, StudentAdditionalInformation, AcademicYear, Teacher
from jp_sms.students.models import SubjectMaster, StudentYearlyInformation, ClassMaster, TestMapping
from jp_sms.students.models import StudentTestMarks, AttendanceMaster, StudentAttendance, PhysicalFitnessInfo
from jp_sms.students.models import SocialActivity, CoCurricular, CompetitiveExam, Competition
from jp_sms.students.models import AbhivyaktiVikas, Project, Elocution, Library
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class StudentBasicInfoAdmin(admin.ModelAdmin):
    list_display = ('RegistrationNo', 'DateOfRegistration', 'FirstName', 'LastName', 'DateOfBirth', 'Gender', 'FathersName', 'MothersName')
    ordering = ('RegistrationNo',)
    search_fields =['RegistrationNo', 'FirstName', 'LastName',]
    
class StudentAdditionalInformationAdmin(admin.ModelAdmin):
    list_display = ('Id', 'Strength', 'Weakness', 'Sankalp', 'Sankalp_Comment', 'Hobbies', 'Family_Background', 'Fathers_Income',
                    'Fathers_Education', 'Fathers_Occupation', 'Fathers_Phone_No', 'Fathers_Email', 'Mothers_Income' ,'Mothers_Education',
                    'Mothers_Occupation', 'Mothers_Phone_No', 'Mothers_Email', 'Address')
    ordering = ('Id',)

class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('Year',)
    ordering = ('Year',)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Email', 'ResidenceNo', 'MobileNo')
    ordering = ('Name',)
    search_fields = ['Name', 'MobileNo', 'ResidenceNo', 'Email',]
    
class SubjectMasterAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Standard',)
    ordering = ('Name', 'Standard',)
    search_fields = ['Name', 'Standard']

class StudentYearlyInformationAdmin(admin.ModelAdmin):
    list_display = ('StudentBasicInfo', 'RollNo', 'ClassMaster', 'Photo')
    ordering = ('ClassMaster', 'RollNo', )
    search_fields = ['StudentBasicInfo__FirstName', 'StudentBasicInfo__LastName', 'ClassMaster__Teacher__Name', 'RollNo', 'ClassMaster__Standard','ClassMaster__AcademicYear__Year']

class ClassMasterAdmin(admin.ModelAdmin):
    list_display = ('AcademicYear' ,'Standard', 'Division', 'Teacher')
    ordering = ('AcademicYear', 'Standard', 'Division',)
    
class TestMappingAdmin(admin.ModelAdmin):
    list_display = ('SubjectMaster', 'TestType', 'MaximumMarks', 'Teacher', 'AcademicYear')
    search_fields = ['TestType', 'SubjectMaster__Name', 'Teacher__Name', 'AcademicYear__Year']
    
class StudentTestMarksAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'TestMapping', 'MarksObtained')
    search_fields = ['MarksObtained', 'TestMapping__SubjectMaster__Name', 'TestMapping__SubjectMaster__Standard', 'StudentYearlyInformation__StudentBasicInfo__FirstName', 'StudentYearlyInformation__StudentBasicInfo__LastName', 'TestMapping__Teacher__Name']

class AttendanceMasterAdmin(admin.ModelAdmin):
    list_display = ('ClassMaster', 'WorkingDays')
    
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('AttendanceMaster', 'ActualAttendance')

class PhysicalFitnessInfoAdmin(admin.ModelAdmin):
    list_display = ('Weight', 'Height')
    
class SocialActivityAdmin(admin.ModelAdmin):
    pass

class CoCurricularAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'Activity', 'Objectives', 'Date', 'Guide', 'Grade')
    search_fields = ('StudentYearlyInformation__StudentBasicInfo__FirstName', 'Activity')
    pass

class CompetitiveExamAdmin(admin.ModelAdmin):
    pass

class CompetitionAdmin(admin.ModelAdmin):
    pass

class AbhivyaktiVikasAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'MediumOfExpression', 'Teacher', 'Participation', 'ReadinessToLearn', 'ContinuityInWork', 'SkillDevelopment', 'Creativity')
    search_fields = ('StudentYearlyInformation__StudentBasicInfo__FirstName', 'MediumOfExpression', 'Teacher__Name')
    pass

class ProjectAdmin(admin.ModelAdmin):
    pass

class ElocutionAdmin(admin.ModelAdmin):
    list_display = ('Title', 'StudentYearlyInformation', 'Memory', 'Content', 'Understanding', 'Skill', 'Presentation',)
    search_fields = ['Title', 'StudentYearlyInformation__StudentBasicInfo__FirstName', 'StudentYearlyInformation__StudentBasicInfo__LastName']
    pass

class LibraryAdmin(admin.ModelAdmin):
    pass

admin.site.register(AttendanceMaster, AttendanceMasterAdmin)
admin.site.register(StudentAttendance, StudentAttendanceAdmin)
admin.site.register(StudentTestMarks, StudentTestMarksAdmin)
admin.site.register(TestMapping, TestMappingAdmin)
admin.site.register(ClassMaster, ClassMasterAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(SubjectMaster, SubjectMasterAdmin)
admin.site.register(StudentYearlyInformation, StudentYearlyInformationAdmin)
admin.site.register(AcademicYear, AcademicYearAdmin)
admin.site.register(StudentBasicInfo, StudentBasicInfoAdmin)
admin.site.register(StudentAdditionalInformation, StudentAdditionalInformationAdmin)
admin.site.register(PhysicalFitnessInfo, PhysicalFitnessInfoAdmin)
admin.site.register(SocialActivity, SocialActivityAdmin)
admin.site.register(CoCurricular, CoCurricularAdmin)
admin.site.register(CompetitiveExam, CompetitiveExamAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(AbhivyaktiVikas, AbhivyaktiVikasAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Elocution, ElocutionAdmin)
admin.site.register(Library, LibraryAdmin)