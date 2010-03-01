from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms

CLASS_MASTER_CHOICES = (
    ('P', 'Prashala'),
    ('D', 'Dal'),
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

STANDARD_CHOICES = (
    (5, 'Fifth'),
    (6, 'Sixth'),
    (7, 'Seventh'),
    (8, 'Eighth'),
    (9, 'Nineth'),
    (10, 'Tenth'),
)

MONTH_CHOICES = (
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
)

DIVISION_CHOICES = (
    ('G', 'Girls'),
    ('B', 'Boys'),
)

EXAM_CHOICES = (
    ('D', 'Daily'),
    ('W', 'Weekly'),
    ('M', 'Monthly'),
    ('HY', 'Half Yearly'),
    ('Y', 'Yearly'),
)

GRADE_CHOICES = (
    ('0', 'None'),
    ('1', 'Unsatisfactory'),
    ('2', 'Needs Improvement'),
    ('3', 'Satisfactory'),
    ('4', 'Good'),
    ('5', 'Excellent'),
    ('6', 'Outstanding'),
)

PROJECT_TYPE_CHOICES = (
    ('CC', 'Collection, Classification'),
    ('MM', 'Model Making'),
    ('IS', 'Investivation by Survey'),
    ('I', 'Investigation'),
    ('CP', 'Creative production'),
    ('AC', 'Appreciation-criticism'),
    ('O', 'Open ended exploration'),
    ('N', 'None')
)

HOSTEL_CHOICES = (
	('1', 'No Hostel'),
	('2', 'Full Hostel'),
	('3', 'Half Hostel'),
)
	
class StudentBasicInfo(models.Model):
    RegistrationNo = models.PositiveIntegerField(primary_key=True)
    DateOfRegistration = models.DateField()
    FirstName = models.CharField(max_length=30)
    LastName = models.CharField(max_length=30)
    DateOfBirth = models.DateField()
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    FathersName = models.CharField(max_length=60, blank=True)
    MothersName = models.CharField(max_length=60, blank=True)
    TerminationDate = models.DateField(null=True, blank=True)
    Caste = models.CharField(max_length=50, blank=True)
    Nationality = models.CharField(max_length=50, blank=True)
    BirthPlace = models.CharField(max_length=50, blank=True)
    ReasonOfLeavingSchool = models.CharField(max_length=100, blank=True)
    PreviousSchool = models.CharField(max_length=200, blank=True)
    Category = models.CharField(max_length=200, blank=True)
    def __unicode__(self):
        return "%d-%s %s" % (self.RegistrationNo, self.FirstName, self.LastName)
    

class StudentAdditionalInformation(models.Model):
    Id = models.ForeignKey(StudentBasicInfo, primary_key=True)
    Strength = models.CharField(max_length=200)
    Weakness = models.CharField(max_length=200)
    Sankalp = models.CharField(max_length=200)
    Sankalp_Comment = models.CharField(max_length=200)
    Hobbies = models.CharField(max_length=200)
    Family_Background = models.CharField(max_length=200)
    Fathers_Income = models.CharField(max_length=60)
    Fathers_Education = models.CharField(max_length=100)
    Fathers_Occupation = models.CharField(max_length=100)
    Fathers_Phone_No = models.CharField(max_length=15)
    Fathers_Email = models.EmailField()
    Mothers_Income = models.CharField(max_length=60)
    Mothers_Education = models.CharField(max_length=100)
    Mothers_Occupation = models.CharField(max_length=100)
    Mothers_Phone_No = models.CharField(max_length=15)
    Mothers_Email = models.EmailField()
    Address = models.CharField(max_length=300)
    class Meta:
        verbose_name_plural = "Student Additional Information"


class AcademicYear(models.Model):
    Year = models.CharField(max_length=9, primary_key=True)
    def __unicode__(self):
        return str(self.Year)
    class Meta:
        verbose_name_plural = "Academic Years"


class Teacher(models.Model):
    Name = models.CharField(max_length=60, primary_key=True)
    Email = models.EmailField(unique=True)
    ResidenceNo = models.CharField(max_length=15)
    MobileNo = models.CharField(max_length=15)
    def __unicode__(self):
        return str(self.Name)


class SubjectMaster(models.Model):
    Name = models.CharField(max_length=50)
    Standard = models.PositiveIntegerField(choices=STANDARD_CHOICES)
    def __unicode__(self):
        return "%d - %s" % (self.Standard, self.Name)


class ClassMaster(models.Model):
    AcademicYear = models.ForeignKey(AcademicYear) 
    Standard = models.PositiveIntegerField(choices=STANDARD_CHOICES)
    Division = models.CharField(max_length=1, choices=DIVISION_CHOICES)
    Teacher = models.ForeignKey(Teacher)
    Type = models.CharField(max_length=1, choices=CLASS_MASTER_CHOICES)
    def __unicode__(self):
        return "%s %d %s %s" % (self.AcademicYear, self.Standard, self.Division, self.Teacher)


class StudentYearlyInformation(models.Model):
    StudentBasicInfo = models.ForeignKey(StudentBasicInfo)
    RollNo = models.PositiveIntegerField()
    ClassMaster = models.ForeignKey(ClassMaster)
    Photo = models.ImageField(upload_to='media', blank=True)
    Hostel = models.PositiveIntegerField(choices=HOSTEL_CHOICES)
    def __unicode__(self):
        return "%s, %d, %s" % (self.StudentBasicInfo, self.RollNo, self.ClassMaster)


class TestMapping(models.Model):
    SubjectMaster = models.ForeignKey(SubjectMaster)
    TestType = models.CharField(max_length=5)
    MaximumMarks = models.FloatField()
    Teacher = models.ForeignKey(Teacher)
    AcademicYear = models.ForeignKey(AcademicYear)
    def __unicode__(self):
        return "%s-%s-%s" % (self.SubjectMaster, self.TestType, self.Teacher)


class StudentTestMarks(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    TestMapping = models.ForeignKey(TestMapping)
    MarksObtained = models.FloatField()
    class Meta:
        verbose_name_plural = "Student Test Marks"
    def __unicode__(self):
        return "%s, %s, %f" % (self.StudentYearlyInformation, self.TestMapping, self.MarksObtained)


class AttendanceMaster(models.Model):
    ClassMaster = models.ForeignKey(ClassMaster)
    Month = models.PositiveIntegerField(choices=MONTH_CHOICES)
    WorkingDays = models.PositiveIntegerField()
    def __unicode__(self):
        return "%s, %d, %d" % (self.ClassMaster, self.Month, self.WorkingDays)


class StudentAttendance(models.Model):
    AttendanceMaster = models.ForeignKey(AttendanceMaster)
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    ActualAttendance = models.PositiveIntegerField()
    def __unicode__(self):
        return "%s" % (self.AttendanceMaster)

class PhysicalFitnessInfo(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Weight = models.FloatField(blank=True, null=True)
    Height = models.PositiveIntegerField(blank=True, null=True)
    FlexibleForwardBending = models.IntegerField(blank=True, null=True)
    FlexibleBackwardBending = models.IntegerField(blank=True, null=True)
    SBJ = models.FloatField(blank=True, null=True)
    VerticleJump = models.FloatField(blank=True, null=True)
    BallThrow = models.FloatField(blank=True, null=True)
    ShuttleRun = models.FloatField(blank=True, null=True)
    SitUps = models.PositiveIntegerField(blank=True, null=True)
    Sprint = models.FloatField(blank=True, null=True)
    Running400m = models.FloatField(blank=True, null=True)
    ShortPutThrow = models.FloatField(blank=True, null=True)
    Split = models.PositiveIntegerField(blank=True, null=True)
    BodyMassIndex = models.FloatField(blank=True, null=True)
    Balancing = models.PositiveIntegerField(blank=True, null=True)
    PrivateComment = models.CharField(max_length=200,blank=True, null=True)
    PublicComment = models.CharField(max_length=200,blank=True, null=True)
    Pathak = models.CharField(max_length=50,blank=True, null=True)
    Pratod = models.CharField(max_length=50,blank=True, null=True)
    Margadarshak = models.CharField(max_length=50,blank=True, null=True)
    SpecialSport = models.CharField(max_length=50,blank=True, null=True)
    Grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    class Meta:
        verbose_name_plural = "Physical Fitness Information"

class SocialActivity(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Activity = models.CharField(max_length=50)
    Objectives = models.CharField(max_length=200)
    Date = models.DateField()
    Organizer = models.CharField(max_length=50)
    Grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)
    class Meta:
        verbose_name_plural = "Social Activities"

class CoCurricular(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Activity = models.CharField(max_length=50)
    Objectives = models.CharField(max_length=200)
    Date = models.DateField()
    Guide = models.CharField(max_length=30)
    Grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)
    def __unicode__(self):
        return "%s, %s" % (self.Activity, self.StudentYearlyInformation)

class CompetitiveExam(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Name = models.CharField(max_length=30)
    Subject = models.CharField(max_length=30)
    Level = models.CharField(max_length=30)
    Date = models.DateField(blank=True, null=True)
    Grade = models.CharField(max_length=50)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)
    def __unicode__(self):
        return "%s, %s" % (self.Name, self.StudentYearlyInformation)

class Competition(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Organizer = models.CharField(max_length=50)
    Subject = models.CharField(max_length=30)
    Date = models.DateField()
    Achievement = models.CharField(max_length=20, blank=True)
    Guide = models.CharField(max_length=30)
    PublicComment = models.CharField(max_length=200, blank=True)
    PrivateComment = models.CharField(max_length=200, blank=True)
    def __unicode__(self):
        return "%s, %s" % (self.Subject, self.StudentYearlyInformation)

class AbhivyaktiVikas(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    MediumOfExpression = models.CharField(max_length=10)
    Teacher = models.ForeignKey(Teacher)
    Participation = models.CharField(max_length=1, choices=GRADE_CHOICES)
    ReadinessToLearn = models.CharField(max_length=1, choices=GRADE_CHOICES)
    ContinuityInWork = models.CharField(max_length=1, choices=GRADE_CHOICES)
    SkillDevelopment = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Creativity = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)
    class Meta:
        verbose_name_plural = "Abhivyakti Vikas"
    def __unicode__(self):
        return "%s, %s" % (self.MediumOfExpression, self.StudentYearlyInformation)

class Project(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Title = models.CharField(max_length=30)
    Type = models.CharField(max_length=2, choices=PROJECT_TYPE_CHOICES)
    Subject = models.CharField(max_length=30)
    ProblemSelection = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Review = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Planning = models.CharField(max_length=1, choices=GRADE_CHOICES)
    ExecutionAndHardWork = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Documentation = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Communication = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)

class Elocution(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Title = models.CharField(max_length=30)
    Memory = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Content = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Understanding = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Pronunciation = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Presentation = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)
    def __unicode__(self):
        return "%s, %s" % (self.Title, self.StudentYearlyInformation)

class Library(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    BooksRead = models.PositiveIntegerField()
    Grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)
    class Meta:
        verbose_name_plural = "Libraries"

class WorkExperience(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Teacher = models.ForeignKey(Teacher)
    Task = models.CharField(max_length=200)
    Communication = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Confidence = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Involvement = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)

class PhysicalEducation(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Name = models.CharField(max_length=50)
    Pratod = models.CharField(max_length=50,blank=True, null=True)
    AbilityToWorkInTeam = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Cooperation = models.CharField(max_length=1, choices=GRADE_CHOICES)
    LeadershipSkill = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)

class ThinkingSkill(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Teacher = models.ForeignKey(Teacher)
    Inquiry = models.CharField(max_length=1, choices=GRADE_CHOICES)
    LogicalThinking = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Creativity = models.CharField(max_length=1, choices=GRADE_CHOICES)
    DecisionMakingAndProblemSolving = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)

class SocialSkill(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Teacher = models.ForeignKey(Teacher)
    Communication = models.CharField(max_length=1, choices=GRADE_CHOICES)
    InterPersonal = models.CharField(max_length=1, choices=GRADE_CHOICES)
    TeamWork = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)

class EmotionalSkill(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Teacher = models.ForeignKey(Teacher)
    Empathy = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Expression = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Management = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)

class AttitudeTowardsSchool(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Teacher = models.ForeignKey(Teacher)
    SchoolTeachers = models.CharField(max_length=1, choices=GRADE_CHOICES)
    SchoolMates = models.CharField(max_length=1, choices=GRADE_CHOICES)
    SchoolPrograms = models.CharField(max_length=1, choices=GRADE_CHOICES)
    SchoolEnvironment = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)

class Values(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Teacher = models.ForeignKey(Teacher)
    Obedience = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Honesty = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Equality = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Responsibility = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)
    class Meta:
        verbose_name_plural = "Values"

class SearchDetailsForm(forms.Form):
    Year = forms.CharField(max_length=9)
    RegistrationNo = forms.IntegerField()

class CompetitionDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Organizer = forms.CharField(max_length=50)
    Subject = forms.CharField(max_length=30)
    Date = forms.DateField()
    Achievement = forms.CharField(max_length=20, required=False)
    Guide = forms.CharField(max_length=30, required=False)
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class ElocutionDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Title = forms.CharField(max_length=50)
    Memory = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Content = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Understanding = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Pronunciation = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Presentation = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class ProjectDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Title = forms.CharField(max_length=50)
    Type = forms.ChoiceField(choices=PROJECT_TYPE_CHOICES, initial='N')
    Subject = forms.CharField(max_length=50)
    ProblemSelection = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Review = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Planning = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    ExecutionAndHardWork = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Documentation = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Communication = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)
    

class AbhivyaktiVikasDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    MediumOfExpression = forms.CharField(max_length=10)
    Teacher = forms.ModelChoiceField(Teacher.objects.all())
    Participation = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    ReadinessToLearn = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    ContinuityInWork = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    SkillDevelopment = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Creativity = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class CompetitiveExamDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Name = forms.CharField(max_length=30)
    Subject = forms.CharField(max_length=30)
    Level = forms.CharField(max_length=30)
    Date = forms.DateField()
    Grade = forms.CharField(max_length=20, required=False)
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class CoCurricularDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Activity = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), max_length=50)
    Objectives = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), max_length=200)
    Date = forms.DateField()
    Guide = forms.CharField(max_length=30, required=False)
    Grade = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class SocialActivityDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Activity = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), max_length=50)
    Objectives = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), max_length=200)
    Date = forms.DateField()
    Organizer = forms.CharField(max_length=30, required=False)
    Grade = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)
    
class PhysicalFitnessInfoDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Weight = forms.FloatField(required=False)
    Height = forms.IntegerField(required=False)
    FlexibleForwardBending = forms.IntegerField(required=False)
    FlexibleBackwardBending = forms.IntegerField(required=False)
    SBJ = forms.FloatField(required=False)
    VerticleJump = forms.FloatField(required=False)
    BallThrow = forms.FloatField(required=False)
    ShuttleRun = forms.FloatField(required=False)
    SitUps = forms.IntegerField(required=False)
    Sprint = forms.FloatField(required=False)
    Running400m = forms.FloatField(required=False)
    ShortPutThrow = forms.FloatField(required=False)
    Split = forms.IntegerField(required=False)
    BodyMassIndex = forms.FloatField(required=False)
    Balancing = forms.IntegerField(required=False)
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Pathak = forms.CharField(max_length=50, required=False)
    Pratod = forms.CharField(max_length=50, required=False)
    Margadarshak = forms.CharField(max_length=50, required=False)
    SpecialSport = forms.CharField(max_length=50, required=False)
    Grade = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Delete = forms.CharField(required=False)

class WorkExperienceDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Teacher = forms.ModelChoiceField(Teacher.objects.all())
    Task = forms.CharField(max_length=200)
    Communication = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Confidence = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Involvement = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class PhysicalEducationDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Name = forms.CharField(max_length=50)
    Pratod = forms.CharField(max_length=50, required=False)
    AbilityToWorkInTeam = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Cooperation = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    LeadershipSkill = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class ThinkingSkillDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    #Teacher = forms.ModelChoiceField(Teacher.objects.all())
    Inquiry = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    LogicalThinking = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Creativity = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    DecisionMakingAndProblemSolving = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class SocialSkillDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Teacher = forms.ModelChoiceField(Teacher.objects.all())
    Communication = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    InterPersonal = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    TeamWork = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class EmotionalSkillDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Teacher = forms.ModelChoiceField(Teacher.objects.all())
    Empathy = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Expression = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Management = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class AttitudeTowardsSchoolDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Teacher = forms.ModelChoiceField(Teacher.objects.all())
    SchoolTeachers = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    SchoolMates = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    SchoolPrograms = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    SchoolEnvironment = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class ValuesDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Teacher = forms.ModelChoiceField(Teacher.objects.all())
    Obedience = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Honesty = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Equality = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Responsibility = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)
    