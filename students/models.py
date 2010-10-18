from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

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

GRADE_CHOICES_3 = (
    ('0', 'None'),
    ('1', 'Satisfactory'),
    ('2', 'Good'),
    ('3', 'Outstanding'),
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
	(1, 'No Hostel'),
	(2, 'Full Hostel'),
	(3, 'Half Hostel'),
)

BLOOD_GROUP_CHOICES = (
    ('0', 'None'),
    ('A+', 'A+'),
    ('B+', 'B+'),
    ('AB+', 'AB+'),
    ('O+', 'O+'),
    ('A+', 'A-'),
    ('B+', 'B-'),
    ('AB-', 'AB-'),
    ('O-', 'O-'),
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
    ReasonOfLeavingSchool = models.TextField(max_length=100, blank=True)
    PreviousSchool = models.CharField(max_length=200, blank=True)
    Category = models.CharField(max_length=200, blank=True)
    def __unicode__(self):
        return "%d-%s %s" % (self.RegistrationNo, self.FirstName, self.LastName)
    

class StudentAdditionalInformation(models.Model):
    Id = models.ForeignKey(StudentBasicInfo, primary_key=True)
    Address = models.TextField(max_length=300)
    Strength = models.TextField(max_length=200, blank=True)
    Weakness = models.TextField(max_length=200, blank=True)
    Hobbies = models.TextField(max_length=200, blank=True)
    Family_Background = models.TextField(max_length=200, blank=True)
    Fathers_Income = models.CharField(max_length=60, blank=True)
    Fathers_Education = models.CharField(max_length=100, blank=True)
    Fathers_Occupation = models.CharField(max_length=100, blank=True)
    Fathers_Phone_No = models.CharField(max_length=15, blank=True)
    Fathers_Email = models.EmailField(blank=True)
    Mothers_Income = models.CharField(max_length=60, blank=True)
    Mothers_Education = models.CharField(max_length=100, blank=True)
    Mothers_Occupation = models.CharField(max_length=100, blank=True)
    Mothers_Phone_No = models.CharField(max_length=15, blank=True)
    Mothers_Email = models.EmailField(blank=True)
    class Meta:
        verbose_name_plural = "Student Additional Information"

class Scrap(models.Model):
    User = models.ForeignKey(User)
    StudentBasicInfo = models.ForeignKey(StudentBasicInfo)
    date = models.DateField()
    data = models.CharField(max_length=500)


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
    Sankalp = models.TextField(max_length=200, blank=True)
    Sankalp_Comment = models.TextField(max_length=200, blank=True)
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
    Height = models.FloatField(blank=True, null=True)
    FlexibleForwardBending = models.FloatField(blank=True, null=True)
    FlexibleBackwardBending = models.FloatField(blank=True, null=True)
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
    PrivateComment = models.TextField(max_length=200,blank=True, null=True)
    PublicComment = models.TextField(max_length=200,blank=True, null=True)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)
    Pathak = models.CharField(max_length=50,blank=True, null=True)
    Pratod = models.CharField(max_length=50,blank=True, null=True)
    Margadarshak = models.CharField(max_length=50,blank=True, null=True)
    SpecialSport = models.CharField(max_length=50,blank=True, null=True)
    Grade = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    class Meta:
        verbose_name_plural = "Physical Fitness Information"

class SocialActivity(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Activity = models.CharField(max_length=50)
    Objectives = models.CharField(max_length=200)
    Date = models.DateField()
    Organizer = models.CharField(max_length=50)
    Grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.TextField(max_length=200)
    PrivateComment = models.TextField(max_length=200)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)
    class Meta:
        verbose_name_plural = "Social Activities"

class CoCurricular(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Activity = models.CharField(max_length=50)
    Objectives = models.CharField(max_length=200)
    Date = models.DateField()
    Guide = models.CharField(max_length=30)
    Grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.TextField(max_length=200)
    PrivateComment = models.TextField(max_length=200)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)
    def __unicode__(self):
        return "%s, %s" % (self.Activity, self.StudentYearlyInformation)

class CompetitiveExam(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Name = models.CharField(max_length=30)
    Subject = models.CharField(max_length=30)
    Level = models.CharField(max_length=30)
    Date = models.DateField(blank=True, null=True)
    Grade = models.CharField(max_length=50)
    PublicComment = models.TextField(max_length=200)
    PrivateComment = models.TextField(max_length=200)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)
    def __unicode__(self):
        return "%s, %s" % (self.Name, self.StudentYearlyInformation)

class Competition(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Organizer = models.CharField(max_length=50)
    Subject = models.CharField(max_length=30)
    Date = models.DateField()
    Achievement = models.CharField(max_length=20, blank=True)
    Guide = models.CharField(max_length=30)
    PublicComment = models.TextField(max_length=200, blank=True)
    PrivateComment = models.TextField(max_length=200, blank=True)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)
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
    PublicComment = models.TextField(max_length=200)
    PrivateComment = models.TextField(max_length=200)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)
    class Meta:
        verbose_name_plural = "Abhivyakti Vikas"
    def __unicode__(self):
        return "%s, %s" % (self.MediumOfExpression, self.StudentYearlyInformation)

class Project(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Title = models.CharField(max_length=30)
    Type = models.CharField(max_length=2, choices=PROJECT_TYPE_CHOICES)
    Subject = models.CharField(max_length=30)
    ProblemSelection = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    Review = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    Planning = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    ExecutionAndHardWork = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    Documentation = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    Communication = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    PublicComment = models.TextField(max_length=200)
    PrivateComment = models.TextField(max_length=200)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)

class Elocution(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Title = models.CharField(max_length=30)
    Memory = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    Content = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    Understanding = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    Pronunciation = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    Presentation = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    PublicComment = models.TextField(max_length=200)
    PrivateComment = models.TextField(max_length=200)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)
    def __unicode__(self):
        return "%s, %s" % (self.Title, self.StudentYearlyInformation)

class Library(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    BooksRead = models.PositiveIntegerField()
    Grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.TextField(max_length=200)
    PrivateComment = models.TextField(max_length=200)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)
    class Meta:
        verbose_name_plural = "Libraries"

class WorkExperience(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Teacher = models.ForeignKey(Teacher)
    Task = models.CharField(max_length=200)
    Communication = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Confidence = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Involvement = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.TextField(max_length=200)
    PrivateComment = models.TextField(max_length=200)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)

class PhysicalEducation(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Name = models.CharField(max_length=50)
    Pratod = models.CharField(max_length=50,blank=True, null=True)
    AbilityToWorkInTeam = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Cooperation = models.CharField(max_length=1, choices=GRADE_CHOICES)
    LeadershipSkill = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.TextField(max_length=200)
    PrivateComment = models.TextField(max_length=200)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)

class ThinkingSkill(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Teacher = models.ForeignKey(Teacher)
    Inquiry = models.CharField(max_length=1, choices=GRADE_CHOICES)
    LogicalThinking = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Creativity = models.CharField(max_length=1, choices=GRADE_CHOICES)
    DecisionMakingAndProblemSolving = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.TextField(max_length=200)
    PrivateComment = models.TextField(max_length=200)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)

class SocialSkill(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Teacher = models.ForeignKey(Teacher)
    Communication = models.CharField(max_length=1, choices=GRADE_CHOICES)
    InterPersonal = models.CharField(max_length=1, choices=GRADE_CHOICES)
    TeamWork = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.TextField(max_length=200)
    PrivateComment = models.TextField(max_length=200)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)

class EmotionalSkill(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Teacher = models.ForeignKey(Teacher)
    Empathy = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Expression = models.CharField(max_length=1, choices=GRADE_CHOICES)
    Management = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.TextField(max_length=200)
    PrivateComment = models.TextField(max_length=200)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)

class AttitudeTowardsSchool(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Teacher = models.ForeignKey(Teacher)
    SchoolTeachers = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    SchoolMates = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    SchoolPrograms = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    SchoolEnvironment = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    PublicComment = models.TextField(max_length=200)
    PrivateComment = models.TextField(max_length=200)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)

class Values(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Teacher = models.ForeignKey(Teacher)
    Obedience = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    Honesty = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    Equality = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    Responsibility = models.CharField(max_length=1, choices=GRADE_CHOICES_3)
    PublicComment = models.TextField(max_length=200)
    PrivateComment = models.TextField(max_length=200)
    DescriptiveIndicator = models.TextField(max_length=200,blank=True, null=True)
    class Meta:
        verbose_name_plural = "Values"

class MedicalReport(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Height = models.FloatField()
    Weight = models.FloatField()
    BloodGroup = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    VisionL = models.TextField(max_length=200)
    VisionR = models.TextField(max_length=200)
    Teeth = models.TextField(max_length=200)
    OralHygiene = models.TextField(max_length=200)
    SpecificAilment = models.TextField(max_length=200)
    Doctor = models.TextField(max_length=200)
    ClinicAddress = models.TextField(max_length=200)
    Phone = models.CharField(max_length=15)
