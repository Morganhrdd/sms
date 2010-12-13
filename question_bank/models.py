from django.db import models

# Create your models here.

class ObjectiveType(models.Model):
    Name = models.CharField(max_length=100)
    def __unicode__(self):
        return "%s" % (self.Name)

class ObjectiveLength(models.Model):
    Name = models.CharField(max_length=100)
    def __unicode__(self):
        return "%s" % (self.Name)

class Marks(models.Model):
    Value = models.FloatField()
    def __unicode__(self):
        return "%5.2f" % (self.Value)
    class Meta:
        verbose_name_plural = "Marks"


class DifficultyLevel(models.Model):
    Level = models.PositiveIntegerField()
    Comment = models.CharField(max_length=200)
    def __unicode__(self):
        return "%s" % (self.Comment)

class Question(models.Model):
    Content = models.TextField(max_length=5000)
    ObjectiveType = models.ForeignKey(ObjectiveType)
    ObjectiveLength = models.ForeignKey(ObjectiveLength)
    Marks = models.ForeignKey(Marks)
    DifficultyLevel = models.ForeignKey(DifficultyLevel)
    ExpectedTime = models.FloatField()
    Unit = models.CharField(max_length=500)
    Standard = models.CharField(max_length=100, help_text='Common seperated standards')
