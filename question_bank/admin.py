from sms.question_bank.models import *
from django.contrib import admin

class ObjectiveTypeAdmin(admin.ModelAdmin):
    list_display = ['Name']
    search_fields = ['Name']

class ObjectiveLengthAdmin(admin.ModelAdmin):
    list_display = ['Name']
    search_fields = ['Name']

class MarksAdmin(admin.ModelAdmin):
    list_display = ['Value']
    search_fields = ['Value']

class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ['Level', 'Comment']
    search_fields = ['Level', 'Comment']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['Content', 'ObjectiveType', 'ObjectiveLength', 'Marks', 'DifficultyLevel', 'ExpectedTime', 'Standard', 'Subject']
    search_fields = ['Content', 'ObjectiveType', 'ObjectiveLength', 'Marks', 'DifficultyLevel', 'ExpectedTime', 'Standard', 'Subject']


admin.site.register(ObjectiveType, ObjectiveTypeAdmin)
admin.site.register(ObjectiveLength, ObjectiveLengthAdmin)
admin.site.register(Marks, MarksAdmin)
admin.site.register(DifficultyLevel, DifficultyLevelAdmin)
admin.site.register(Question, QuestionAdmin)

