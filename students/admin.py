from jp_sms.students.models import StudentBasicInfo, StudentAdditionalInformation, AcademicYear, Teacher
from jp_sms.students.models import SubjectMaster, StudentYearlyInformation, ClassMaster, TestMapping
from jp_sms.students.models import StudentTestMarks, AttendanceMaster, StudentAttendance, PhysicalFitnessInfo
from jp_sms.students.models import SocialActivity, CoCurricular, CompetitiveExam, Competition
from jp_sms.students.models import AbhivyaktiVikas, Project, Elocution, Library, WorkExperience, PhysicalEducation
from jp_sms.students.models import ThinkingSkill, SocialSkill, EmotionalSkill, AttitudeTowardsSchool, Values
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
    search_fields = ['Id__RegistrationNo', 'Id__FirstName', 'Id__LastName']
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
    search_fields = ['StudentBasicInfo__FirstName', 'StudentBasicInfo__LastName', 'ClassMaster__Teacher__Name', 'RollNo', 'ClassMaster__Standard','ClassMaster__AcademicYear__Year', 'StudentBasicInfo__RegistrationNo']

class ClassMasterAdmin(admin.ModelAdmin):
    list_display = ('AcademicYear' ,'Standard', 'Division', 'Teacher', 'Type')
    ordering = ('AcademicYear', 'Standard', 'Division',)
    search_fields = ['AcademicYear__Year', 'Standard', 'Division', 'Teacher__Name']
    
class TestMappingAdmin(admin.ModelAdmin):
    list_display = ('SubjectMaster', 'TestType', 'MaximumMarks', 'Teacher', 'AcademicYear')
    search_fields = ['TestType', 'SubjectMaster__Name', 'Teacher__Name', 'AcademicYear__Year']
    
class StudentTestMarksAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'TestMapping', 'MarksObtained')
    search_fields = ['MarksObtained', 'TestMapping__SubjectMaster__Name', 'TestMapping__SubjectMaster__Standard', 'StudentYearlyInformation__StudentBasicInfo__FirstName', 'StudentYearlyInformation__StudentBasicInfo__LastName', 'TestMapping__Teacher__Name']

class AttendanceMasterAdmin(admin.ModelAdmin):
    list_display = ('ClassMaster', 'WorkingDays', 'Month',)
    search_fields = ('ClassMaster__Standard', 'ClassMaster__Division', 'Month', 'ClassMaster__AcademicYear__Year', 'ClassMaster__Teacher__Name')

class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation','AttendanceMaster', 'ActualAttendance',)
    search_fields = [ 'AttendanceMaster__ClassMaster__Teacher__Name', 'StudentYearlyInformation__StudentBasicInfo__RegistrationNo' ]

class PhysicalFitnessInfoAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'Weight','Height','FlexibleForwardBending','FlexibleBackwardBending','SBJ','VerticleJump','BallThrow','ShuttleRun','SitUps','Sprint','Running400m','ShortPutThrow','Split','BodyMassIndex','Balancing','PrivateComment','PublicComment','Pathak','Pratod','Margadarshak','SpecialSport','Grade')
    search_fields = ('StudentYearlyInformation__StudentBasicInfo__FirstName', 'StudentYearlyInformation__StudentBasicInfo__LastName', 'StudentYearlyInformation__StudentBasicInfo__RegistrationNo')
    
class SocialActivityAdmin(admin.ModelAdmin):
    pass

class CoCurricularAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'Activity', 'Objectives', 'Date', 'Guide', 'Grade')
    search_fields = ('StudentYearlyInformation__StudentBasicInfo__FirstName', 'Activity', 'Guide')

class CompetitiveExamAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'Name', 'Subject', 'Level', 'Date', 'Grade')
    search_fields = ('StudentYearlyInformation__StudentBasicInfo__FirstName', 'Name', 'Subject', 'Level', 'StudentYearlyInformation__StudentBasicInfo__RegistrationNo')

class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'Organizer', 'Subject', 'Date', 'Achievement', 'Guide')
    search_fields = ('StudentYearlyInformation__StudentBasicInfo__FirstName', 'Subject', 'Guide', 'Organizer', 'StudentYearlyInformation__StudentBasicInfo__RegistrationNo')

class AbhivyaktiVikasAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'MediumOfExpression', 'Teacher', 'Participation', 'ReadinessToLearn', 'ContinuityInWork', 'SkillDevelopment', 'Creativity')
    search_fields = ('StudentYearlyInformation__StudentBasicInfo__FirstName', 'MediumOfExpression', 'Teacher__Name', 'StudentYearlyInformation__StudentBasicInfo__RegistrationNo')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'Title', 'Type', 'Subject', 'ProblemSelection', 'Review', 'Planning', 'ExecutionAndHardWork', 'Documentation', 'Communication')
    search_fields = ['Title', 'StudentYearlyInformation__StudentBasicInfo__FirstName', 'StudentYearlyInformation__StudentBasicInfo__LastName', 'Subject', 'Type', 'StudentYearlyInformation__StudentBasicInfo__RegistrationNo']

class ElocutionAdmin(admin.ModelAdmin):
    list_display = ('Title', 'StudentYearlyInformation', 'Memory', 'Content', 'Understanding', 'Pronunciation', 'Presentation',)
    search_fields = ['Title', 'StudentYearlyInformation__StudentBasicInfo__FirstName', 'StudentYearlyInformation__StudentBasicInfo__LastName']

class LibraryAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'BooksRead', 'Grade', 'PublicComment', 'PrivateComment')
    search_fields = ['StudentYearlyInformation__StudentBasicInfo__FirstName', 'StudentYearlyInformation__StudentBasicInfo__LastName', 'PublicComment', 'PrivateComment']

class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'Teacher', 'Task', 'Communication', 'Confidence', 'Involvement')
    search_fields = ['StudentYearlyInformation__StudentBasicInfo__FirstName', 'StudentYearlyInformation__StudentBasicInfo__LastName']

class PhysicalEducationAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'Name', 'Pratod', 'AbilityToWorkInTeam', 'Cooperation', 'LeadershipSkill')
    search_fields = ['StudentYearlyInformation__StudentBasicInfo__FirstName', 'StudentYearlyInformation__StudentBasicInfo__LastName']
class ThinkingSkillAdmin(admin.ModelAdmin):   
    list_display = ('StudentYearlyInformation', 'Teacher', 'Inquiry','LogicalThinking', 'Creativity', 'DecisionMakingAndProblemSolving')
    search_fields = ['StudentYearlyInformation__StudentBasicInfo__FirstName', 'StudentYearlyInformation__StudentBasicInfo__LastName']

class SocialSkillAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'Teacher', 'Communication', 'InterPersonal', 'TeamWork')
    search_fields = ['StudentYearlyInformation__StudentBasicInfo__FirstName', 'StudentYearlyInformation__StudentBasicInfo__LastName']

class EmotionalSkillAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'Teacher', 'Empathy', 'Expression', 'Management')
    search_fields = ['StudentYearlyInformation__StudentBasicInfo__FirstName', 'StudentYearlyInformation__StudentBasicInfo__LastName']

class AttitudeTowardsSchoolAdmin(admin.ModelAdmin):
    list_display = ('StudentYearlyInformation', 'Teacher', 'SchoolTeachers', 'SchoolMates', 'SchoolPrograms', 'SchoolEnvironment')    
    search_fields = ['StudentYearlyInformation__StudentBasicInfo__FirstName', 'StudentYearlyInformation__StudentBasicInfo__LastName']

class ValuesAdmin(admin.ModelAdmin):
    search_fields = ['StudentYearlyInformation__StudentBasicInfo__FirstName', 'StudentYearlyInformation__StudentBasicInfo__LastName']


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
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(PhysicalEducation, PhysicalEducationAdmin)
admin.site.register(ThinkingSkill, ThinkingSkillAdmin)
admin.site.register(SocialSkill, SocialSkillAdmin)
admin.site.register(EmotionalSkill, EmotionalSkillAdmin)
admin.site.register(AttitudeTowardsSchool, AttitudeTowardsSchoolAdmin)
admin.site.register(Values, ValuesAdmin)