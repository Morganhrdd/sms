from django.conf.urls.defaults import *
#from students import views
# The next two lines enable the admin and load each admin.py file:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^marks_add/', 'students.views.marks_add'),
    (r'^attendance_add/', 'students.views.attendance_add'),
    (r'^report/', 'students.views.report'),
    (r'^ams/', 'ams.views.get_barcode'),
    (r'^leave/', 'ams.views.app_leave'),
    #(r'^useradd/', views.user_add),
    # ... the rest of your URLs here ...
)
