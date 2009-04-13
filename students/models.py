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
    ('5', 'Outstanding'),
    ('4', 'Excellent'),
    ('3', 'Good'),
    ('2', 'Satisfactory'),
    ('1', 'Needs Improvement'),
    ('0', 'Unsatisfactory'),
)

PROJECT_TYPE_CHOICES = (
    ('CC', 'Collection, Classification'),
    ('MM', 'Model Making'),
    ('IS', 'Investivation by Survey'),
    ('I', 'Investigation'),
    ('CP', 'Creative production'),
    ('AC', 'Appreciation-criticism'),
    ('O', 'Open ended exploration'),
)

class StudentBasicInfo(models.Model):
    RegistrationNo = models.PositiveIntegerField(primary_key=True)
    DateOfRegistration = models.DateField()
    FirstName = models.CharField(max_length=30)
    LastName = models.CharField(max_length=30)
    DateOfBirth = models.DateField()
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    FathersName = models.CharField(max_length=60)
    MothersName = models.CharField(max_length=60)
    TerminationDate = models.DateField()
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
    Email = models.EmailField()
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
    Weight = models.PositiveIntegerField()
    Height = models.PositiveIntegerField()
    FlexibleForwardBending = models.PositiveIntegerField()
    FlexibleBackwardBending = models.PositiveIntegerField()
    SBJ = models.PositiveIntegerField()
    VerticleJump = models.PositiveIntegerField()
    BallThrow = models.PositiveIntegerField()
    ShuttleRun = models.PositiveIntegerField()
    SitUps = models.PositiveIntegerField()
    Sprint = models.PositiveIntegerField()
    Running400m = models.PositiveIntegerField()
    ShortPutThrow = models.PositiveIntegerField()
    Split = models.PositiveIntegerField()
    BodyMassIndex = models.FloatField()
    Balancing = models.PositiveIntegerField()
    PrivateComment = models.CharField(max_length=200)
    PublicComment = models.CharField(max_length=200)
    Pathak = models.CharField(max_length=50)
    Pratod = models.CharField(max_length=50)
    Margadarshak = models.CharField(max_length=50)
    SpecialSport = models.CharField(max_length=50)
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
    Date = models.DateField()
    Grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)

class Competition(models.Model):
    StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
    Organizer = models.CharField(max_length=50)
    Subject = models.CharField(max_length=30)
    Date = models.DateField()
    Achievement = models.CharField(max_length=20)
    Guide = models.CharField(max_length=30)
    PublicComment = models.CharField(max_length=200)
    PrivateComment = models.CharField(max_length=200)

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
    Skill = models.CharField(max_length=1, choices=GRADE_CHOICES)
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
    