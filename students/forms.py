from django import forms
from django.forms.extras.widgets import SelectDateWidget

from sms.students.vars import *
from sms.students.models import *
    
class SearchDetailsForm(forms.Form):
    Year = forms.CharField(max_length=9)
    RegistrationNo = forms.IntegerField(required=False)
    FirstName = forms.CharField(required=False)
    LastName = forms.CharField(required=False)

class SearchClassDetailsForm(forms.Form):
    Year = forms.CharField(max_length=9)
    Standard = forms.IntegerField()
    Division = forms.CharField()
    Columns = forms.IntegerField()

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
    DescriptiveIndicator = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class ElocutionDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Title = forms.CharField(max_length=50)
    Memory = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    Content = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    Understanding = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    Pronunciation = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    Presentation = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    DescriptiveIndicator = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class ProjectDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Title = forms.CharField(max_length=50)
    Type = forms.ChoiceField(choices=PROJECT_TYPE_CHOICES, initial='N')
    Subject = forms.CharField(max_length=50)
    ProblemSelection = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    Review = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    Planning = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    ExecutionAndHardWork = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    Documentation = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    Communication = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    DescriptiveIndicator = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
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
    DescriptiveIndicator = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class CompetitiveExamDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Name = forms.CharField(max_length=30)
    Subject = forms.CharField(max_length=30)
    Level = forms.CharField(max_length=30)
    Date = forms.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    Grade = forms.CharField(max_length=20, required=False)
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    DescriptiveIndicator = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class CoCurricularDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Activity = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), max_length=50)
    Objectives = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), max_length=200)
    Date = forms.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    Guide = forms.CharField(max_length=30, required=False)
    Grade = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    DescriptiveIndicator = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class SocialActivityDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Activity = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), max_length=50)
    Objectives = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), max_length=200)
    Date = forms.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    Organizer = forms.CharField(max_length=30, required=False)
    Grade = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    DescriptiveIndicator = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
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
    DescriptiveIndicator = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Pathak = forms.CharField(max_length=50, required=False)
    Pratod = forms.CharField(max_length=50, required=False)
    Margadarshak = forms.CharField(max_length=50, required=False)
    SpecialSport = forms.CharField(max_length=50, required=False)
    Grade = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
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
    DescriptiveIndicator = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
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
    DescriptiveIndicator = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class ThinkingSkillDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Inquiry = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    LogicalThinking = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Creativity = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    DecisionMakingAndProblemSolving = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    DescriptiveIndicator = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class SocialSkillDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Communication = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    InterPersonal = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    TeamWork = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    DescriptiveIndicator = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class EmotionalSkillDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Empathy = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Expression = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    Management = forms.ChoiceField(choices=GRADE_CHOICES, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    DescriptiveIndicator = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class AttitudeTowardsSchoolDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    SchoolTeachers = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    SchoolMates = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    SchoolPrograms = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    SchoolEnvironment = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    DescriptiveIndicator = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)

class ValuesDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Obedience = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    Honesty = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    Equality = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    Responsibility = forms.ChoiceField(choices=GRADE_CHOICES_3, initial='0')
    PublicComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    PrivateComment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    DescriptiveIndicator = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Delete = forms.CharField(required=False)
    
#
class MedicalReportForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk=forms.IntegerField(widget=pkwidget, required=False)
    Height = forms.FloatField(help_text="In cms")
    Weight = forms.FloatField(help_text="In kgs")
    BloodGroup = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, initial='0')
    VisionL = forms.CharField()
    VisionR = forms.CharField()
    Teeth = forms.CharField()
    OralHygiene = forms.CharField()
    SpecificAilment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    Doctor = forms.CharField()
    ClinicAddress = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))
    Phone = forms.CharField(required=False)
    Delete = forms.CharField(required=False)

class ScrapDetailsForm(forms.Form):
    pkwidget = forms.HiddenInput()
    pk = forms.IntegerField(widget=pkwidget, required=False)
    data = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    User = forms.CharField()
    Delete = forms.CharField(required=False)
