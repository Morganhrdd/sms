from django.conf.urls.defaults import *
from students import views
# The next two lines enable the admin and load each admin.py file:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^marks_add/', views.marks_add),
    (r'^attendance_add/', views.attendance_add),
    (r'^report/', views.report),
    # ... the rest of your URLs here ...
)
