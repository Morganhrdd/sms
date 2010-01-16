from jp_sms.pravesh.models import ClassRoom, Session, Student, HallTicket
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ['Number', 'Medium', 'Name', 'Capacity']
    search_fields = ['Number', 'Medium', 'Name', 'Capacity']

class SessionAdmin(admin.ModelAdmin):
    list_display = ['Number', 'Name', 'Start', 'End']
    search_fields = ['Number', 'Name', 'Start', 'End']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['FirstName', 'LastName', 'Email', 'Gender']
    search_fields = ['FirstName', 'LastName', 'Email', 'Gender']

class HallTicketAdmin(admin.ModelAdmin):
    list_display = ['Student', 'ClassRoom', 'SeatNumber']
    search_fields = ['Student__FirstName', 'Student__LastName', 'SeatNumber']

admin.site.register(ClassRoom, ClassRoomAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(HallTicket, HallTicketAdmin)
