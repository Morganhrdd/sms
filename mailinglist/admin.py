from sms.mailinglist.models import *
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class PersonAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Address', 'City', 'Taluka', 'District', 'PinCode', 'Phone')
    ordering = ('Name',)
    search_fields =['Name', 'Address', 'City', 'Taluka', 'District', 'PinCode', 'Phone']
    

admin.site.register(Person, PersonAdmin)

