from django.db import models

# Create your models here.

class TypeByObjective(models.Model):
    Name = models.CharField(max_length=100)
    def __unicode__(self):
        return "%s" % (self.Name)

class TypeByLength(models.Model):
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
    TypeByObjective= models.ForeignKey(TypeByObjective)
    TypeByLength= models.ForeignKey(TypeByLength)
    Marks = models.ForeignKey(Marks)
    DifficultyLevel = models.ForeignKey(DifficultyLevel)
    ExpectedTime = models.FloatField()
    Subject = models.CharField(max_length=200)
    Unit = models.CharField(max_length=500)
    Standard = models.CharField(max_length=100, help_text='Common seperated standards')
